import subprocess
import RPi.GPIO as GPIO
import time
import re
import json
import dht11

RECYCLING_PIN = 24
COMPOST_PIN = 25
DHT_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(RECYCLING_PIN, GPIO.OUT)
GPIO.setup(COMPOST_PIN, GPIO.OUT)

# Set up PWM for both servos
pwm_recycling = GPIO.PWM(RECYCLING_PIN, 50)
pwm_compost = GPIO.PWM(COMPOST_PIN, 50)

# Set up dht11 pin
sensor = dht11.DHT11(pin=DHT_PIN)

pwm_recycling.start(0)
pwm_compost.start(0)

# to prevent servo continually polling 
last_movement_time = 0  
delay_for_motor = 10


def temp_humidity():
    result = sensor.read()
    temperature = result.temperature
    humidity = result.humidity
    print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
    if temperature >= 50 and temperature <=60:
        print("Optimal temperature for compostion")
    else:
        print("Temperature needs to be between 50 and 60 degrees for optimal compostion")
                
    if humidity >= 50 and humidity <=60:
        print("Optimal humidity for compostion")
    else:
        print("Humidity needs to be between 50 and 60 percent for optimal compostion")


def open_bin(pwm):
    print("Opening bin") 
    pwm.ChangeDutyCycle(7.5)  
    print("Holding open for 5 seconds...")
    # I might add in functionlity here so that if the IR senor detected something dropping in the bin, it then closes the lid?
    time.sleep(6) 
    print("Closing bin")  
    pwm.ChangeDutyCycle(2.5)  
    time.sleep(1)
    pwm.ChangeDutyCycle(0) 

# Start the model process
process = subprocess.Popen(
    ['edge-impulse-linux-runner'], 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    text=True
)

print("Project starting, detecting for Waste or Compost!")

last_dht_read_time = time.time()
# i want the dht11 fucntion to run every min


try:
    while True:
        line = process.stdout.readline()

        if not line:
            continue 

        print(line.strip())  # gives the live data of whats detected

        match = re.search(r'(\[.*\])', line)
        if match:
            try:
                detections = json.loads(match.group(1))  

                # Checks time
                current_time = time.time()

                for obj in detections:
                    label = obj.get("label")

                    if label in ["Recycling", "Compost"]:
                        if current_time - last_movement_time >= delay_for_motor:
                            if label == "Recycling":
                                print("Recycling detected, opening bin!")
                                open_bin(pwm_recycling)
                            elif label == "Compost":
                                print("Compost detected, opening bin")
                                open_bin(pwm_compost)

                            # Updates time
                            last_movement_time = current_time
                        else:
                            print(f"Detected {label}, but waiting on delay.")

            except json.JSONDecodeError:
                print("Error with json")
                
            # Every min   
            if time.time() - last_dht_read_time >= 60:
                temp_humidity()
                last_dht_read_time = time.time()

#if i want to exit out of the termonal command, press ctrl + c
except KeyboardInterrupt:
    print("\nStopping script...")
    pwm_recycling.stop()
    pwm_compost.stop()
    GPIO.cleanup()
    process.terminate()
