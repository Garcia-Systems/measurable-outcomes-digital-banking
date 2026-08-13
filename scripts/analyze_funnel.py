#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_fcu.member_experience import *
events=load_events(ROOT/'data/synthetic/part2/application_before.csv'); counts=funnel_counts(events)
conversion=stage_conversion(counts); abandoned=stage_abandonment(counts)
print("Harbor FCU Digital Application Funnel (synthetic)\n")
first=next(iter(counts.values()))
for stage,count in counts.items():
    bar='█'*round(20*count/first); rate='baseline' if conversion[stage] is None else f"stage {conversion[stage]:5.1f}%"
    print(f"{stage:25} {bar:<20} {count:3} ({100*count/first:5.1f}% overall; {rate})")
stage,dropped,rate=largest_dropoff(counts)
print(f"\nLargest drop-off: before {stage} ({dropped} sessions; {rate:.1f}% abandonment)")
print(f"Overall conversion: {100*counts['application_submitted']/counts['application_viewed']:.1f}%")
print("This locates observed abandonment; it does not establish its cause.")
