import can

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

print("CAN-Sential Decoder Started...")
print("Waiting for CAN messages...\n")

while True:
    message = bus.recv()
    if message is None:
        continue

    can_id = message.arbitration_id
    data = message.data
    if data is None:
        continue

    try:
        if can_id == 0x101:
            if len(data) >= 2:
                rpm = (data[0] << 8) | data[1]
                print(f"Engine ECU      → {rpm} RPM")
            else:
                print("Engine ECU message too short")

        elif can_id == 0x102:
            if len(data) >= 1:
                speed = data[0]
                print(f"Speed ECU       → {speed} km/h")

        elif can_id == 0x103:
            if len(data) >= 1:
                brake = data[0]
                print(f"Brake ECU       → {brake}%")

        elif can_id == 0x104:
            if len(data) >= 2:
                encoded = (data[0] << 8) | data[1]
                steering = encoded - 450
                print(f"Steering ECU    → {steering}°")

        elif can_id == 0x105:
            if len(data) >= 1:
                temperature = data[0]
                print(f"Temperature ECU → {temperature}°C")

        else:
            print(f"Unknown CAN ID: {hex(can_id)}")
    except Exception as e:
        print("Error decoding message:", e)
