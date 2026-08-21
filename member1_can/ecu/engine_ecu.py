import can
import time
import random

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

def main():
    while True:
        rpm = random.randint(800, 4000)

        high = (rpm >> 8) & 0xFF
        low = rpm & 0xFF

        data = bytes([high, low] + [0] * 6)

        msg = can.Message(arbitration_id=0x101, data=data, is_extended_id=False)
        try:
            bus.send(msg)
            print(f"Engine ECU → RPM {rpm}")
        except can.CanError:
            print("Failed to send CAN message")

        time.sleep(1)


if __name__ == "__main__":
    main()
