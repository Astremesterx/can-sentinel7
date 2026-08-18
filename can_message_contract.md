# CAN Message Contract – Engine ECU

## Objective

Define the CAN frame structure used by the Engine ECU.

| Field | Value |
|--------|-------|
| CAN ID | 0x101 |
| DLC | 8 |
| Data | 07 D0 00 00 00 00 00 00 |

## Description

- CAN ID `0x101` identifies the Engine ECU.
- DLC `8` indicates an 8-byte payload.
- The first two bytes (`07 D0`) represent the engine RPM.
- Remaining bytes are reserved for future use.
