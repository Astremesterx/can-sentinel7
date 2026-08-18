# CAN Message Contract – Engine ECU

### Objective

Define the CAN frame used by the Engine ECU to transmit RPM data.

| Field | Value |
|--------|-------|
| CAN ID | 0x101 |
| DLC | 8 |
| Data | RPM Value |

## Example Frames

| RPM | CAN Frame |
|------|-----------|
| 800 | `101#0320000000000000` |
| 2000 | `101#07D0000000000000` |
| 3000 | `101#0BB8000000000000` |

## Description

- CAN ID `0x101` identifies the Engine ECU.
- DLC `8` indicates an 8-byte payload.
- The first two bytes (`07 D0`) represent the engine RPM.
- Remaining bytes are reserved for future use.


  ## Result

The Engine ECU transmits an 8-byte CAN frame every second with a dynamic RPM value over the virtual CAN bus (`vcan0`).
