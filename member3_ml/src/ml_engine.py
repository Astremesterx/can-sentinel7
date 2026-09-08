import sys
import argparse
import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'isolation_forest.pkl')

SYSTEM_MAP = {
    0x101: "Engine",
    0x102: "Speed",
    0x103: "Brakes",
    0x104: "Steering",
    0x105: "Temperature"
}

def train_model(dataset_path):
    print(f"[*] Loading dataset from {dataset_path}...")
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"[-] Error: Could not find dataset at {dataset_path}")
        return

    features = ['can_id', 'frequency', 'inter_arrival_time']
    if not all(feature in df.columns for feature in features):
        print("[-] Error: Dataset must contain 'can_id', 'frequency', and 'inter_arrival_time'.")
        return

    df['can_id'] = df['can_id'].astype(str).apply(lambda x: int(x, 16))

    X = df[features].values.astype(np.float64)
    print(f"[*] Training Isolation Forest on {len(X)} samples with features: {features}...")
    
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(X)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"[+] Model successfully trained and saved to {MODEL_PATH}")

def evaluate_model(dataset_path):
    if not os.path.exists(MODEL_PATH):
        print(f"[-] Error: Trained model not found at {MODEL_PATH}. Please run with --train first.")
        return

    print(f"[*] Evaluating model performance against {dataset_path}...")
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"[-] Error: Could not find dataset at {dataset_path}")
        return

    features = ['can_id', 'frequency', 'inter_arrival_time']
    if not all(feature in df.columns for feature in features):
        print("[-] Error: Dataset missing required feature columns.")
        return

    df['can_id'] = df['can_id'].astype(str).apply(lambda x: int(x, 16))
    
    # Filter startup warm-up if message_count exists
    if 'message_count' in df.columns:
        df = df[df['message_count'] >= 5]

    X = df[features].values.astype(np.float64)
    model = joblib.load(MODEL_PATH)
    preds = model.predict(X)
    
    anomalies = (preds == -1).sum()
    total = len(preds)
    anomaly_rate = (anomalies / total * 100.0) if total > 0 else 0.0

    print("=" * 60)
    print(f"       CAN-SENTINEL ML EVALUATION REPORT")
    print("=" * 60)
    print(f" Total evaluated samples : {total}")
    print(f" Normal samples (1)     : {total - anomalies} ({100.0 - anomaly_rate:.2f}%)")
    print(f" Anomalies flagged (-1) : {anomalies} ({anomaly_rate:.2f}%)")
    print("-" * 60)
    print(f"{'Component':<15} {'CAN ID':<10} {'Samples':<10} {'Anomalies':<10}")
    print("-" * 60)

    for cid, name in SYSTEM_MAP.items():
        cid_mask = (df['can_id'].values == cid)
        sub_total = cid_mask.sum()
        if sub_total > 0:
            sub_anom = (preds[cid_mask] == -1).sum()
            print(f"{name:<15} 0x{cid:03X}     {sub_total:<10} {sub_anom:<10}")

    print("=" * 60)

def run_live():
    if not os.path.exists(MODEL_PATH):
        print(f"[-] Error: Trained model not found at {MODEL_PATH}. Please run with --train first.")
        return

    model = joblib.load(MODEL_PATH)
    
    FREQ_IDX = 6
    IAT_IDX = 7
    ID_IDX = 2
    COUNT_IDX = 5  # message_count column

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line or line.startswith("timestamp"):
                continue

            parts = line.split(',')
            if len(parts) < 8:
                continue

            try:
                can_id_hex = parts[ID_IDX]
                can_id_int = int(can_id_hex, 16)
                freq = float(parts[FREQ_IDX])
                iat = float(parts[IAT_IDX])
                msg_count = int(parts[COUNT_IDX])
            except ValueError:
                continue

            # WARM-UP FILTER: Ignore the first 5 messages of any ECU to prevent startup noise false alarms
            if msg_count < 5:
                continue
                
            if freq == 0.0:
                continue

            sample = np.array([[can_id_int, freq, iat]], dtype=np.float64)
            prediction = model.predict(sample)[0]
            
            if prediction == -1:
                component = SYSTEM_MAP.get(can_id_int, "Unknown")
                alert = {
                    "alert_type": "INTRUSION_DETECTED",
                    "timestamp": parts[0],
                    "can_id": can_id_hex,
                    "component": component,
                    "frequency": round(freq, 2),
                    "status": "ANOMALY",
                    "message": f"CRITICAL: Anomaly detected on {component} (ID: {can_id_hex})!"
                }
                print(json.dumps(alert))
                sys.stdout.flush()

    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=str, help="Train Isolation Forest model on CSV dataset")
    parser.add_argument("--eval", type=str, help="Evaluate model performance against CSV dataset")
    parser.add_argument("--live", action="store_true", help="Run live inference streaming from stdin")
    args = parser.parse_args()

    if args.train:
        train_model(args.train)
    elif args.eval:
        evaluate_model(args.eval)
    elif args.live:
        run_live()
