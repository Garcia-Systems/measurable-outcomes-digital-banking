"""Deterministic operational telemetry and reliability measures for Harbor FCU."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable

from .measurement import percentage_improvement


def _time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


@dataclass(frozen=True)
class RequestObservation:
    timestamp: str
    request_id: str
    operation_id: str
    endpoint: str
    status_code: int
    latency_ms: int

    @property
    def successful(self) -> bool:
        return 200 <= self.status_code < 400


@dataclass(frozen=True)
class LogEvent:
    timestamp: str
    incident_id: str
    request_id: str
    operation_id: str
    component: str
    event: str
    result: str
    duration_ms: int | None = None
    error_category: str | None = None


@dataclass(frozen=True)
class Incident:
    incident_id: str
    service: str
    started_at: str
    detected_at: str
    investigation_started_at: str
    mitigated_at: str
    recovered_at: str
    severity: str
    failure_category: str


@dataclass(frozen=True)
class AlertWindow:
    timestamp: str
    error_rate_pct: float
    incident_active: bool


@dataclass(frozen=True)
class Alert:
    timestamp: str
    incident_active: bool


@dataclass(frozen=True)
class ReliabilityComparison:
    before_mttd_minutes: float
    after_mttd_minutes: float
    detection_improvement_pct: float
    before_mttr_minutes: float
    after_mttr_minutes: float
    recovery_improvement_pct: float
    before_false_positive_rate_pct: float
    after_false_positive_rate_pct: float
    diagnostic_queries_before: int
    diagnostic_queries_after: int


def request_success_rate(requests: Iterable[RequestObservation]) -> float:
    items = list(requests)
    if not items:
        raise ValueError("request success rate requires at least one request")
    return 100 * sum(item.successful for item in items) / len(items)


def observed_availability(requests: Iterable[RequestObservation]) -> float:
    """Useful-work availability: requests returning a successful response."""
    return request_success_rate(requests)


def endpoint_error_rates(requests: Iterable[RequestObservation]) -> dict[str, float]:
    groups: dict[str, list[RequestObservation]] = {}
    for item in requests:
        groups.setdefault(item.endpoint, []).append(item)
    return {name: 100 - request_success_rate(items) for name, items in groups.items()}


def _minutes(start: str, end: str) -> float:
    duration = (_time(end) - _time(start)).total_seconds() / 60
    if duration < 0:
        raise ValueError("incident timestamps must be chronological")
    return duration


def detection_duration(incident: Incident) -> float:
    return _minutes(incident.started_at, incident.detected_at)


def recovery_duration(incident: Incident) -> float:
    """Minutes from incident start until useful service is restored."""
    return _minutes(incident.started_at, incident.recovered_at)


def incident_duration(incident: Incident) -> float:
    return recovery_duration(incident)


def mttd(incidents: Iterable[Incident]) -> float:
    items = list(incidents)
    if not items:
        raise ValueError("MTTD requires at least one incident")
    return sum(map(detection_duration, items)) / len(items)


def mttr(incidents: Iterable[Incident]) -> float:
    items = list(incidents)
    if not items:
        raise ValueError("MTTR requires at least one incident")
    return sum(map(recovery_duration, items)) / len(items)


def evaluate_alerts(windows: Iterable[AlertWindow], threshold_pct: float,
                    consecutive_windows: int) -> list[Alert]:
    """Alert once when a strict threshold is exceeded for N consecutive windows."""
    if consecutive_windows < 1:
        raise ValueError("consecutive_windows must be positive")
    run = 0
    alerting = False
    alerts = []
    for window in windows:
        run = run + 1 if window.error_rate_pct > threshold_pct else 0
        if run >= consecutive_windows and not alerting:
            alerts.append(Alert(window.timestamp, window.incident_active))
            alerting = True
        if run == 0:
            alerting = False
    return alerts


def alert_false_positive_rate(alerts: Iterable[Alert]) -> float:
    items = list(alerts)
    if not items:
        return 0.0
    return 100 * sum(not item.incident_active for item in items) / len(items)


def reconstruct_timeline(events: Iterable[LogEvent], *, incident_id: str | None = None,
                         request_id: str | None = None, operation_id: str | None = None,
                         component: str | None = None) -> list[LogEvent]:
    filters = {"incident_id": incident_id, "request_id": request_id,
               "operation_id": operation_id, "component": component}
    selected = [event for event in events if all(value is None or getattr(event, key) == value
                                                   for key, value in filters.items())]
    return sorted(selected, key=lambda event: _time(event.timestamp))


def compare_reliability(before: Iterable[Incident], after: Iterable[Incident],
                        before_alerts: Iterable[Alert], after_alerts: Iterable[Alert],
                        diagnostic_queries_before: int, diagnostic_queries_after: int) -> ReliabilityComparison:
    before_items, after_items = list(before), list(after)
    before_mttd, after_mttd = mttd(before_items), mttd(after_items)
    before_mttr, after_mttr = mttr(before_items), mttr(after_items)
    return ReliabilityComparison(
        before_mttd, after_mttd, percentage_improvement(before_mttd, after_mttd, True),
        before_mttr, after_mttr, percentage_improvement(before_mttr, after_mttr, True),
        alert_false_positive_rate(before_alerts), alert_false_positive_rate(after_alerts),
        diagnostic_queries_before, diagnostic_queries_after,
    )


def evaluate_part4_success(result: ReliabilityComparison) -> dict[str, bool]:
    """Predeclared capstone criteria; guardrail means false positives do not rise."""
    return {
        "detection_improvement_at_least_50_pct": result.detection_improvement_pct >= 50,
        "recovery_improvement_at_least_25_pct": result.recovery_improvement_pct >= 25,
        "false_positive_rate_did_not_increase": (
            result.after_false_positive_rate_pct <= result.before_false_positive_rate_pct
        ),
    }


def reliability_requests() -> list[RequestObservation]:
    endpoints = (["/balances"] * 6 + ["/verify"] * 6 + ["/transfers"] * 8)
    failures = {"req-verify-05": 503, "req-transfer-04": 504, "req-transfer-07": 502}
    rows = []
    counters = {"/balances": 0, "/verify": 0, "/transfers": 0}
    base_latency = {"/balances": 85, "/verify": 240, "/transfers": 310}
    for number, endpoint in enumerate(endpoints, 1):
        counters[endpoint] += 1
        label = endpoint.strip("/")[:-1] if endpoint != "/verify" else "verify"
        request_id = f"req-{label}-{counters[endpoint]:02d}"
        status = failures.get(request_id, 200)
        latency = base_latency[endpoint] + counters[endpoint] * 9 + (2200 if status >= 500 else 0)
        rows.append(RequestObservation(f"2026-02-02T08:00:{number:02d}Z", request_id,
                                       f"op-{number:04d}", endpoint, status, latency))
    return rows


def incident_logs() -> list[LogEvent]:
    return [
        LogEvent("2026-02-03T08:12:03Z", "inc-017", "req-transfer-017", "transfer-0017", "banking-api", "latency_threshold", "EXCEEDED", 1900),
        LogEvent("2026-02-03T08:12:04Z", "inc-017", "req-transfer-017", "transfer-0017", "transfer-adapter", "vendor_call", "TIMEOUT", 3800, "DEPENDENCY_TIMEOUT"),
        LogEvent("2026-02-03T08:12:05Z", "inc-017", "req-transfer-017", "transfer-0017", "NorthstarPay", "response", "TIMEOUT", 3800, "TIMEOUT"),
        LogEvent("2026-02-03T08:12:06Z", "inc-017", "req-transfer-017", "transfer-0017", "banking-api", "request_complete", "FAILED", 4010, "DEPENDENCY_TIMEOUT"),
        LogEvent("2026-02-03T08:15:00Z", "inc-017", "", "", "banking-api", "error_rate", "EXCEEDED", None),
        LogEvent("2026-02-03T08:17:00Z", "inc-017", "", "", "alert-evaluator", "alert", "GENERATED"),
        LogEvent("2026-02-03T08:20:00Z", "inc-017", "", "", "incident-response", "investigation", "STARTED"),
        LogEvent("2026-02-03T08:31:00Z", "inc-017", "", "", "transfer-adapter", "mitigation", "APPLIED"),
        LogEvent("2026-02-03T08:34:00Z", "inc-017", "", "", "banking-api", "service", "RESTORED"),
    ]


def incident_metrics() -> dict[str, tuple[int, int]]:
    """Component p50/p95 milliseconds during inc-017; no diagnosis is encoded."""
    return {"member-web": (120, 180), "banking-api": (620, 4200), "database": (70, 110),
            "ClearVerify": (210, 290), "NorthstarPay": (880, 3800), "application-cpu-pct": (42, 58)}


def _incident(identifier: str, start_hour: int, detect: int, recover: int, category: str) -> Incident:
    start = datetime(2026, 2, int(identifier[-1]) + 4, start_hour, tzinfo=timezone.utc)
    stamp = lambda minutes: (start + timedelta(minutes=minutes)).isoformat().replace("+00:00", "Z")
    return Incident(identifier, "banking-api", stamp(0), stamp(detect), stamp(detect + 3),
                    stamp(recover - 4), stamp(recover), "SEV-2", category)


def response_incidents() -> list[Incident]:
    return [_incident("inc-021", 10, 8, 32, "CACHE_SATURATION"),
            _incident("inc-022", 11, 11, 41, "DEPENDENCY_TIMEOUT"),
            _incident("inc-023", 12, 5, 23, "QUERY_CONTENTION")]


def experiment_scenarios() -> tuple[list[Incident], list[Incident], list[Alert], list[Alert]]:
    before = [_incident("inc-031", 9, 12, 42, "DEPENDENCY_TIMEOUT"),
              _incident("inc-032", 10, 15, 48, "DEPENDENCY_TIMEOUT"),
              _incident("inc-033", 11, 9, 36, "DEPENDENCY_TIMEOUT")]
    after = [_incident("inc-041", 9, 4, 22, "DEPENDENCY_TIMEOUT"),
             _incident("inc-042", 10, 5, 25, "DEPENDENCY_TIMEOUT"),
             _incident("inc-043", 11, 3, 19, "DEPENDENCY_TIMEOUT")]
    before_alerts = [Alert(f"2026-03-01T0{i}:00:00Z", i >= 4) for i in range(1, 7)]
    after_alerts = [Alert("2026-03-08T01:00:00Z", False)] + [Alert(f"2026-03-08T0{i}:00:00Z", True) for i in range(2, 5)]
    return before, after, before_alerts, after_alerts
