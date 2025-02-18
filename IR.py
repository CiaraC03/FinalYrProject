import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

try:
    while True:
        if GPIO.input(23):  
            print("Bin is empty")
        else:  
            print("Bin is full")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    GPIO.cleanup()
