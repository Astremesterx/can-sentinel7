# CAN-Sentinel Automated Test Suite

This directory contains comprehensive end-to-end, validation, and integration tests for the CAN-Sentinel system.

## Test Structure

- **`normal_traffic/test_normal_traffic.py`**:
  - Validates captured baseline dataset schema and structure.
  - Verifies presence and message contracts for all 5 ECUs (Engine, Speed, Brakes, Steering, Temperature).
  - Verifies that normal steady-state broadcast frequencies stabilize around the 1.0 Hz target and inter-arrival times are ~1.0 second.

- **`attack_traffic/test_attack_detection.py`**:
  - Simulates high-frequency Denial-of-Service (DoS) / flooding attacks (50–120 Hz).
  - Simulates microsecond-level rapid packet injection bursts.
  - Verifies that the trained Isolation Forest model achieves 100% anomaly detection on attack bursts while maintaining >98% baseline preservation on normal traffic.

- **`integration/test_pipeline.py`**:
  - Verifies compilation and existence of the C-based SocketCAN sniffer binary.
  - Validates that CSV traffic features piped into `ml_engine.py` produce schema-compliant JSON alert payloads matching the dashboard contract (`alert_type`, `can_id`, `component`, `frequency`, `status`).
  - Tests resilience of the ML engine against malformed, corrupted, or truncated inputs.

## Running All Tests

To execute the entire automated test suite:
```bash
bash tests/run_all_tests.sh
```
Or via the master launcher:
```bash
./integration/run_system.sh --test
```
