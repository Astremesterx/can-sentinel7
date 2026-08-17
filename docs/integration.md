# Integration

This document will contain instructions for integrating the four CAN-Sentinel modules.

The final system is expected to connect the C traffic acquisition layer to the Python ML layer, then send detection results to the PyQt dashboard.

Expected flow:

```text
Member 1 -> vcan0 -> Member 2 -> structured features -> Member 3 -> detection result -> Member 4
```

The exact communication format and runtime process will be documented as the team agrees on module interfaces.
