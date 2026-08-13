#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from harbor_fcu.integration_metrics import eventual_success_rate, experiment, percentile, requests_per_operation, retry_exhaustions, total_operation_latencies
from harbor_fcu.integrations import NorthstarPaySimulator

print("Retry comparison (100 matched synthetic verification operations)")
for name in ("baseline", "after"):
    rows=experiment(name)
    print(f"{name:8} success={eventual_success_rate(rows):.1f}% requests/op={requests_per_operation(rows):.2f} p95={percentile(total_operation_latencies(rows),95)}ms exhausted={retry_exhaustions(rows, 1 if name=='baseline' else 2)}")
pay=NorthstarPaySimulator(); pay.transfer("transfer-100",10000,True); pay.transfer("transfer-100",10000)
print(f"Idempotency demo: two sends, processed transfers={len(pay.processed)}, amount=$100.00")
