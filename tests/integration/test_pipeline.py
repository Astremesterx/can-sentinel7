#!/usr/bin/env python3
"""
Test Suite: End-to-End Pipeline Integration
Verifies the integration contracts between the C-Sniffer, Python ML Engine,
and the PyQt Dashboard.
"""

import os
import sys
import json
import subprocess
import unittest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
ML_ENGINE_SCRIPT = os.path.join(ROOT_DIR, "member3_ml/src/ml_engine.py")
SNIFFER_BIN = os.path.join(ROOT_DIR, "member2_sniffer/output/sniffer")

class TestPipelineIntegration(unittest.TestCase):

    def test_sniffer_binary_exists(self):
        """Verify the compiled C sniffer binary is present."""
        self.assertTrue(os.path.isfile(SNIFFER_BIN), f"Sniffer binary missing at {SNIFFER_BIN}. Run make in member2_sniffer.")

    def test_ml_engine_alert_json_schema(self):
        """Feed synthetic attack CSV line into ml_engine.py and verify valid JSON alert schema."""
        # Warm up with 5 normal messages (count >= 5), then an anomaly
        mock_input = (
            "timestamp,sequence_num,can_id,dlc,payload,message_count,frequency,inter_arrival_time\n"
            "1787691120.0,1,101,8,0102030405060708,5,1.0000,1.000000\n"
            "1787691120.01,2,101,8,0102030405060708,6,80.0000,0.012500\n"
        )

        proc = subprocess.Popen(
            [sys.executable, ML_ENGINE_SCRIPT, "--live"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = proc.communicate(input=mock_input, timeout=5)
        
        # Verify output contains a valid JSON alert
        lines = [line.strip() for line in stdout.splitlines() if line.strip()]
        self.assertGreater(len(lines), 0, f"Expected alert output from ML engine, got none. Stderr: {stderr}")

        alert = json.loads(lines[0])
        expected_keys = ["alert_type", "timestamp", "can_id", "component", "frequency", "status", "message"]
        for key in expected_keys:
            self.assertIn(key, alert, f"Missing key in JSON alert: {key}")

        self.assertEqual(alert["alert_type"], "INTRUSION_DETECTED")
        self.assertEqual(alert["component"], "Engine")
        self.assertEqual(alert["status"], "ANOMALY")

    def test_ml_engine_malformed_input_resilience(self):
        """Ensure ml_engine does not crash when fed corrupted or truncated lines."""
        corrupted_input = (
            "junk line without commas\n"
            ",,,,\n"
            "timestamp,not_a_seq,BAD_ID,not_dlc,payload,not_count,bad_freq,bad_iat\n"
            "\n"
        )

        proc = subprocess.Popen(
            [sys.executable, ML_ENGINE_SCRIPT, "--live"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, _ = proc.communicate(input=corrupted_input, timeout=5)
        # Should gracefully consume and exit without crashing
        self.assertEqual(proc.returncode, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
