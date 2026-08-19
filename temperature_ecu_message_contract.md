# Temperature ECU Message Contract

The Temperature ECU simulates the vehicle's engine temperature and sends the temperature value through the virtual CAN bus.

## CAN Message

| Field | Value |
|---|---|
| CAN ID | `0x105` |
| DLC | `8` bytes |
| Signal | Engine Temperature |
| Range | `70–120 °C` |
| Byte 0 | Engine Temperature |
| Byte 1–7 | Reserved (`00`) |

## Data Encoding

The engine temperature is stored as an 8-bit unsigned integer.

- Byte 0 contains the engine temperature.
- Byte 1–7 are currently unused and set to `00`.

## Example

For an engine temperature of `90°C`:

```text
Decimal: 90
Hexadecimal: 5A
