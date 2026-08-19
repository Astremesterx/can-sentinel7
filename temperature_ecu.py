import os
import time
import random

while True:
    temperature = random.randint(70, 120)

    data = f"{temperature:02X}00000000000000"

    os.system(f"cansend vcan0 105#{data}")
    print(f"Temperature ECU → {temperature} °C")

    time.sleep(1)
