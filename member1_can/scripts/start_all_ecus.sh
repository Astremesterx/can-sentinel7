#!/bin/bash
echo "[*] Starting all normal ECUs in the background..."
python3 member1_can/ecu/engine_ecu.py &
P1=$!
python3 member1_can/ecu/speed_ecu.py &
P2=$!
python3 member1_can/ecu/brake_ecu.py &
P3=$!
python3 member1_can/ecu/steering_ecu.py &
P4=$!
python3 member1_can/ecu/temperature_ecu.py &
P5=$!

function cleanup {
  echo ""
  echo "[-] Stopping ECUs..."
  kill $P1 $P2 $P3 $P4 $P5
  exit 0
}

trap cleanup EXIT INT TERM

echo "[+] All ECUs running. Press Ctrl+C to stop."
wait
