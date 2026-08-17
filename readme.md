# CAN-Sentinel

## Automotive ECU Intrusion Detection System

CAN-Sentinel is a simulated automotive CAN environment for studying normal ECU traffic and malicious CAN-bus activity. The project is organized as four connected modules: a virtual CAN environment, a CAN traffic sniffer, a heuristic / machine learning engine, and a diagnostic dashboard.

## Modules

1. Virtual CAN Environment
2. CAN Traffic Sniffer
3. Heuristic / Machine Learning Engine
4. Diagnostic Dashboard

## Overall Data Flow

```text
Member 1
ECUs + attacker
     |
     v
   vcan0
     |
     v
Member 2
C CAN Sniffer
     |
     v
Structured traffic / features
     |
     v
Member 3
ML / anomaly detection
     |
     v
Member 4
PyQt dashboard
```

During live operation, Member 2 captures and structures CAN traffic. Member 3 performs the normal / anomaly decision using the agreed feature representation. Member 2 does not classify traffic as malicious.

## Directory Overview

- `docs/` contains shared architecture, setup, integration, testing, CAN ID, and data schema documentation.
- `member1_can/` is the primary workspace for the virtual CAN environment, simulated ECUs, normal traffic, attacker simulation, and CAN configuration. Existing Member 1 vCAN setup and Engine ECU work is organized there.
- `member2_sniffer/` is the primary workspace for the C-based CAN traffic sniffer and feature extraction layer.
- `member3_ml/` is the primary workspace for data preprocessing, feature selection, baseline learning, Isolation Forest anomaly detection, and model evaluation.
- `member4_dashboard/` is the primary workspace for the PyQt diagnostic dashboard.
- `integration/` contains material for connecting the modules into the final end-to-end system.
- `tests/` contains shared integration and traffic test material.

## Team Workflow

Each member should work primarily in their assigned module directory and use pull requests to propose changes into `main`. Shared contracts such as CAN identifiers, payload encoding, and data schemas should be documented before modules depend on them.
