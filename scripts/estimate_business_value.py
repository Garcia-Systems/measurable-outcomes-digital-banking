#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.outcomes import estimate_business_value, outcome_dataset

d = outcome_dataset(); avoided = d["baseline"]["manual_reviews"] - d["after"]["manual_reviews"]
r = estimate_business_value({"manual_reviews_avoided": avoided},
                            {"minutes_per_review": 8, "labor_cost_per_hour": 30})
print("HARBOR BUSINESS-VALUE ESTIMATE (FICTIONAL / SYNTHETIC)")
for label in ("MEASURED", "ASSUMED", "DERIVED", "ESTIMATED"):
    print(f"\n{label}")
    for key, value in r[label].items(): print(f"{key}: {value:.2f}")
print("\nEstimated labor-value equivalent is not actual realized savings.")
