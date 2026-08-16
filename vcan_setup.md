# Configure Virtual CAN Interface (vcan0)

## Objective

Create a virtual CAN network using Linux SocketCAN for CAN-Sentinel.

## Commands

sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
ip link show vcan0

## Explanation

- `modprobe vcan` — Loads the virtual CAN driver.
- `ip link add` — Creates the `vcan0` interface.
- `ip link set up` — Activates the interface.
- `ip link show` — Verifies that `vcan0` is running.

## Result
The virtual CAN interface (`vcan0`) was successfully created and is ready for CAN frame transmission and reception.
