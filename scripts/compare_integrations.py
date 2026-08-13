#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from harbor_fcu.integrations import ClearVerifyAdapter, HeritageCoreAdapter
from harbor_fcu.integration_metrics import success_rate, percentile

print("Normalized REST/SOAP comparison (no network calls)")
for adapter in (ClearVerifyAdapter(), HeritageCoreAdapter()):
    rows=[adapter.call(f"compare-{i}", s) for i,s in enumerate(["success","slow_success","temporary_failure","timeout","invalid_response","permanent_failure"],1)]
    print(f"{adapter.vendor:14} requests={len(rows)} success={success_rate(rows):.1f}% p95={percentile([r.duration_ms for r in rows],95)}ms")
    print("  normalized: " + ", ".join(r.error_category.value for r in rows))
