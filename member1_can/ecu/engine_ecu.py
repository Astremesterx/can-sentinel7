import os
import time
import random

while True:
    rpm = random.randint(800, 4000)

    high = (rpm >> 8) & 0xFF
    low = rpm & 0xFF

    data = f"{high:02X}{low:02X}000000000000"

    os.system(f"cansend vcan0 101#{data}")
    print(f"Engine ECU → RPM {rpm}")

    time.sleep(1)
