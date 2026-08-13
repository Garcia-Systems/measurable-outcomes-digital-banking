#!/usr/bin/env python3
"""Chapter 34 downstream controlled incident-response simulation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.intelligence import intelligence_experiment

r = intelligence_experiment(); a, b = r["baseline"], r["assisted"]
print("Harbor FCU Intelligent Operations Experiment")
print(f"\nDETECTION\n{'':30} {'BASELINE':>10} {'ASSISTED':>10}")
for label, key, fmt in (("True positives","true_positive",".0f"),("False positives","false_positive",".0f"),("False negatives","false_negative",".0f"),("Precision","precision",".1%"),("Recall","recall",".1%")):
    print(f"{label:30} {format(a[key],fmt):>10} {format(b[key],fmt):>10}")
print("\nENGINEERING WORKFLOW")
for label, key in (("Median investigation time (min)","median_investigation_minutes"),("Alerts investigated","alerts_investigated"),("Critical incidents in first 3","critical_first_three")):
    print(f"{label:35} {a[key]:6.1f} {b[key]:6.1f}")
print("\nOPERATIONAL OUTCOME")
print(f"MTTD (min) {a['mttd_minutes']:.1f} -> {b['mttd_minutes']:.1f}")
print(f"MTTR (min) {a['mttr_minutes']:.1f} -> {b['mttr_minutes']:.1f}")
print("\nSUCCESS CRITERIA")
for name, passed in r["criteria"].items(): print(f"{name.replace('_',' ').title():30} {'PASS' if passed else 'FAIL'}")
print("\nSUPPORTED CONCLUSION\nThe assisted queue changed detection and reduced investigation-start time in this simulation.")
print("\nPOTENTIAL DOWNSTREAM EFFECT\nEarlier investigation may reduce member-facing disruption under similar conditions.")
print("\nNOT ESTABLISHED\nProduction safety, financial savings, member satisfaction, or real-world causal effects.")
