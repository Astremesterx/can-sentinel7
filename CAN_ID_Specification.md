# CAN ID Specification

This document defines the CAN IDs assigned to each ECU in the CAN-Sential project.

The CAN IDs are used to identify which ECU sent a CAN message on the virtual CAN bus.

## ECU CAN ID Assignment

| CAN ID | ECU | Message | Description |
|--------|-----|---------|-------------|
| `0x101` | Engine ECU | Engine RPM | Represents engine rotational speed |
| `0x102` | Speed ECU | Vehicle Speed | Represents vehicle speed |
| `0x103` | Steering ECU | Steering Angle | Represents steering wheel angle |
| `0x104` | Brake ECU | Brake Pressure | Represents brake pedal/braking pressure |
| `0x105` | Temperature ECU | Engine Temperature | Represents engine coolant/engine temperature |
