"""Shared measurements for normalized integration telemetry."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
import math
from .integrations import FailureCategory, IntegrationObservation, RETRYABLE


def percentile(values: list[int], percentile_value: float) -> int:
    if not values:
        raise ValueError("percentile requires observations")
    if not 0 < percentile_value <= 100:
        raise ValueError("percentile must be in (0, 100]")
    ordered = sorted(values)
    return ordered[math.ceil(percentile_value / 100 * len(ordered)) - 1]


def operation_groups(rows):
    groups = {}
    for row in rows:
        groups.setdefault(row.operation_id, []).append(row)
    return groups


def success_rate(rows):
    rows = list(rows)
    return 100 * sum(r.succeeded for r in rows) / len(rows) if rows else 0.0


def eventual_success_rate(rows):
    groups = operation_groups(rows)
    return 100 * sum(any(r.succeeded for r in group) for group in groups.values()) / len(groups) if groups else 0.0


def error_category_counts(rows):
    return Counter(r.error_category for r in rows if not r.succeeded)


def timeout_rate(rows):
    rows = list(rows)
    return 100 * sum(r.error_category is FailureCategory.TIMEOUT for r in rows) / len(rows) if rows else 0.0


def retry_rate(rows):
    groups = operation_groups(rows)
    return 100 * sum(len(g) > 1 for g in groups.values()) / len(groups) if groups else 0.0


def requests_per_operation(rows):
    rows = list(rows); groups = operation_groups(rows)
    return len(rows) / len(groups) if groups else 0.0


def retry_exhaustions(rows, max_attempts):
    return sum(len(g) == max_attempts and not g[-1].succeeded and g[-1].error_category in RETRYABLE
               for g in operation_groups(rows).values())


def total_operation_latencies(rows):
    return [sum(r.duration_ms for r in group) for group in operation_groups(rows).values()]


def evaluate_criteria(rows):
    groups = operation_groups(rows)
    permanent_retried = any(any(r.error_category is FailureCategory.PERMANENT_ERROR for r in g[:-1]) for g in groups.values())
    totals = total_operation_latencies(rows)
    return {
        "reliability target": eventual_success_rate(rows) >= 97,
        "latency target": percentile(totals, 95) < 2000,
        "request-volume guardrail": requests_per_operation(rows) < 1.20,
        "permanent-failure safety": not permanent_retried,
    }


def reliability_sample():
    from .integrations import ClearVerifyAdapter
    scenarios = (["success"] * 94 + ["temporary_failure"] * 3 + ["timeout"] * 2 + ["business_rejection"])
    return [ClearVerifyAdapter().call(f"verify-{i:03d}", scenario) for i, scenario in enumerate(scenarios, 1)]


def experiment(policy: str):
    """Matched 100-operation baseline or controlled-retry intervention."""
    from .integrations import ClearVerifyAdapter, execute_with_retries
    plans = [["success"]] * 92 + [["temporary_failure", "success"]] * 4 + [["timeout", "success"]] * 2 + [["permanent_failure"]] + [["business_rejection"]]
    rows = []
    for i, plan in enumerate(plans, 1):
        chosen = plan[:1] if policy == "baseline" else plan
        rows += execute_with_retries(ClearVerifyAdapter(), f"verify-{i:03d}", chosen, 1 if policy == "baseline" else 2)
    return rows
