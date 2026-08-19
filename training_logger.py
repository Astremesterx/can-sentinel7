import can
import csv
from datetime import datetime

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

with open("can_training_dataset.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "can_id", "dlc", "data", "label"])

    print("Recording training dataset... Press Ctrl+C to stop.")

    try:
        while True:
            msg = bus.recv()
            if msg is None:
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            can_id = msg.arbitration_id
            data = msg.data
            if data is None:
                continue
            raw = data.hex().upper()

            label = "normal"

            if can_id == 0x101 and len(data) >= 2:
                rpm = (data[0] << 8) | data[1]
                if rpm > 6000:
                    label = "anomaly"

            elif can_id == 0x102 and len(data) >= 1:
                speed = data[0]
                if speed > 120:
                    label = "anomaly"

            elif can_id == 0x103 and len(data) >= 1:
                brake = data[0]
                if brake > 100:
                    label = "anomaly"

            elif can_id == 0x104 and len(data) >= 2:
                steering = ((data[0] << 8) | data[1]) - 450
                if steering < -450 or steering > 450:
                    label = "anomaly"

            elif can_id == 0x105 and len(data) >= 1:
                temp = data[0]
                if temp > 120:
                    label = "anomaly"

            writer.writerow([timestamp, hex(can_id), msg.dlc, raw, label])
            print(timestamp, hex(can_id), raw, label)

    except KeyboardInterrupt:
        print("Training dataset saved.")
