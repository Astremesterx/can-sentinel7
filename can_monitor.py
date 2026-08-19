import can

bus = can.interface.Bus(channel="vcan0", interface="socketcan")

print("CAN-Sential Monitor Started...")
print("Listening on vcan0...\n")

while True:
    message = bus.recv()

    can_id = hex(message.arbitration_id)
    data = message.data.hex().upper()

    print(f"CAN ID: {can_id} | Data: {data}")
