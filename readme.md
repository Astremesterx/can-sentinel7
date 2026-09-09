# CAN-Sentinel

## Automotive ECU Intrusion Detection System

CAN-Sentinel is a simulated automotive cybersecurity system designed to demonstrate the detection of anomalous and potentially malicious traffic on a Controller Area Network (CAN).

The project creates a virtual vehicle CAN environment using Linux SocketCAN and `vcan0`. Multiple simulated Electronic Control Units (ECUs) generate normal vehicle traffic, while an attacker simulation introduces abnormal CAN messages.

The generated CAN traffic is captured by a C-based CAN sniffer, processed into traffic and timing features, and analyzed using a machine-learning based anomaly detection engine. Detection results are presented through a PyQt-based diagnostic dashboard.

The project demonstrates the following intrusion detection workflow:

```text
ECU Simulation
      ?
CAN Traffic on vcan0
      ?
C-Based CAN Sniffer
      ?
Traffic Features
      ?
Isolation Forest
      ?
Intrusion Detection
      ?
Diagnostic Dashboard
```

---

# 1. Project Overview

Modern vehicles rely heavily on CAN communication between different ECUs. Since traditional CAN communication does not inherently provide strong authentication or encryption, abnormal or malicious messages can potentially affect vehicle systems.

CAN-Sentinel demonstrates a complete detection pipeline for such behavior across four integrated components:

1. **Virtual CAN Environment** (`member1_can`): Linux SocketCAN `vcan0` with 5 vehicle ECUs and an injection attacker.
2. **CAN Traffic Sniffer** (`member2_sniffer`): High-speed, low-level C program capturing raw frames and calculating real-time frequency & inter-arrival time.
3. **Heuristic & Machine Learning Engine** (`member3_ml`): Scikit-Learn Isolation Forest model detecting statistical timing anomalies.
4. **Diagnostic Dashboard** (`member4_dashboard`): Native PyQt5 desktop interface dynamically tracking vehicle ECU security health.

---

# 2. Overall System Architecture

```text
       +----------------+
       |   Normal ECUs  |
       +-------+--------+
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
      |  C CAN Sniffer   |
      +--------+---------+
               |
               v
     +--------------------+
     |  Traffic Features  |
     | (ID, Freq, IAT)    |
     +---------+----------+
               |
               v
      +------------------+
      | Isolation Forest |
      +--------+---------+
               |
        +------+------+
        |             |
      Normal       Anomaly
                      |
                      v
            +--------------------+
            |   PyQt Dashboard   |
            +--------------------+
```

---

# 3. How to Replicate and Run the Project

This guide provides step-by-step instructions for anyone looking to test or replicate the CAN-Sentinel pipeline.

## Prerequisites
- Linux Environment (e.g., Kali Linux natively or via WSL)
- Python 3
- GCC (for compiling the C sniffer)

### Step 1: Install Dependencies
Install the required Python libraries for the ML Engine and Dashboard:
```bash
pip3 install scikit-learn pandas joblib python-can PyQt5
```

### Step 2: Compile the C-Sniffer
Compile the low-level SocketCAN sniffer:
```bash
cd member2_sniffer
make
cd ..
```

### Step 3: Start the Virtual Car Network (Terminal 1)
Boot up the `vcan0` interface and start all normal ECUs in the background:
```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
./member1_can/scripts/start_all_ecus.sh
```
*(Leave this terminal running. The virtual car is now generating baseline traffic).*

### Step 4: Train or Evaluate the ML Model (Terminal 2)
*(Note: A pre-trained model is already included in the repository at `member3_ml/models/isolation_forest.pkl`. If you wish to skip training and use the pre-trained brain, you can skip directly to Step 5!)*

If you wish to re-train the model from scratch, capture 10 seconds of baseline traffic using the sniffer and train the Isolation Forest:
```bash
# 1. Capture data (Wait 10 seconds, then press Ctrl+C)
./member2_sniffer/output/sniffer > member3_ml/data/can_normal_dataset.csv

# 2. Train the AI on the captured baseline
python3 member3_ml/src/ml_engine.py --train member3_ml/data/can_normal_dataset.csv

# 3. Optional: Run an instant ML evaluation report
python3 member3_ml/src/ml_engine.py --eval member3_ml/data/can_normal_dataset.csv
```

### Step 5: Launch the Diagnostic Dashboard (Terminal 2)
Run the ultimate chained pipeline! This pipes the live C-Sniffer into the ML Engine, and routes the AI alerts straight into the PyQt Dashboard:
```bash
./member2_sniffer/output/sniffer | python3 member3_ml/src/ml_engine.py --live | python3 member4_dashboard/src/dashboard.py
```
*(A dark-themed Vehicle Diagnostics GUI will pop open, showing all ECUs as NORMAL).*

### Step 6: Simulate a Cyberattack (Terminal 3)
Inject spoofed, high-frequency malicious packets to trigger an anomaly:
```bash
# Default randomized attack (1 Hz):
python3 member1_can/attacker/attack_ecu.py

# High-frequency targeted DoS flood attack on Brakes (50 Hz):
python3 member1_can/attacker/attack_ecu.py --mode flood --target brake

# Rapid-fire targeted burst on Engine:
python3 member1_can/attacker/attack_ecu.py --mode inject --target engine --rate 25.0 --count 50

# Random ID and payload fuzzing attack:
python3 member1_can/attacker/attack_ecu.py --mode fuzz --rate 10.0
```
*(Watch the PyQt Dashboard instantly highlight the compromised physical component, track the attack frequency, increment threat telemetry counters, and export incident reports!)*

---

# 4. Master Launcher & Automated Testing

### One-Click Master System Launcher
Instead of managing three separate terminals, you can launch the complete ecosystem with a single command:
```bash
./integration/run_system.sh
```
*(Automatically verifies vcan0, checks binaries, starts all ECUs, runs the live pipeline with the PyQt dashboard, and handles graceful teardown on Ctrl+C).*

### Automated Review Demo Mode
For rapid project demonstrations and presentations, run the automated demo:
```bash
./integration/run_system.sh --demo
```
*(Brings up the vehicle and dashboard, automatically injects a targeted flood attack on the Brakes after 4 seconds, and demonstrates real-time detection and self-healing recovery back to normal).*

### Running the Automated Test Suite
To verify system integrity, normal baseline metrics, and attack detection sensitivity:
```bash
bash tests/run_all_tests.sh
```
Or via the master launcher:
```bash
./integration/run_system.sh --test
```
