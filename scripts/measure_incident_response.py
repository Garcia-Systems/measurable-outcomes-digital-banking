#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from harbor_fcu.reliability import detection_duration, mttd, mttr, recovery_duration, response_incidents

rows = response_incidents()
print("Harbor FCU incident response (synthetic)")
print("Definitions: MTTD=start→detection; MTTR=start→service restoration.")
for row in rows:
    print(f"{row.incident_id}: detection={detection_duration(row):.0f} min recovery={recovery_duration(row):.0f} min category={row.failure_category}")
print(f"MTTD: {mttd(rows):.1f} min")
print(f"MTTR: {mttr(rows):.1f} min")
print("Review each incident too: an average can hide a severe tail.")
