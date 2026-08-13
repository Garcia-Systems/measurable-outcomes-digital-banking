#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from harbor_fcu.reliability import incident_logs, incident_metrics, reconstruct_timeline

print("Harbor FCU incident inc-017 evidence (synthetic; diagnosis intentionally withheld)")
print("Component                    p50       p95")
for component, (p50, p95) in incident_metrics().items():
    unit = "%" if component == "application-cpu-pct" else "ms"
    print(f"{component:<25} {p50:>5}{unit:<3} {p95:>7}{unit}")
print("\nTimeline")
for event in reconstruct_timeline(incident_logs(), incident_id="inc-017"):
    detail = f" error={event.error_category}" if event.error_category else ""
    print(f"{event.timestamp[11:19]}  {event.component:<18} {event.event}={event.result}{detail}")
print("\nQuestion: Which component is the strongest suspect, and what remains unproven?")
print("Recovery should be confirmed by transfer success/error rate and p95 returning to target.")
