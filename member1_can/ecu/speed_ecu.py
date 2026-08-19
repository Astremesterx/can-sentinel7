import can
import time
import random

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

def main():
    while True:
        speed = random.randint(0, 120)
        data = bytes([speed] + [0] * 7)

        msg = can.Message(arbitration_id=0x102, data=data, is_extended_id=False)
        try:
            bus.send(msg)
            print(f"Speed ECU → {speed} km/h")
        except can.CanError:
            print("Failed to send CAN message")

        time.sleep(1)


if __name__ == "__main__":
    main()
