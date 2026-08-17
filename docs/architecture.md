# Architecture

This document will contain the detailed CAN-Sentinel system architecture and data flow.

The expected high-level flow is:

```text
Simulated ECUs + Attacker
          |
          v
        vcan0
          |
          v
 C CAN Traffic Sniffer
          |
          v
Traffic Processing / Feature Extraction
          |
          v
   Python ML Engine
          |
          v
  Anomaly Detection
          |
          v
   PyQt Dashboard
```

Detailed module boundaries, runtime processes, and integration decisions will be documented here as the project develops.
