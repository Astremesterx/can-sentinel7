# Data Schema

This document will define the data exchanged between CAN-Sentinel modules. The final schema should be agreed by the team before module integration.

## Member 1 -> Member 2

Raw CAN frame data from the virtual CAN environment.

Possible fields:

- `timestamp`
- `can_id`
- `dlc`
- `data`

## Member 2 -> Member 3

Structured traffic records and extracted features from the C CAN sniffer.

Possible fields:

- `timestamp`
- `sequence_number`
- `can_id`
- `dlc`
- `data`
- `message_count`
- `frequency`
- `inter_arrival_time`
- other agreed features

The final ML feature set must be agreed between Member 2 and Member 3.

## Member 3 -> Member 4

Detection results produced by the ML engine for dashboard display.

Possible fields:

- `timestamp`
- `can_id`
- `status`
- `anomaly_score`
- `threat_level`
- `affected_system`
- `message`

These fields are placeholders and do not force a final schema.
