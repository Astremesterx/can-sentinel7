# Member 1: Virtual CAN Environment

This directory is the primary working area for Member 1.

It will eventually contain:

- Virtual CAN setup
- Simulated ECUs
- Normal CAN traffic
- Attacker simulation
- Malicious CAN traffic
- CAN-ID and payload configuration
- Startup scripts

Implementation files should be placed under `ecu/`, `attacker/`, `scripts/`, and `config/` as appropriate.

This module sends traffic to `vcan0`, which is consumed by the Member 2 CAN sniffer.

## Existing Member 1 Work

The current Member 1 work from `main` is organized as:

- `ecu/engine_ecu.py` sends an Engine ECU CAN frame on `vcan0`.
- `vcan_setup.md` documents virtual CAN interface setup.
- `vcan_verification.md` documents `candump` / `cansend` verification.

Future ECU, attacker, script, and configuration work should continue inside this module directory.
