import sys
import argparse
import json
import os
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
import warnings

# Suppress sklearn warnings about feature names when predicting single rows
warnings.filterwarnings("ignore", category=UserWarning)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'isolation_forest.pkl')

def train_model(dataset_path):
    print(f"[*] Loading dataset from {dataset_path}...")
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"[-] Error: Could not find dataset at {dataset_path}")
        return

    features = ['frequency', 'inter_arrival_time']
    if not all(feature in df.columns for feature in features):
        print("[-] Error: Dataset must contain 'frequency' and 'inter_arrival_time' columns.")
        return

    X = df[features]
    print(f"[*] Training Isolation Forest on {len(X)} samples...")
    
    # Contamination represents the expected proportion of outliers.
    # Set to a very small value assuming normal training data is mostly clean.
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(X)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"[+] Model successfully trained and saved to {MODEL_PATH}")

def run_live():
    if not os.path.exists(MODEL_PATH):
        print(f"[-] Error: Trained model not found at {MODEL_PATH}. Please run with --train first.")
        return

    print("[*] Loading trained Isolation Forest model...")
    model = joblib.load(MODEL_PATH)
    print("[+] Model loaded. Listening on stdin for live C-Sniffer data...")

    # Expected CSV format from the C Sniffer:
    # timestamp,sequence_num,can_id,dlc,payload,message_count,frequency,inter_arrival_time
    FREQ_IDX = 6
    IAT_IDX = 7
    ID_IDX = 2

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line or line.startswith("timestamp"):
                continue  # Skip header or empty lines

            parts = line.split(',')
            if len(parts) < 8:
                continue

            can_id = parts[ID_IDX]
            try:
                freq = float(parts[FREQ_IDX])
                iat = float(parts[IAT_IDX])
            except ValueError:
                continue

            # Skip prediction if frequency is 0 (first message ever seen for this ID)
            if freq == 0.0:
                continue

            # Predict (1 = normal, -1 = anomaly)
            prediction = model.predict([[freq, iat]])[0]
            
            if prediction == -1:
                alert = {
                    "alert_type": "INTRUSION_DETECTED",
                    "timestamp": parts[0],
                    "can_id": can_id,
                    "frequency": freq,
                    "inter_arrival_time": iat,
                    "status": "ANOMALY",
                    "message": f"Suspicious traffic frequency spike detected on CAN ID {can_id}!"
                }
                print(json.dumps(alert))
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n[*] Shutting down ML Engine.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CAN-Sentinel ML Engine")
    parser.add_argument("--train", type=str, help="Path to CSV dataset for training")
    parser.add_argument("--live", action="store_true", help="Run live anomaly detection reading from stdin")
    
    args = parser.parse_args()

    if args.train:
        train_model(args.train)
    elif args.live:
        run_live()
    else:
        parser.print_help()
