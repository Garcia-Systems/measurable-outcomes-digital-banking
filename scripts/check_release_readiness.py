#!/usr/bin/env python3
"""Evaluate the local Chapter 28 release criteria."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.quality import CANDIDATES, release_gate

parser = argparse.ArgumentParser()
parser.add_argument("--candidate", choices=sorted(CANDIDATES), default="valid")
args = parser.parse_args()
result = release_gate(CANDIDATES[args.candidate])
print(f"Harbor FCU Release Readiness — {args.candidate}")
labels = {"formatting": "Formatting/static checks", "unit": "Unit tests", "integration": "Integration tests",
          "security": "Security cases", "regression": "Regression suite", "artifacts": "Required artifacts"}
for name, passed in result["checks"].items():
    print(f"{labels[name]:27} {'PASS' if passed else 'FAIL'}")
print("-" * 34)
print(f"DEPLOYMENT READY            {'YES' if result['ready'] else 'NO'}")
# A rejected candidate is an expected measured result, not a broken laboratory command.
