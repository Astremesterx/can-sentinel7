import can
import time
import random

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

def main():
    while True:
        temperature = random.randint(70, 120)
        data = bytes([temperature] + [0] * 7)

        msg = can.Message(arbitration_id=0x105, data=data, is_extended_id=False)
        try:
            bus.send(msg)
            print(f"Temperature ECU → {temperature} °C")
        except can.CanError:
            print("Failed to send CAN message")

        time.sleep(1)


if __name__ == "__main__":
    main()
