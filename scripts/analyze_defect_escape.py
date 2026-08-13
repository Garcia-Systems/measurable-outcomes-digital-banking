#!/usr/bin/env python3
"""Analyze the Chapter 26 fictional release history."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.quality import RELEASE_HISTORY, defect_metrics

result = defect_metrics(RELEASE_HISTORY)
print("Harbor FCU Synthetic Defect History")
for release in RELEASE_HISTORY:
    print(f"Release {release.release_id}: known={release.known}, pre-release={release.detected}, escaped={release.known-release.detected}")
print(f"Known defects          {result['known']}")
print(f"Detection rate         {result['detection_rate']:.1f}%")
print(f"Escape rate            {result['escape_rate']:.1f}%")
counts = result["escaped_by_type"]
most = max(counts, key=counts.get)
print(f"Most frequent escape   {most} ({counts[most]})")
print("Limitation: unknown defects are absent from the denominator.")
