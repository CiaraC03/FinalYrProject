# SmartCycle
A computer vision based project which detects Recycling or Compost!

## What does it do?
Hosted on edge impulse, this smart waste system uses computer vision to detect compost or recycling and sorts them into their appropriate class. The bin features two servo motors which physically opens the bin while the addition of an infrared sensor notifies the user if the bin needs emptying. Using a temperature and humidity sensor will help keep the compost conditions optimal.

### Prerequisites
- Raspberry Pi 4
- Camera
- Python 3.11
- Flask (for the web interface)

### Steps
1. Clone the repository:
   ```bash
   https://github.com/CiaraC03/FinalYrProject

2. Connections on Raspberry Pi:
   The servo motors, IR sensor and DHT11 sensor are connected to the Raspberry Pi via GPIO pins, see sensors.py
