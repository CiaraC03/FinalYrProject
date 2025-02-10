import subprocess
import RPi.GPIO as GPIO
import time
import re
import json


SERVO_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# PWM of 50 and duty of 0
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0) 

def move_servo():
    print("Opening bin") 
    pwm.ChangeDutyCycle(7.5)  
    time.sleep(1)  
    pwm.ChangeDutyCycle(2.5)  
    time.sleep(1)
    pwm.ChangeDutyCycle(0)  

# This is what I run the start to model
process = subprocess.Popen(
    ['edge-impulse-linux-runner'], 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    text=True
)

print("Model running")


try:
    while True:
        line = process.stdout.readline()

        if not line:
            continue 

        print(line.strip()) #Live output which we can see

        # the classes, recycling and compost are cast as labels called Recycling/Compost in json
        match = re.search(r'(\[.*\])', line)
        if match:
            try:
                detections = json.loads(match.group(1))  

                
                for obj in detections:
                    if obj.get("label") == "Recycling":
                        print("♻️ Recycling detected! Moving the servo...")
                        move_servo()  

            except json.JSONDecodeError:
                print("Error")

except KeyboardInterrupt:
    print("\n🛑 Stopping script...")
    pwm.stop()
    GPIO.cleanup()
    process.terminate()
