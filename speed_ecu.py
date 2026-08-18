import os
import time
import random

while True:
    speed = random.randint(0, 120)

    data = f"{speed:02X}00000000000000"

    os.system(f"cansend vcan0 102#{data}")
    print(f"Speed ECU → {speed} km/h")

    time.sleep(1)

