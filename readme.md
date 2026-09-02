# CAN-Sentinel

## Automotive ECU Intrusion Detection System

CAN-Sentinel is a simulated automotive cybersecurity system designed
to demonstrate the detection of anomalous and potentially malicious
traffic on a Controller Area Network (CAN).

The project simulates a vehicle CAN environment containing multiple
Electronic Control Units (ECUs), generates normal vehicle traffic,
introduces malicious CAN traffic through an attacker simulation,
captures and analyzes the traffic, and presents the detection results
through a diagnostic dashboard.

The system combines low-level CAN traffic acquisition, traffic
analysis, machine learning-based anomaly detection, and a graphical
diagnostic interface.

---

# 1. Project Overview

Modern vehicles rely heavily on CAN communication between different
ECUs. Since traditional CAN communication does not inherently provide
strong authentication or encryption, abnormal or malicious messages
can potentially affect vehicle systems.

CAN-Sentinel demonstrates a simplified detection pipeline for such
behavior.

The project is divided into four major components:

1. Virtual CAN Environment
2. CAN Traffic Sniffer
3. Heuristic & Machine Learning Engine
4. Diagnostic Dashboard

The components are developed independently and then integrated into
a single end-to-end system.

---

# 2. Overall System Architecture

The high-level architecture is:

```                    +----------------+
                    |   Normal ECUs  |
                    +-------+--------+
                            |
                            |
                    +-------v--------+
                    |    Attacker    |
                    +-------+--------+
                            |
                            v
                       +---------+
                       |  vcan0  |
                       +----+----+
                            |
                            v
                   +------------------+
                   |   C CAN Sniffer |
                   +--------+---------+
                            |
                            v
                  +--------------------+
                  |  Traffic Features  |
                  |                    |
                  | CAN ID             |
                  | Timestamp          |
                  | Payload            |
                  | Frequency          |
                  | Inter-arrival Time |
                  +---------+----------+
                            |
                            v
                   +------------------+
                   |  Isolation Forest|
                   +--------+---------+
                            |
                 +----------+----------+
                 |                     |
               Normal               Anomaly
                                       |
                                       v
                             +----------------+
                             | PyQt Dashboard |
                             +----------------+