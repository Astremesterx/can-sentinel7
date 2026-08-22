import can

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

print("CAN-Sential Anomaly Detector Started...")
print("Monitoring CAN traffic...\n")

while True:

    message = bus.recv()

    can_id = message.arbitration_id
    data = message.data

    if can_id == 0x101:
        rpm = (data[0] << 8) | data[1]

        if rpm > 6000:
            print(f"🚨 ALERT: High Engine RPM ({rpm} RPM)")
        else:
            print(f"Engine RPM: {rpm}")

    elif can_id == 0x102:
        speed = data[0]

        if speed > 120:
            print(f"🚨 ALERT: Overspeed ({speed} km/h)")
        else:
            print(f"Speed: {speed} km/h")

    elif can_id == 0x103:
        brake = data[0]

        if brake > 100:
            print(f"🚨 ALERT: Invalid Brake Value ({brake}%)")
        else:
            print(f"Brake: {brake}%")

    elif can_id == 0x104:
        encoded = (data[0] << 8) | data[1]
        steering = encoded - 450

        if steering < -450 or steering > 450:
            print(f"🚨 ALERT: Steering Anomaly ({steering}°)")
        else:
            print(f"Steering: {steering}°")

    elif can_id == 0x105:
        temperature = data[0]

        if temperature > 120:
            print(f"🚨 ALERT: Engine Overheating ({temperature}°C)")
        else:
            print(f"Temperature: {temperature}°C")
