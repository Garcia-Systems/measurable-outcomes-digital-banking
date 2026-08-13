#!/usr/bin/env python3
"""Chapter 0: observe a real metric in the shared synthetic environment."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from harbor_fcu.measurement import load_observations, success_rate  # noqa: E402
from harbor_fcu.scenarios import BASELINE  # noqa: E402
rows = load_observations(BASELINE)
print("Harbor FCU synthetic member-verification observations")
print(f"Completed successfully: {sum(row.successful for row in rows)}/{len(rows)}")
print(f"Verification success rate: {success_rate(rows):.1f}%")
