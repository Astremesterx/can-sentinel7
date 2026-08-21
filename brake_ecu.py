import os
import time
import random

while True:
    brake = random.randint(0, 100)

    data = f"{brake:02X}00000000000000"

    os.system(f"cansend vcan0 103#{data}")
    print(f"Brake ECU → {brake}%")

    time.sleep(1)
