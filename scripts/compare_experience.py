#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_fcu.member_experience import *
before=summarize_experience(load_events(ROOT/'data/synthetic/part2/application_before.csv'))
after=summarize_experience(load_events(ROOT/'data/synthetic/part2/application_after.csv'))
c=compare_experience(before,after)
print("Harbor FCU Controlled Experience Comparison (synthetic)")
print(f"{'Metric':25} {'BEFORE':>10} {'AFTER':>10}")
print(f"{'Completion rate':25} {before.completion_rate_pct:9.1f}% {after.completion_rate_pct:9.1f}%")
print(f"{'Median completion':25} {before.median_completion_ms/60000:9.2f}m {after.median_completion_ms/60000:9.2f}m")
print(f"{'p95 completion':25} {before.p95_completion_ms/60000:9.2f}m {after.p95_completion_ms/60000:9.2f}m")
print(f"{'Error-session rate':25} {before.error_rate_pct:9.1f}% {after.error_rate_pct:9.1f}%")
print(f"\nCompletion change: {c.completion_change_points:+.1f} percentage points\np95 improvement: {c.p95_improvement_pct:.1f}%\nError change: {c.error_change_points:+.1f} percentage points")
for result in evaluate_experience(c): print(f"{result.criterion.metric}: {'PASS' if result.passed else 'FAIL'} ({result.criterion.operator} {result.criterion.threshold:g})")
print("Measured conversion is not automatically revenue or cost savings.")
