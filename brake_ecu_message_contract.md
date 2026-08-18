# Brake ECU Message Contract

The Brake ECU simulates the vehicle's brake pressure and sends the brake value through the virtual CAN bus.

## CAN Message

| Field | Value |
|---|---|
| CAN ID | `0x103` |
| DLC | `8` bytes |
| Signal | Brake Pressure |
| Range | `0–100%` |
| Byte 0 | Brake Pressure |
| Byte 1–7 | Reserved (`00`) |

## Data Encoding

The brake value is stored as an 8-bit unsigned integer.

- Byte 0 contains the brake value.
- Byte 1–7 are currently unused and set to `00`.

## Example

For a brake value of `75%`:

```text
Decimal: 75
Hexadecimal: 4B
