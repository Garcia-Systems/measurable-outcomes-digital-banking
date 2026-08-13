#!/usr/bin/env python3
"""Chapter 3: evaluate the whole predeclared success contract."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from harbor_fcu.measurement import evaluate_measurement, load_observations, summarize  # noqa: E402
from harbor_fcu.scenarios import FAST_CANDIDATE, SUCCESS_CRITERIA  # noqa: E402
m=summarize(load_observations(FAST_CANDIDATE)); results=evaluate_measurement(m, SUCCESS_CRITERIA)
print("Fast candidate against predeclared criteria")
for r in results: print(f"{r.criterion.metric}: {r.actual:g} {r.criterion.operator} {r.criterion.threshold:g} — {'PASS' if r.passed else 'FAIL'}")
print(f"Overall: {'PASS' if all(r.passed for r in results) else 'FAIL'}")
