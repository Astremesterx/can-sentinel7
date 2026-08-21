
import can

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

print("CAN-Sential Decoder Started...")
print("Waiting for CAN messages...\n")

while True:
    message = bus.recv()

    can_id = message.arbitration_id
    data = message.data

    if can_id == 0x101:
        rpm = (data[0] << 8) | data[1]
        print(f"Engine ECU      → {rpm} RPM")

    elif can_id == 0x102:
        speed = data[0]
        print(f"Speed ECU       → {speed} km/h")

    elif can_id == 0x103:
        brake = data[0]
        print(f"Brake ECU       → {brake}%")

    elif can_id == 0x104:
        encoded = (data[0] << 8) | data[1]
        steering = encoded - 450
        print(f"Steering ECU    → {steering}°")

    elif can_id == 0x105:
        temperature = data[0]
        print(f"Temperature ECU → {temperature}°C")

    else:
        print(f"Unknown CAN ID: {hex(can_id)}")
