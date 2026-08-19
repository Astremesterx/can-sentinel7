import can
import csv
from datetime import datetime

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

with open("can_normal_dataset.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "timestamp",
        "can_id",
        "dlc",
        "data",
        "label",
    ])

    print("Recording CAN traffic... Press Ctrl+C to stop.")

    try:
        while True:
            message = bus.recv()
            if message is None:
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            can_id = hex(message.arbitration_id)
            dlc = message.dlc
            data = message.data
            raw = data.hex().upper()

            writer.writerow([timestamp, can_id, dlc, raw, "normal"])
            print(timestamp, can_id, raw)

    except KeyboardInterrupt:
        print("\nDataset saved as can_normal_dataset.csv")
