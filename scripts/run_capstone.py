#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.outcomes import classify_statement, estimate_business_value, outcome_dataset, success_criteria

d = outcome_dataset(); b, a = d["baseline"], d["after"]
sections = {
 "1. TECHNICAL OUTCOMES": ("p95_api_latency_ms", "query_count", "error_rate_pct"),
 "2. RELIABILITY OUTCOMES": ("integration_success_pct", "mttd_min", "mttr_min"),
 "3. DELIVERY OUTCOMES": ("defect_escape_pct", "security_pass_pct", "release_success_pct"),
 "4. MEMBER OUTCOMES": ("completion_pct", "abandonment_pct", "p95_completion_min"),
 "5. OPERATIONAL OUTCOMES": ("manual_reviews", "support_cases"),
}
print("HARBOR FEDERAL CREDIT UNION\nMEASURABLE OUTCOMES ENGINEERING REVIEW\n(FICTIONAL; ALL DATA SYNTHETIC)\n\nInitiative: Digital Account Opening Improvement")
for heading, keys in sections.items():
    print("\n" + "="*48 + "\n" + heading + "\n" + "="*48)
    print("Metric                       Baseline   After   Change")
    for key in keys: print(f"{key:28} {b[key]:8.1f} {a[key]:7.1f} {a[key]-b[key]:+8.1f}")
value = estimate_business_value({"manual_reviews_avoided": b["manual_reviews"]-a["manual_reviews"]}, {"minutes_per_review": 8, "labor_cost_per_hour": 30})
print("\n"+"="*48+"\n6. BUSINESS RELEVANCE\n"+"="*48)
for label in value:
    print(label+": "+", ".join(f"{k}={v:.2f}" for k,v in value[label].items()))
print("Estimated values are assumption-dependent equivalents, not realized savings.")
print("\n"+"="*48+"\nSUCCESS CRITERIA\n"+"="*48)
for key, passed in success_criteria(d).items(): print(f"{key:28} {'PASS' if passed else 'FAIL'}")
claims = classify_statement("workflow completion percentage", b["completion_pct"], a["completion_pct"], "the controlled synthetic Harbor workload", "technical failure rate decreased", {"minutes_per_review": 8, "labor_cost_per_hour": 30})
for label, title in (("SUPPORTED", "SUPPORTED CONCLUSIONS"), ("POTENTIAL", "REASONABLE HYPOTHESES"), ("NOT_ESTABLISHED", "NOT ESTABLISHED")):
    print("\n"+"="*48+f"\n{title}\n"+"="*48)
    print("\n".join("- "+line for line in claims[label]) or "- None beyond measured evidence.")
