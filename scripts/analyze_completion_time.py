#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_fcu.member_experience import *
events=load_events(ROOT/'data/synthetic/part2/application_before.csv'); m=summarize_experience(events)
durations=completion_durations(events)
print("Harbor FCU Completion-Time Analysis (synthetic)")
print(f"Median completion: {m.median_completion_ms/60000:.2f} minutes")
print(f"p95 completion: {m.p95_completion_ms/60000:.2f} minutes")
print("\nStage timing (median / p95):")
for step,values in step_durations(events).items(): print(f"{step:16} {median_duration(values)/1000:6.1f}s / {percentile(values,95)/1000:6.1f}s")
cutoff=m.p95_completion_ms
print(f"\nUnusually long sessions (at or above p95): {', '.join(k for k,v in durations.items() if v>=cutoff)}")
print("Timing identifies a friction signal, not its cause. Faster is not automatically better.")
