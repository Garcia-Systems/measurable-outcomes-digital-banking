#!/usr/bin/env python3
"""Report the predeclared Chapter 29 before/after delivery experiment."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.quality import delivery_experiment

r = delivery_experiment(); before = r["before"]; after = r["after"]
print("Harbor FCU Delivery Improvement Experiment")
print(f"{'':30} {'BEFORE':>8} {'AFTER':>8}")
for label, key in (("Defined checks", "defined_checks"), ("Pre-release defects caught", "caught"),
                   ("Escaped defects", "escaped"), ("Security cases blocked", "security_blocked"),
                   ("Invalid releases blocked", "invalid_blocked"), ("Validation duration (s)", "duration_seconds")):
    print(f"{label:30} {before[key]:8} {after[key]:8}")
print("\nSUCCESS CRITERIA")
for name, passed in r["criteria"].items():
    print(f"{name.replace('_', ' ').title():30} {'PASS' if passed else 'FAIL'}")
print("\nSUPPORTED CONCLUSION")
print("The improved process detected more defined defects and security failures before simulated deployment.")
print("\nPOTENTIAL DOWNSTREAM EFFECT")
print("Earlier detection may reduce production regressions and incident-response workload.")
print("\nNOT ESTABLISHED")
print("Complete system security; zero future defects; member satisfaction; financial savings.")
