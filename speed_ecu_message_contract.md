# Speed ECU Message Contract

The Speed ECU simulates the vehicle's current speed and sends the speed value through the virtual CAN bus.

## CAN Message

| Field | Value |
|---|---|
| CAN ID | `0x102` |
| DLC | `8` bytes |
| Signal | Vehicle Speed |
| Range | `0–120 km/h` |
| Byte 0 | Vehicle Speed |
| Byte 1–7 | Reserved (`00`) |

## Data Encoding

The vehicle speed is stored as an 8-bit unsigned integer.

- Byte 0 contains the vehicle speed.
- Byte 1–7 are currently unused and set to `00`.

## Example

For a vehicle speed of `60 km/h`:

```text
Decimal: 60
Hexadecimal: 3C
