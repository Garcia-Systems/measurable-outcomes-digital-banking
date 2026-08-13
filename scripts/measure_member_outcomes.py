#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.outcomes import outcome_dataset

d = outcome_dataset()
print("CONTROLLED CROSS-LAYER HARBOR EXPERIMENT (SYNTHETIC)")
for layer, keys in (("TECHNICAL", ("integration_success_pct", "error_rate_pct", "p95_api_latency_ms")),
                    ("MEMBER BEHAVIOR", ("completion_pct", "abandonment_pct", "p95_completion_min"))):
    print(f"\n{layer}")
    for key in keys: print(f"{key:28} {d['baseline'][key]:6.1f} -> {d['after'][key]:6.1f}")
print("\nSUPPORTED: the implementation reduced technical failures and increased workflow completion under laboratory conditions.")
print("NOT ESTABLISHED: member satisfaction.")
