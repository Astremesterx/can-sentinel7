# CAN-Sentinel

## Automotive ECU Intrusion Detection System

CAN-Sentinel is a simulated automotive cybersecurity system designed to demonstrate the detection of anomalous and potentially malicious traffic on a Controller Area Network (CAN).

The project creates a virtual vehicle CAN environment using Linux SocketCAN and `vcan0`. Multiple simulated Electronic Control Units (ECUs) generate normal vehicle traffic, while an attacker simulation introduces abnormal CAN messages.

The generated CAN traffic is captured by a C-based CAN sniffer, processed into traffic and timing features, and analyzed using a machine-learning based anomaly detection engine. Detection results can then be presented through a PyQt-based diagnostic dashboard.

The project demonstrates the following intrusion detection workflow:

```text

ECU Simulation

      ↓

CAN Traffic on vcan0

      ↓

C-Based CAN Sniffer

      ↓

Traffic Features

      ↓

Isolation Forest

      ↓

Intrusion Detection

      ↓

Diagnostic Dashboard

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