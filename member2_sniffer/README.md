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

The final ML feature set must be agreed between Member 2 and Member 3.
