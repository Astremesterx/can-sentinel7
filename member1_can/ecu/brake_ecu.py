import can
import time
import random

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

def main():
    while True:
        brake = random.randint(0, 100)
        data = bytes([brake] + [0] * 7)

        msg = can.Message(arbitration_id=0x103, data=data, is_extended_id=False)
        try:
            bus.send(msg)
            print(f"Brake ECU → {brake}%")
        except can.CanError:
            print("Failed to send CAN message")

        time.sleep(1)


if __name__ == "__main__":
    main()
