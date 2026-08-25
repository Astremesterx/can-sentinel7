import sys
import argparse
import json
import os
import joblib
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

    # Convert hexadecimal can_id strings to integers for the ML model
    df['can_id'] = df['can_id'].apply(lambda x: int(str(x), 16) if isinstance(x, str) else x)

    X = df[features]
    print(f"[*] Training Isolation Forest on {len(X)} samples with features: {features}...")
    
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(X)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"[+] Model successfully trained and saved to {MODEL_PATH}")

def run_live():
    if not os.path.exists(MODEL_PATH):
        print(f"[-] Error: Trained model not found at {MODEL_PATH}. Please run with --train first.")
        return

    model = joblib.load(MODEL_PATH)
    
    # Indices based on C-Sniffer CSV output
    FREQ_IDX = 6
    IAT_IDX = 7
    ID_IDX = 2

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
            except ValueError:
                continue

            if freq == 0.0:
                continue

            # Predict based on CAN ID and timing features
            prediction = model.predict([[can_id_int, freq, iat]])[0]
            
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
    parser.add_argument("--train", type=str)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    if args.train:
        train_model(args.train)
    elif args.live:
        run_live()
