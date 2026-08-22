# Steering ECU Message Contract

The Steering ECU simulates the vehicle's steering angle and sends the steering value through the virtual CAN bus.

## CAN Message

| Field | Value |
|---|---|
| CAN ID | `0x104` |
| DLC | `8` bytes |
| Signal | Steering Angle |
| Range | `-450° to +450°` |
| Byte 0 | Steering angle high byte |
| Byte 1 | Steering angle low byte |
| Byte 2–7 | Reserved (`00`) |

## Data Encoding

The steering angle can be negative or positive, so an offset is used before transmitting the value.

The formula is:

```
Encoded Value = Steering Angle + 450
```
