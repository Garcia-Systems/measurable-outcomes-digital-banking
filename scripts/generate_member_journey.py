#!/usr/bin/env python3
"""Regenerate deterministic, fictional Harbor FCU journey observations."""
import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/synthetic/part2"
STAGES = ["session_started", "application_viewed", "application_started",
          "personal_info_completed", "verification_started", "verification_completed",
          "review_viewed", "application_submitted", "confirmation_viewed"]
STEPS = ["session", "view", "start", "personal_info", "verification", "verification",
         "review", "submit", "confirmation"]

def generate(path, after=False):
    rows=[]
    base=datetime(2026,1,12 if not after else 19,tzinfo=timezone.utc)
    completed=44 if after else 38
    reached=[60,58,55,51,49,46 if after else 43,45 if after else 41,completed,completed]
    for i in range(60):
        now=base+timedelta(minutes=i*20)
        for index,(event,step) in enumerate(zip(STAGES,STEPS)):
            if i >= reached[index]: break
            duration=0 if index==0 else 8000 + ((i*17+index*13)%24)*1000
            if step=="verification":
                duration += (60000 if after else 150000) + (240000 if i%13==0 else 0)
            if step=="personal_info": duration += 90000+(i%5)*15000
            result="error" if event=="verification_started" and i in ({7,22} if after else {7,14,22,35,48}) else "ok"
            now += timedelta(milliseconds=duration)
            rows.append([f"session_{i+1:04d}",event,now.isoformat().replace('+00:00','Z'),step,result,duration])
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as target:
        writer=csv.writer(target); writer.writerow(["session_id","event_type","timestamp","step","result","duration_ms"]); writer.writerows(rows)

if __name__ == '__main__':
    generate(OUT/'application_before.csv'); generate(OUT/'application_after.csv',True)
    print("Generated deterministic Part II observations (no real member data).")
