#!/bin/bash
# ==============================================================================
# CAN-Sentinel: Complete Automotive Intrusion Detection System
# Master Orchestration & Integration Runner
# ==============================================================================

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

BANNER="
${CYAN}${BOLD}
   ______  ___    _   __         _____            __  _            __
  / ____/ /   |  / | / /        / ___/___  ____  / /_(_)___  ___  / /
 / /     / /| | /  |/ / ______  \__ \/ _ \/ __ \/ __/ / __ \/ _ \/ / 
/ /___  / ___ |/ /|  / /_____/ ___/ /  __/ / / / /_/ / / / /  __/ /  
\____/ /_/  |_/_/ |_/         /____/\___/_/ /_/\__/_/_/ /_/\___/_/   
${NC}${YELLOW}   Automotive ECU Intrusion Detection System — Master Launcher${NC}
"

echo -e "$BANNER"

# ------------------------------------------------------------------------------
# 1. Argument Parsing (Quick tools that don't need vcan0)
# ------------------------------------------------------------------------------
MODE="gui"
if [ "$1" == "--headless" ]; then
    MODE="headless"
elif [ "$1" == "--eval" ]; then
    echo -e "${BLUE}[*] Running ML Model Baseline Evaluation...${NC}"
    DATASET="${2:-member3_ml/data/can_normal_dataset.csv}"
    python3 member3_ml/src/ml_engine.py --eval "$DATASET"
    exit 0
elif [ "$1" == "--test" ]; then
    echo -e "${BLUE}[*] Running CAN-Sentinel Test Suite...${NC}"
    if [ -f "tests/run_all_tests.sh" ]; then
        bash tests/run_all_tests.sh
    else
        echo -e "${YELLOW}[!] Test runner script not found.${NC}"
    fi
    exit 0
fi

# ------------------------------------------------------------------------------
# 2. Pre-Flight Checks
# ------------------------------------------------------------------------------
echo -e "${BLUE}[*] Performing system pre-flight checks...${NC}"

# Check virtual CAN interface
if ! ip link show vcan0 >/dev/null 2>&1; then
    echo -e "${YELLOW}[!] vcan0 interface not detected.${NC}"
    if sudo -n true 2>/dev/null; then
        sudo modprobe vcan || true
        sudo ip link add dev vcan0 type vcan || true
        sudo ip link set vcan0 up || true
    else
        echo -e "${YELLOW}[i] Please initialize vcan0 by running:${NC}"
        echo -e "    sudo modprobe vcan && sudo ip link add dev vcan0 type vcan && sudo ip link set vcan0 up"
        echo -e "${YELLOW}[!] Attempting to proceed (sudo password may be required)...${NC}"
        sudo modprobe vcan || true
        sudo ip link add dev vcan0 type vcan || true
        sudo ip link set vcan0 up || true
    fi
fi

# ------------------------------------------------------------------------------
# 3. Process Management & Cleanup
# ------------------------------------------------------------------------------
PIDS=()

cleanup() {
    echo -e "\n${YELLOW}[*] Shutting down CAN-Sentinel services...${NC}"
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null || true
        fi
    done
    # Kill any dangling ECU background jobs
    pkill -f "member1_can/ecu/" 2>/dev/null || true
    echo -e "${GREEN}[+] All services stopped cleanly. Goodbye.${NC}"
}
trap cleanup EXIT INT TERM

# ------------------------------------------------------------------------------
# 4. Start Normal ECUs
# ------------------------------------------------------------------------------
echo -e "\n${BLUE}[*] Starting 5 vehicle ECUs (Engine, Speed, Brakes, Steering, Temp)...${NC}"
python3 member1_can/ecu/engine_ecu.py &
PIDS+=($!)
python3 member1_can/ecu/speed_ecu.py &
PIDS+=($!)
python3 member1_can/ecu/brake_ecu.py &
PIDS+=($!)
python3 member1_can/ecu/steering_ecu.py &
PIDS+=($!)
python3 member1_can/ecu/temperature_ecu.py &
PIDS+=($!)

sleep 1
echo -e "${GREEN}[+] All 5 vehicle ECUs are broadcasting on vcan0.${NC}"

# ------------------------------------------------------------------------------
# 5. Launch Detection Pipeline
# ------------------------------------------------------------------------------
if [ "$MODE" == "gui" ]; then
    echo -e "\n${CYAN}[*] Launching Live Pipeline (Sniffer -> ML Engine -> PyQt Dashboard)...${NC}"
    echo -e "${YELLOW}[i] To simulate an attack in another terminal, run:${NC}"
    echo -e "    ${BOLD}python3 member1_can/attacker/attack_ecu.py${NC}\n"
    
    "$SNIFFER_BIN" | python3 member3_ml/src/ml_engine.py --live | python3 member4_dashboard/src/dashboard.py
else
    echo -e "\n${CYAN}[*] Running in HEADLESS mode (Sniffer -> ML Engine -> JSON alerts)...${NC}"
    "$SNIFFER_BIN" | python3 member3_ml/src/ml_engine.py --live
fi
