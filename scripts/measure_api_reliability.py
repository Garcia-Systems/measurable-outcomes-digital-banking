#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from harbor_fcu.integration_metrics import error_category_counts, reliability_sample, success_rate

rows = reliability_sample(); errors = error_category_counts(rows)
print("Harbor FCU / ClearVerify observed reliability (synthetic)")
print(f"Requests: {len(rows)}\nSuccessful business results: {sum(r.succeeded for r in rows)}")
print(f"Success rate: {success_rate(rows):.1f}%\nError rate: {100-success_rate(rows):.1f}%")
for category, count in sorted(errors.items(), key=lambda item: item[0].value): print(f"{category.value}: {count}")
print("Observed availability is the consumer's valid-business-result rate, not merely HTTP 200 rate.")
