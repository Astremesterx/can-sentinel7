# Member 2: CAN Traffic Sniffer

# CAN-Sentinel — CAN Traffic Sniffer

## Overview

The CAN Traffic Sniffer is the traffic acquisition and preprocessing
component of CAN-Sentinel.

Its purpose is to capture CAN frames from the Linux SocketCAN virtual
CAN interface (`vcan0`) and convert the raw CAN traffic into structured
information that can be used by the anomaly detection layer.

The sniffer is implemented in C using Linux SocketCAN raw CAN sockets.

```text
                 vcan0
                   |
                   v
          +------------------+
          |   CAN Frames     |
          +--------+---------+
                   |
                   v
          +------------------+
          |   C CAN Sniffer  |
          +--------+---------+
                   |
                   v
          +------------------+
          | Traffic Features |
          +--------+---------+
                   |
                   v
          ML / Detection Engine