# Member 2: CAN Traffic Sniffer

This directory is the primary working area for Member 2.

It will eventually contain the C-based CAN traffic sniffer.

Responsibilities include:

- Capturing CAN frames
- Reading traffic from `vcan0`
- Validating CAN frames
- Parsing CAN frames
- Timestamping traffic
- Recording sequence information
- Counting messages
- Calculating message frequency
- Calculating inter-arrival timing
- Producing other agreed traffic features
- Writing structured output
- Preparing future C-to-Python integration

Implementation files should be placed under `src/`, headers under `include/`, generated output under `output/`, and module tests under `tests/`.

The final ML feature set must be agreed between Member 2 and Member # CAN-Sentinel — CAN Traffic Sniffer

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
