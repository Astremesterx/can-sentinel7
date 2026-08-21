import can
import time
import random

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

def main():
    while True:
        steering = random.randint(-450, 450)
        encoded = steering + 450

        high = (encoded >> 8) & 0xFF
        low = encoded & 0xFF

        data = bytes([high, low] + [0] * 6)

        msg = can.Message(arbitration_id=0x104, data=data, is_extended_id=False)
        try:
            bus.send(msg)
            print(f"Steering ECU → {steering}°")
        except can.CanError:
            print("Failed to send CAN message")

        time.sleep(1)


if __name__ == "__main__":
    main()
