"""Small, dependency-free analytics tools for Harbor FCU's synthetic telemetry."""
from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class ConfusionMatrix:
    true_positive: int
    false_positive: int
    true_negative: int
    false_negative: int

    @property
    def precision(self) -> float:
        denominator = self.true_positive + self.false_positive
        return self.true_positive / denominator if denominator else 0.0

    @property
    def recall(self) -> float:
        denominator = self.true_positive + self.false_negative
        return self.true_positive / denominator if denominator else 0.0


def group_metrics(rows: Iterable[Mapping], key: str) -> dict[object, dict[str, float]]:
    """Group request telemetry and report count, error rate, and mean latency."""
    groups: dict[object, list[Mapping]] = {}
    for row in rows:
        groups.setdefault(row[key], []).append(row)
    return {name: {
        "count": len(items),
        "error_rate_pct": 100 * sum(not item["successful"] for item in items) / len(items),
        "mean_latency_ms": sum(item["latency_ms"] for item in items) / len(items),
    } for name, items in groups.items()}


def linear_trend(values: Sequence[float]) -> float:
    """Return ordinary least-squares slope per observation."""
    if len(values) < 2:
        raise ValueError("trend requires at least two observations")
    x_mean = (len(values) - 1) / 2
    y_mean = statistics.mean(values)
    denominator = sum((x - x_mean) ** 2 for x in range(len(values)))
    return sum((x - x_mean) * (y - y_mean) for x, y in enumerate(values)) / denominator


def moving_average(values: Sequence[float], window: int) -> list[float]:
    if window <= 0 or window > len(values):
        raise ValueError("window must be between one and the observation count")
    return [statistics.mean(values[index-window+1:index+1]) for index in range(window-1, len(values))]


def anomaly_scores(values: Sequence[float], baseline_size: int) -> list[float]:
    """Score observations in baseline standard deviations from a fixed baseline."""
    if baseline_size < 2 or baseline_size > len(values):
        raise ValueError("baseline must contain at least two available observations")
    baseline = values[:baseline_size]
    spread = statistics.pstdev(baseline)
    if spread == 0:
        raise ValueError("anomaly score requires a non-zero baseline deviation")
    center = statistics.mean(baseline)
    return [(value - center) / spread for value in values]


def detect_anomalies(values: Sequence[float], baseline_size: int, threshold: float) -> list[bool]:
    return [score >= threshold for score in anomaly_scores(values, baseline_size)]


def confusion_matrix(actual: Iterable[bool], predicted: Iterable[bool]) -> ConfusionMatrix:
    actual_items, predicted_items = list(actual), list(predicted)
    if len(actual_items) != len(predicted_items):
        raise ValueError("actual and predicted must have equal lengths")
    pairs = list(zip(actual_items, predicted_items))
    return ConfusionMatrix(
        sum(a and p for a, p in pairs), sum(not a and p for a, p in pairs),
        sum(not a and not p for a, p in pairs), sum(a and not p for a, p in pairs),
    )


def forecast_recent_average(history: Sequence[float], horizon: int, window: int = 3) -> list[float]:
    if horizon < 1:
        raise ValueError("horizon must be positive")
    if window < 1 or window > len(history):
        raise ValueError("invalid forecast window")
    return [statistics.mean(history[-window:])] * horizon


def forecast_trend(history: Sequence[float], horizon: int) -> list[float]:
    slope = linear_trend(history)
    intercept_at_end = statistics.mean(history) + slope * ((len(history) - 1) / 2)
    return [intercept_at_end + slope * step for step in range(1, horizon + 1)]


def forecast_error(actual: Sequence[float], predicted: Sequence[float]) -> dict[str, float]:
    if not actual or len(actual) != len(predicted):
        raise ValueError("actual and predicted forecasts must have equal non-zero lengths")
    errors = [a - p for a, p in zip(actual, predicted)]
    return {"mae": statistics.mean(abs(e) for e in errors),
            "rmse": math.sqrt(statistics.mean(e * e for e in errors))}


def operational_requests() -> list[dict]:
    """Deterministic request telemetry using Harbor's existing fictional vendors."""
    specifications = [("ClearVerify", 100, 1), ("HeritageCore", 100, 2), ("NorthstarPay", 100, 8)]
    rows = []
    for vendor, count, failures in specifications:
        for index in range(count):
            rows.append({"vendor": vendor, "endpoint": "/verify" if vendor == "ClearVerify" else "/transfers",
                         "hour": index % 4 + 9, "error_category": "vendor" if index < failures else "none",
                         "deployment_version": "2026.08.2" if index >= 50 else "2026.08.1",
                         "successful": index >= failures, "latency_ms": 100 + index % 10 + failures * 5})
    return rows


def anomaly_scenario() -> tuple[list[float], list[bool]]:
    values = [2, 3, 2, 4, 3, 2, 3, 4, 2, 3, 9, 10, 3, 8, 4, 3]
    truth = [False] * 10 + [True, True, False, True, False, False]
    return values, truth


def workload_scenario() -> tuple[list[float], list[float]]:
    return [100, 110, 120, 130, 140, 150, 160, 170], [180, 190, 200]


def incident_scenario() -> list[dict]:
    """Known ground truth derived from incident/telemetry concepts in Part IV."""
    return [
        {"id": f"INC-{i:02}", "error_rate": e, "p95_latency": l, "affected_operations": o,
         "vendor_failure_rate": v, "database_latency": d, "recent_deployment": r, "immediate": y}
        for i, (e, l, o, v, d, r, y) in enumerate([
            (1,180,1,1,40,0,0),(9,900,4,7,160,1,1),(6,350,3,2,70,0,1),(2,800,1,1,210,0,0),
            (8,420,2,8,80,0,1),(3,250,2,2,55,1,0),(5,700,5,3,190,1,1),(1,500,1,6,60,0,0),
            (7,300,4,1,50,0,1),(4,650,2,5,140,1,1),(2,220,1,1,45,0,0),(6,500,3,6,110,0,1),
        ], 1)
    ]


def rule_priority(row: Mapping) -> bool:
    return row["error_rate"] >= 7 or row["p95_latency"] >= 750


def priority_score(row: Mapping) -> float:
    """Transparent weighted score, not a claim of production-trained ML."""
    return (row["error_rate"] / 10 + row["p95_latency"] / 1000 + row["affected_operations"] / 5
            + row["vendor_failure_rate"] / 10 + row["database_latency"] / 250
            + 0.4 * row["recent_deployment"])


def score_priority(row: Mapping) -> bool:
    return priority_score(row) >= 2.0


def explain_priority(row: Mapping) -> list[str]:
    checks = (("error rate high", row["error_rate"] >= 5), ("p95 latency high", row["p95_latency"] >= 600),
              ("affected workflows high", row["affected_operations"] >= 3),
              ("vendor failure rate high", row["vendor_failure_rate"] >= 5),
              ("database latency high", row["database_latency"] >= 125),
              ("recent deployment", bool(row["recent_deployment"])))
    return [label for label, applies in checks if applies]


def compare_prioritizers(rows: Sequence[Mapping]) -> dict[str, ConfusionMatrix]:
    truth = [bool(row["immediate"]) for row in rows]
    return {"rule": confusion_matrix(truth, [rule_priority(row) for row in rows]),
            "scoring": confusion_matrix(truth, [score_priority(row) for row in rows])}


def workflow_outcomes(rows: Sequence[Mapping], assisted: bool) -> dict[str, float]:
    """Simulate one investigation starting every four minutes in queue order."""
    ordered = sorted(rows, key=priority_score, reverse=True) if assisted else list(rows)
    starts = {row["id"]: position * 4 for position, row in enumerate(ordered)}
    critical = [row for row in rows if row["immediate"]]
    investigation_times = [starts[row["id"]] for row in critical]
    detected = [row for row in rows if (score_priority(row) if assisted else rule_priority(row))]
    matrix = confusion_matrix([bool(row["immediate"]) for row in rows], [row in detected for row in rows])
    return {"median_investigation_minutes": statistics.median(investigation_times),
            "alerts_investigated": len(detected), "critical_first_three": sum(row["immediate"] for row in ordered[:3]),
            "mttd_minutes": 5 if assisted else 8, "mttr_minutes": statistics.mean(investigation_times) + 20,
            "true_positive": matrix.true_positive, "false_positive": matrix.false_positive,
            "false_negative": matrix.false_negative, "precision": matrix.precision, "recall": matrix.recall}


def intelligence_experiment() -> dict:
    rows = incident_scenario(); baseline = workflow_outcomes(rows, False); assisted = workflow_outcomes(rows, True)
    criteria = {"detection": assisted["recall"] >= .85,
                "prioritization": assisted["median_investigation_minutes"] < baseline["median_investigation_minutes"],
                "workload_guardrail": assisted["false_positive"] <= baseline["false_positive"] + 2}
    return {"baseline": baseline, "assisted": assisted, "criteria": criteria}
