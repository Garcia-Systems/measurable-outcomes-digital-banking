#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.outcomes import operational_scorecard

print("HARBOR FCU OPERATIONAL SCORECARD (FICTIONAL / SYNTHETIC)")
print("No composite score: each signal retains its unit and meaning.\n")
for name, (before, after) in operational_scorecard().items():
    print(f"{name:28} {before:7.1f} -> {after:7.1f}")
