# Configure Virtual CAN Interface (vcan0)

## Objective

Create a virtual CAN network using Linux SocketCAN for CAN-Sentinel.

## Commands

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
ip link show vcan0
```

## Explanation

- `modprobe vcan` loads the virtual CAN driver.
- `ip link add` creates the `vcan0` interface.
- `ip link set up` activates the interface.
- `ip link show` verifies that `vcan0` is running.

## Result

The virtual CAN interface (`vcan0`) was successfully created and is ready for CAN frame transmission and reception.
