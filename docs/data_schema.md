# Data Schema

This document defines the data exchanged between CAN-Sentinel modules.

## Member 1 -> Member 2

Raw CAN frame data captured from the virtual CAN environment (vcan0).
This data flows over the Linux SocketCAN interface and is read by the Member 2 Sniffer.

- timestamp: System time when the frame is captured.
- can_id: 11-bit standard CAN identifier.
- dlc: Data Length Code (0-8 bytes).
- data: Up to 8 bytes of payload.

## Member 2 -> Member 3 (Finalized)

Structured traffic records and extracted features produced by the C-based CAN sniffer.
The Sniffer outputs this data in CSV format to stdout for the ML Engine to consume.

**Format:** CSV
**Header Row:** timestamp,sequence_num,can_id,dlc,payload,message_count,frequency,inter_arrival_time

**Fields:**
- timestamp (float): Unix timestamp in seconds (with microsecond precision).
- sequence_num (int): Global sequence number of the captured message.
- can_id (hex): The CAN ID in hexadecimal (e.g., 101).
- dlc (int): Data Length Code.
- payload (hex): The data payload in hexadecimal string format.
- message_count (int): Cumulative number of messages seen for this specific can_id.
- frequency (float): Current estimated frequency (messages per second) for this can_id.
- inter_arrival_time (float): Time elapsed (in seconds) since the last message of this can_id.

## Member 3 -> Member 4

Detection results produced by the ML engine for dashboard display.

Possible fields:
- timestamp
- can_id
- status (Normal/Anomaly)
- anomaly_score
- threat_level
- affected_system
- message
