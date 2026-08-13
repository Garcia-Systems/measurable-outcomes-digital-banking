#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from harbor_fcu.reliability import incident_logs, reconstruct_timeline

events = reconstruct_timeline(incident_logs(), operation_id="transfer-0017")
print("Harbor FCU correlated operation (synthetic): transfer-0017")
for event in events:
    print(f"{event.timestamp} request={event.request_id} component={event.component:<16} event={event.event:<18} result={event.result}")
print("Metric: incident window error rate elevated. Correlation: one operation across components.")
print("Privacy check: operational identifiers only; no account number, credential, or request body.")
