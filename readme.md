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

```                    +---

# 3. How to Replicate and Run the Project

This guide provides step-by-step instructions for anyone looking to test or replicate the CAN-Sentinel pipeline.

## Prerequisites
- Linux Environment (e.g., Kali Linux natively or via WSL)
- Python 3
- GCC (for the C sniffer)

### Step 1: Install Dependencies
Install the required Python libraries for the ML Engine and Dashboard:
\ash
pip3 install scikit-learn pandas joblib python-can PyQt5
### Step 2: Compile the C-Sniffer
Compile the low-level SocketCAN sniffer:
\ash
cd member2_sniffer
make
cd ..
### Step 3: Start the Virtual Car Network (Terminal 1)
Boot up the \can0\ interface and start all normal ECUs in the background:
\ash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
./member1_can/scripts/start_all_ecus.sh
\*(Leave this terminal running. The virtual car is now generating baseline traffic).*

### Step 4: Train the ML Model (Terminal 2)
*(Note: A pre-trained model is already included in the repository at \member3_ml/models/isolation_forest.pkl\. If you wish to skip training and use the pre-trained brain, you can skip directly to Step 5!)*

If you wish to re-train the model from scratch, capture 10 seconds of baseline traffic using the sniffer and train the Isolation Forest:
\ash
# 1. Capture data (Wait 10 seconds, then press Ctrl+C)
./member2_sniffer/output/sniffer > member3_ml/data/can_normal_dataset.csv

# 2. Train the AI on the captured baseline
python3 member3_ml/src/ml_engine.py --train member3_ml/data/can_normal_dataset.csv
### Step 5: Launch the Diagnostic Dashboard (Terminal 2)
Run the ultimate chained pipeline! This pipes the live C-Sniffer into the ML Engine, and routes the AI alerts straight into the PyQt Dashboard:
\ash
./member2_sniffer/output/sniffer | python3 member3_ml/src/ml_engine.py --live | python3 member4_dashboard/src/dashboard.py
\*(A dark-themed Vehicle Diagnostics GUI will pop open, showing all ECUs as SECURE).*

### Step 6: Simulate a Cyberattack (Terminal 3)
Inject spoofed, high-frequency malicious packets to trigger an anomaly:
\ash
python3 member1_can/attacker/attack_ecu.py
\*(Watch the PyQt Dashboard instantly highlight the compromised physical component and log the intrusion alerts!)*
