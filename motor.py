import subprocess
import RPi.GPIO as GPIO
import time
import re
import json

RECYCLING_PIN = 23
COMPOST_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(RECYCLING_PIN, GPIO.OUT)
GPIO.setup(COMPOST_PIN, GPIO.OUT)

# Set up PWM for both servos
pwm_recycling = GPIO.PWM(RECYCLING_PIN, 50)
pwm_compost = GPIO.PWM(COMPOST_PIN, 50)

pwm_recycling.start(0)
pwm_compost.start(0)

# Track when the servo was last activated
last_movement_time = 0  
DELAY_BETWEEN_MOVEMENTS = 10  # 10 seconds

def move_servo(pwm):
    """Moves the servo to the open position, waits, then returns to closed."""
    print("Opening bin") 
    pwm.ChangeDutyCycle(7.5)  # Move to open position
    time.sleep(1)

    print("Holding open for 5 seconds...")
    time.sleep(5)  # Hold open for 5 seconds

    print("Closing bin")  
    pwm.ChangeDutyCycle(2.5)  # Move back to closed position
    time.sleep(1)

    pwm.ChangeDutyCycle(0)  # Stop signal to prevent jitter

# Start the model process
process = subprocess.Popen(
    ['edge-impulse-linux-runner'], 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    text=True
)

print("Model running...")

try:
    while True:
        line = process.stdout.readline()

        if not line:
            continue 

        print(line.strip())  # Live output

        match = re.search(r'(\[.*\])', line)
        if match:
            try:
                detections = json.loads(match.group(1))  

                # Check the time since the last movement
                current_time = time.time()

                for obj in detections:
                    label = obj.get("label")

                    if label in ["Recycling", "Compost"]:
                        if current_time - last_movement_time >= DELAY_BETWEEN_MOVEMENTS:
                            if label == "Recycling":
                                print("Recycling detected, moving servo.")
                                move_servo(pwm_recycling)
                            elif label == "Compost":
                                print("Compost detected, moving servo.")
                                move_servo(pwm_compost)

                            # Update last movement time
                            last_movement_time = current_time
                        else:
                            print(f"Detected {label}, but waiting for cooldown period to end.")

            except json.JSONDecodeError:
                print("Error decoding JSON")

except KeyboardInterrupt:
    print("\nStopping script...")
    pwm_recycling.stop()
    pwm_compost.stop()
    GPIO.cleanup()
    process.terminate()
