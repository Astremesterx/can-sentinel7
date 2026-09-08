#!/usr/bin/env python3
"""
Test Suite: Normal CAN Traffic Validation
Verifies that normal vehicle telemetry adheres to expected frequency,
inter-arrival time, and message contract constraints.
"""

import os
import sys
import unittest
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATASET_PATH = os.path.join(ROOT_DIR, "member3_ml/data/can_normal_dataset.csv")

EXPECTED_ECUS = {
    0x101: "Engine",
    0x102: "Speed",
    0x103: "Brakes",
    0x104: "Steering",
    0x105: "Temperature"
}

class TestNormalTraffic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(DATASET_PATH):
            raise unittest.SkipTest(f"Dataset not found at {DATASET_PATH}")
        cls.df = pd.read_csv(DATASET_PATH)
        cls.df['can_id_int'] = cls.df['can_id'].astype(str).apply(lambda x: int(x, 16))

    def test_schema_columns(self):
        """Verify all mandatory columns exist in captured baseline dataset."""
        required = ['timestamp', 'sequence_num', 'can_id', 'dlc', 'payload', 'message_count', 'frequency', 'inter_arrival_time']
        for col in required:
            self.assertIn(col, self.df.columns, f"Missing required column: {col}")

    def test_ecu_representation(self):
        """Verify all 5 vehicle ECUs are present in the normal baseline dataset."""
        present_ids = set(self.df['can_id_int'].unique())
        for ecu_id, name in EXPECTED_ECUS.items():
            self.assertIn(ecu_id, present_ids, f"ECU {name} (0x{ecu_id:03X}) missing from baseline dataset.")

    def test_steady_state_frequency(self):
        """Verify normal traffic frequency stabilizes around the 1.0 Hz design target."""
        stable = self.df[self.df['message_count'] >= 5]
        mean_freq = stable['frequency'].mean()
        self.assertGreater(mean_freq, 0.5, f"Mean frequency too low: {mean_freq} Hz")
        self.assertLess(mean_freq, 2.0, f"Mean frequency too high for normal traffic: {mean_freq} Hz")

    def test_inter_arrival_times(self):
        """Verify steady state inter-arrival times are ~1.0 second."""
        stable = self.df[self.df['message_count'] >= 5]
        mean_iat = stable['inter_arrival_time'].mean()
        self.assertAlmostEqual(mean_iat, 1.0, delta=0.25, msg=f"Mean IAT diverged from 1.0s: {mean_iat:.3f}s")

if __name__ == "__main__":
    unittest.main(verbosity=2)
