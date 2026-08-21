import os
import time
import random

while True:
    steering = random.randint(-450, 450)

    encoded = steering + 450

    high = (encoded >> 8) & 0xFF
    low = encoded & 0xFF

    data = f"{high:02X}{low:02X}000000000000"

    os.system(f"cansend vcan0 104#{data}")
    print(f"Steering ECU → {steering}°")

    time.sleep(1)
