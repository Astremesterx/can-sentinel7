# Verify Virtual CAN Interface Using candump

## Objective

Verify that CAN frames can be transmitted and received through the virtual CAN interface (`vcan0`).

## Receiving CAN Frames

```bash
candump vcan0
```

## Sending a Test CAN Frame

```bash
cansend vcan0 101#07D0000000000000
```

## Observed Output

```text
vcan0  101  [8]  07 D0 00 00 00 00 00 00
```

## Result

The virtual CAN interface successfully transmitted and received the Engine ECU CAN frame. This confirms that `vcan0` is functioning correctly for CAN communication.
