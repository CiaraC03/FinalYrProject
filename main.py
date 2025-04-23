import subprocess
import re
import json
import time
import RPi.GPIO as GPIO
import threading
from web import run_flask
from sensors import db, pwm_recycling, pwm_compost, open_bin, temp_humidity


last_movement_motor = 0  
delay_for_motor = 10

flash_thread = threading.Thread(target=run_flask)
flash_thread.start()

process = subprocess.Popen(
    ['edge-impulse-linux-runner'], 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    text=True
)

print("Project starting, detecting for Waste or Compost")

read_dht_time = time.time()

try:
    while True:
        line = process.stdout.readline()

        print(line.strip())  

        match = re.search(r'(\[.*\])', line)
        if match:
            try:
                detections = json.loads(match.group(1))  

                read_motor_time = time.time()

                for obj in detections:
                    label = obj.get("label")

                    if label in ["Recycling", "Compost"]:
                        
                        if read_motor_time - last_movement_motor >= delay_for_motor:
                            if label == "Recycling":
                                print("Recycling detected, opening bin!")
                                db.insert({
                                    "type": "Recycling", 
                                    "action": "Opened bin",
                                    "time": time.time()
                                })
                                open_bin(pwm_recycling)
                            elif label == "Compost":
                                print("Compost detected, opening bin")
                                db.insert({
                                    "type": "Compost", 
                                    "action": "Opened bin",
                                    "time": time.time()
                                })
                                open_bin(pwm_compost)
                                
                            last_movement_motor = read_motor_time
                        else:
                            print(f"Detected {label}, but waiting on delay.")

            except json.JSONDecodeError:
                print("JSON Error")
                
            
            if time.time() - read_dht_time >= 60:
                temp_humidity()
                read_dht_time = time.time()

#if i want to exit out of the termonal command, press ctrl + c
except KeyboardInterrupt:
    print("\nStopping script...")
    pwm_recycling.stop()
    pwm_compost.stop()
    GPIO.cleanup()
    process.terminate()