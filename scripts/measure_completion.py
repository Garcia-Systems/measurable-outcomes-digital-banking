#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_fcu.member_experience import load_events, summarize_experience
m=summarize_experience(load_events(ROOT/'data/synthetic/part2/application_before.csv'))
print("Harbor FCU Digital Application Completion (synthetic)")
print(f"Sessions: {m.sessions}\nTask starts: {m.starts}\nTask completions: {m.completions}")
print(f"Completion rate: {m.completion_rate_pct:.1f}%\nIncomplete sessions: {m.incomplete_sessions}")
print("Traffic and clicks are activity; submission is the defined task completion.")
