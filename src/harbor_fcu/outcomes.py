"""Cross-layer outcome measurements for the fictional, synthetic Harbor FCU lab."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .measurement import percentile


# These are observations, not summary results.  Reports calculate every displayed
# rate and percentile from the same deterministic controlled population.
BASELINE_RUNS = tuple(
    {"success": i < 88, "latency_ms": 1250 if i % 20 == 0 else 620 + i % 90,
     "completed": i < 78, "completion_min": 13.0 + (i % 8) / 2,
     "manual_review": i < 40, "support": i < 18} for i in range(100)
)
IMPROVED_RUNS = tuple(
    {"success": i < 97, "latency_ms": 850 if i % 20 == 0 else 430 + i % 70,
     "completed": i < 88, "completion_min": 8.0 + (i % 7) / 2,
     "manual_review": i < 26, "support": i < 9} for i in range(100)
)


def _rate(count: int, total: int) -> float:
    return 100 * count / total


def measure_runs(runs=BASELINE_RUNS) -> dict[str, float]:
    """Measure technical, member, and operational signals over one population."""
    total = len(runs)
    successes = sum(row["success"] for row in runs)
    completions = [row for row in runs if row["completed"]]
    return {
        "integration_success_pct": _rate(successes, total),
        "error_rate_pct": _rate(total - successes, total),
        "p95_api_latency_ms": float(percentile([row["latency_ms"] for row in runs], 95)),
        "completion_pct": _rate(len(completions), total),
        "abandonment_pct": _rate(total - len(completions), total),
        "p95_completion_min": float(percentile([row["completion_min"] for row in completions], 95)),
        "manual_reviews": float(sum(row["manual_review"] for row in runs)),
        "support_cases": float(sum(row["support"] for row in runs)),
    }


def outcome_dataset() -> dict[str, dict[str, float]]:
    before, after = measure_runs(BASELINE_RUNS), measure_runs(IMPROVED_RUNS)
    # Incident and delivery observations originate in the deterministic initiative
    # fixture; rates are computed here alongside the cross-layer experiment.
    before.update({"mttd_min": 14, "mttr_min": 46, "query_count": 7,
                   "defect_escape_pct": 40, "release_success_pct": 50,
                   "security_pass_pct": 100, "critical_error_pct": 2})
    after.update({"mttd_min": 6, "mttr_min": 24, "query_count": 3,
                  "defect_escape_pct": 10, "release_success_pct": 100,
                  "security_pass_pct": 100, "critical_error_pct": 1})
    return {"baseline": before, "after": after}


def operational_scorecard() -> dict[str, tuple[float, float]]:
    data = outcome_dataset()
    keys = ("integration_success_pct", "p95_api_latency_ms", "mttd_min", "mttr_min",
            "defect_escape_pct", "release_success_pct")
    return {key: (data["baseline"][key], data["after"][key]) for key in keys}


def estimate_business_value(measured: Mapping[str, float],
                            assumptions: Mapping[str, float | None]) -> dict[str, dict[str, float]]:
    """Return only derivations/estimates enabled by explicit supplied assumptions."""
    result = {"MEASURED": dict(measured), "ASSUMED": {}, "DERIVED": {}, "ESTIMATED": {}}
    supplied = {key: value for key, value in assumptions.items() if value is not None}
    result["ASSUMED"].update(supplied)
    avoided = measured.get("manual_reviews_avoided")
    minutes = supplied.get("minutes_per_review")
    labor = supplied.get("labor_cost_per_hour")
    if avoided is not None and minutes is not None:
        result["DERIVED"]["review_hours_avoided"] = avoided * minutes / 60
        if labor is not None:
            result["ESTIMATED"]["labor_value_equivalent"] = result["DERIVED"]["review_hours_avoided"] * labor
    requests = measured.get("vendor_requests_avoided")
    if requests is not None and "vendor_cost_per_request" in supplied:
        result["ESTIMATED"]["vendor_cost_effect"] = requests * supplied["vendor_cost_per_request"]
    incidents = measured.get("incidents_avoided")
    hours = supplied.get("engineering_hours_per_incident")
    if incidents is not None and hours is not None:
        result["DERIVED"]["engineering_hours_avoided"] = incidents * hours
        if labor is not None:
            result["ESTIMATED"]["engineering_labor_value_equivalent"] = incidents * hours * labor
    return result


def classify_statement(metric: str, baseline: float, after: float, context: str,
                       downstream_measurement: str | None = None,
                       assumptions: Mapping[str, float] | None = None) -> dict[str, list[str]]:
    """Construct deterministic, evidence-disciplined statements."""
    supported = [f"In {context}, {metric} changed from {baseline:g} to {after:g}."]
    potential = []
    if downstream_measurement:
        supported.append(f"The same measurement also observed {downstream_measurement}.")
    else:
        potential.append("A downstream member or operational effect should be measured.")
    if assumptions:
        potential.append("Business value can be estimated only under the stated assumptions.")
    return {"SUPPORTED": supported, "POTENTIAL": potential,
            "NOT_ESTABLISHED": ["Member satisfaction, revenue, retention, and realized savings were not established."]}


def success_criteria(data=None) -> dict[str, bool]:
    data = data or outcome_dataset(); before, after = data["baseline"], data["after"]
    return {
        "Technical": after["p95_api_latency_ms"] <= before["p95_api_latency_ms"] * .8 and after["query_count"] < before["query_count"],
        "Reliability": after["integration_success_pct"] >= 95 and after["mttr_min"] <= 30,
        "Member": after["completion_pct"] - before["completion_pct"] >= 5,
        "Delivery": after["security_pass_pct"] == 100 and after["release_success_pct"] == 100,
        "Operational": after["manual_reviews"] < before["manual_reviews"],
        "Guardrails": after["critical_error_pct"] <= before["critical_error_pct"] and after["security_pass_pct"] == 100,
    }


def audience_report(audience: str) -> str:
    if audience not in {"engineer", "operations", "executive"}:
        raise ValueError("audience must be engineer, operations, or executive")
    d = outcome_dataset(); b, a = d["baseline"], d["after"]
    shared = "FICTIONAL HARBOR FCU — SYNTHETIC CONTROLLED LAB\n"
    if audience == "engineer":
        return shared + (f"ENGINEER\np95 API latency: {b['p95_api_latency_ms']:.0f} → {a['p95_api_latency_ms']:.0f} ms\n"
                         f"Error rate: {b['error_rate_pct']:.1f}% → {a['error_rate_pct']:.1f}%\nQuery count: {b['query_count']:.0f} → {a['query_count']:.0f}\nFailed security checks: 0")
    if audience == "operations":
        return shared + (f"OPERATIONS\nWorkflow completion: {b['completion_pct']:.1f}% → {a['completion_pct']:.1f}%\n"
                         f"Manual reviews: {b['manual_reviews']:.0f} → {a['manual_reviews']:.0f}\nMTTR: {b['mttr_min']:.0f} → {a['mttr_min']:.0f} min\nSupport cases: {b['support_cases']:.0f} → {a['support_cases']:.0f}")
    return shared + (f"EXECUTIVE\nApplication completion increased {a['completion_pct']-b['completion_pct']:.1f} percentage points; "
                     f"verification failures decreased {(b['error_rate_pct']-a['error_rate_pct'])/b['error_rate_pct']*100:.1f}%.\n"
                     f"Manual reviews decreased {b['manual_reviews']-a['manual_reviews']:.0f}; release success was {a['release_success_pct']:.0f}% against a 100% target.\n"
                     "No satisfaction, revenue, retention, or realized-savings claim is established.")
