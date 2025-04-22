import RPi.GPIO as GPIO
import time
import dht11
from tinyDB import TinyDB

db = TinyDB('/home/ciara/Documents/FinalYrPro/db.json')
db.truncate()

RECYCLING_PIN = 24
COMPOST_PIN = 16
DHT_PIN = 26
IR_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(RECYCLING_PIN, GPIO.OUT)
GPIO.setup(COMPOST_PIN, GPIO.OUT)
GPIO.setup(IR_PIN, GPIO.IN)

# Set up PWM for both servos
pwm_recycling = GPIO.PWM(RECYCLING_PIN, 50)
pwm_compost = GPIO.PWM(COMPOST_PIN, 50)
sensor = dht11.DHT11(pin=DHT_PIN)

pwm_recycling.start(0)
pwm_compost.start(0)




def temp_humidity():
    result = sensor.read()
    temperature = result.temperature
    humidity = result.humidity
    print(f"Temperature: {temperature}°C, Humidity: {humidity}%")

    db.insert({
        "type": "Temperature and Humidity",
        "temperature": temperature,
        "humidity": humidity,
        "action": f"Temperature: {temperature}°C, Humidity: {humidity}%",
        "timestamp": time.time()
    })


def is_bin_full():
    ir_value = GPIO.input(IR_PIN)
    return ir_value == GPIO.LOW


def open_bin(pwm):
    if is_bin_full():
        print('Bin is full')
        db.insert({
            "type": "Detection",
            "action": "Bin is full",
            "timestamp": time.time()
        })
        return
    time.sleep(0.1) 
    print("Opening bin") 
    pwm.ChangeDutyCycle(5.0)
    time.sleep(3) 
    print("Holding bin")
    
    print("Closing bin")  
    pwm.ChangeDutyCycle(7.5)  
    time.sleep(3)
    pwm.ChangeDutyCycle(0)  


