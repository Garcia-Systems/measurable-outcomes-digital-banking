#!/usr/bin/env python3
"""Chapter 31 deterministic anomaly laboratory."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.intelligence import anomaly_scenario, confusion_matrix, detect_anomalies

values, truth = anomaly_scenario(); predicted = detect_anomalies(values, 10, 3.0); matrix = confusion_matrix(truth, predicted)
print("Harbor FCU Failed Verification Anomaly Detector")
print("Known incident windows:", [i for i, value in enumerate(truth) if value])
print("Detected windows:      ", [i for i, value in enumerate(predicted) if value])
print(f"TP={matrix.true_positive} FP={matrix.false_positive} TN={matrix.true_negative} FN={matrix.false_negative}")
print(f"Precision={matrix.precision:.1%} Recall={matrix.recall:.1%}")
