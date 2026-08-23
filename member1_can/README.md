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
- `ecu/speed_ecu.py` – Simulates Vehicle Speed CAN messages.
- `ecu/brake_ecu.py` – Simulates Brake Pressure CAN messages.
- `ecu/steering_ecu.py` – Simulates Steering Angle CAN messages.
- `ecu/temperature_ecu.py` – Simulates Engine Temperature CAN messages.
- `can_monitor.py` – Monitors real-time CAN traffic from the virtual CAN bus.
- `can_decoder.py` – Decodes raw CAN frames into readable vehicle parameters.
- `can_logger.py` – Records normal CAN traffic and generates `can_normal_dataset.csv`.
- `training_logger.py` – Creates the labeled training dataset for cybersecurity testing.
- `attackers/attack_ecu.py` – Simulates controlled CAN message injection attacks.
- `anomaly_detector.py` – Detects abnormal CAN traffic and generates security alerts.
- `can_id_specification.md` – Documents CAN IDs and ECU signal mapping.
- 
Future ECU, attacker, script, and configuration work should continue inside this module directory.
