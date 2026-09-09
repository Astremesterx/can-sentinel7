#!/usr/bin/env python3
"""
Test Suite: Cyberattack Detection Validation
Simulates various attack patterns (flooding, high-frequency bursts,
and rogue injection) against the trained Isolation Forest ML model
to verify that anomalous frames are flagged with high sensitivity.
"""

import os
import sys
import unittest
import joblib
import numpy as np
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
MODEL_PATH = os.path.join(ROOT_DIR, "member3_ml/models/isolation_forest.pkl")
DATASET_PATH = os.path.join(ROOT_DIR, "member3_ml/data/can_normal_dataset.csv")

class TestAttackDetection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(MODEL_PATH):
            raise unittest.SkipTest(f"Trained model not found at {MODEL_PATH}")
        cls.model = joblib.load(MODEL_PATH)

    def test_flood_attack_detection(self):
        """Simulate high-frequency DoS / Flooding attack (e.g. 50-120 Hz, IAT 0.008-0.02s)."""
        attack_samples = np.array([
            [0x101, 50.0, 0.020],   # Engine flooded
            [0x102, 85.0, 0.011],   # Speed flooded
            [0x103, 120.0, 0.008],  # Brakes flooded
            [0x104, 45.0, 0.022],   # Steering flooded
            [0x105, 60.0, 0.016],   # Temp flooded
        ], dtype=np.float64)

        preds = self.model.predict(attack_samples)
        for i, pred in enumerate(preds):
            self.assertEqual(pred, -1, f"Sample {i} (Flood attack) was not flagged as anomaly (-1): got {pred}")

    def test_microsecond_injection_burst(self):
        """Simulate rapid-fire frame injection where IAT drops to near zero."""
        injection_samples = np.array([
            [0x101, 15.0, 0.001],
            [0x103, 20.0, 0.0005],
            [0x104, 18.0, 0.002],
        ], dtype=np.float64)

        preds = self.model.predict(injection_samples)
        for i, pred in enumerate(preds):
            self.assertEqual(pred, -1, f"Injection burst sample {i} was not detected as anomaly: got {pred}")

    def test_normal_baseline_preservation(self):
        """Verify that genuine steady-state normal traffic samples achieve >98% accuracy."""
        if not os.path.exists(DATASET_PATH):
            raise unittest.SkipTest("Baseline dataset not available")
        
        df = pd.read_csv(DATASET_PATH)
        df['can_id_int'] = df['can_id'].astype(str).apply(lambda x: int(x, 16))
        stable = df[df['message_count'] >= 5]
        
        features = stable[['can_id_int', 'frequency', 'inter_arrival_time']].values.astype(np.float64)
        preds = self.model.predict(features)
        
        normal_ratio = (preds == 1).mean()
        self.assertGreater(normal_ratio, 0.98, f"Normal sample preservation below threshold: {normal_ratio:.2%}")

    def test_attacker_payload_contracts(self):
        """Verify the attack simulator generates compliant CAN frame payloads."""
        sys.path.insert(0, os.path.join(ROOT_DIR, "member1_can/attacker"))
        import attack_ecu

        for target in ["engine", "speed", "brake", "steering", "temperature"]:
            payload, desc = attack_ecu.generate_payload(target)
            self.assertEqual(len(payload), 8, f"Payload for {target} must be 8 bytes DLC")
            self.assertIsInstance(payload, bytes, f"Payload for {target} must be bytes")
            self.assertIsInstance(desc, str)

if __name__ == "__main__":
    unittest.main(verbosity=2)
