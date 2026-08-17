# Member 3: Heuristic / Machine Learning Engine

This directory is the primary working area for Member 3.

It will eventually contain:

- Data preprocessing
- Feature selection
- ML pipeline
- Baseline learning
- Isolation Forest anomaly detection
- Model evaluation

Member 3 can begin development using sample data from Member 1. The final model should use the final feature representation agreed with and produced by Member 2.

Normal and attack datasets should remain distinguishable during offline experiments:

- `data/normal/`
- `data/attack/`

During live operation:

```text
CAN traffic -> Member 2 features -> Member 3 ML -> NORMAL / ANOMALY
```
