"""Reusable member-journey measurements for the fictional Harbor FCU labs."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import median
from typing import Iterable

from .measurement import Criterion, CriterionResult, evaluate, percentile


FUNNEL_STAGES = (
    "application_viewed", "application_started", "personal_info_completed",
    "verification_completed", "review_viewed", "application_submitted",
)


@dataclass(frozen=True)
class AnalyticsEvent:
    session_id: str
    event_type: str
    timestamp: str
    step: str
    result: str
    duration_ms: int


@dataclass(frozen=True)
class ExperienceMeasurement:
    sessions: int
    starts: int
    completions: int
    completion_rate_pct: float
    incomplete_sessions: int
    median_completion_ms: float
    p95_completion_ms: int
    error_rate_pct: float


@dataclass(frozen=True)
class ExperienceComparison:
    before: ExperienceMeasurement
    after: ExperienceMeasurement
    completion_change_points: float
    p95_improvement_pct: float
    error_change_points: float


def load_events(path: Path) -> list[AnalyticsEvent]:
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise ValueError("event data must contain at least one event")
    events = [AnalyticsEvent(row["session_id"], row["event_type"], row["timestamp"],
                             row["step"], row["result"], int(row["duration_ms"]))
              for row in rows]
    return sorted(events, key=lambda event: (event.session_id, event.timestamp))


def sessions(events: Iterable[AnalyticsEvent]) -> dict[str, list[AnalyticsEvent]]:
    grouped: dict[str, list[AnalyticsEvent]] = defaultdict(list)
    for event in events:
        grouped[event.session_id].append(event)
    return dict(grouped)


def task_completion_rate(events: Iterable[AnalyticsEvent], start="application_started",
                         completion="application_submitted") -> float:
    counts = funnel_counts(events, (start, completion))
    if counts[start] == 0:
        raise ValueError("completion rate requires at least one task start")
    return 100 * counts[completion] / counts[start]


def funnel_counts(events: Iterable[AnalyticsEvent], stages=FUNNEL_STAGES) -> dict[str, int]:
    reached = {event_type for event_type in stages}
    result = dict.fromkeys(stages, 0)
    for journey in sessions(events).values():
        observed = {event.event_type for event in journey} & reached
        for stage in stages:
            result[stage] += stage in observed
    return result


def stage_conversion(counts: dict[str, int]) -> dict[str, float | None]:
    result: dict[str, float | None] = {}
    previous = None
    for stage, count in counts.items():
        result[stage] = None if previous is None else (100 * count / previous if previous else 0.0)
        previous = count
    return result


def stage_abandonment(counts: dict[str, int]) -> dict[str, float | None]:
    return {stage: None if value is None else 100 - value
            for stage, value in stage_conversion(counts).items()}


def largest_dropoff(counts: dict[str, int]) -> tuple[str, int, float]:
    pairs = list(counts.items())
    if len(pairs) < 2:
        raise ValueError("drop-off requires at least two stages")
    candidates = [(stage, pairs[index - 1][1] - count,
                   100 * (pairs[index - 1][1] - count) / pairs[index - 1][1]
                   if pairs[index - 1][1] else 0.0)
                  for index, (stage, count) in enumerate(pairs[1:], 1)]
    return max(candidates, key=lambda item: item[1])


def completion_durations(events: Iterable[AnalyticsEvent]) -> dict[str, int]:
    result = {}
    for session_id, journey in sessions(events).items():
        by_type = {event.event_type: event for event in journey}
        if "application_started" in by_type and "application_submitted" in by_type:
            start = datetime.fromisoformat(by_type["application_started"].timestamp)
            end = datetime.fromisoformat(by_type["application_submitted"].timestamp)
            result[session_id] = int((end - start).total_seconds() * 1000)
    return result


def median_duration(values: Iterable[int]) -> float:
    items = list(values)
    if not items:
        raise ValueError("median requires at least one duration")
    return float(median(items))


def step_durations(events: Iterable[AnalyticsEvent]) -> dict[str, list[int]]:
    result: dict[str, list[int]] = defaultdict(list)
    for event in events:
        if event.duration_ms >= 0 and event.event_type not in {"session_started", "application_viewed"}:
            result[event.step].append(event.duration_ms)
    return dict(result)


def summarize_experience(events: Iterable[AnalyticsEvent]) -> ExperienceMeasurement:
    items = list(events)
    grouped = sessions(items)
    counts = funnel_counts(items, ("application_started", "application_submitted"))
    if not counts["application_started"]:
        raise ValueError("experience measurement requires at least one task start")
    durations = list(completion_durations(items).values())
    if not durations:
        raise ValueError("experience measurement requires at least one completion")
    error_sessions = sum(any(event.result == "error" for event in journey)
                         for journey in grouped.values())
    starts, completed = counts.values()
    return ExperienceMeasurement(len(grouped), starts, completed, 100 * completed / starts,
                                 starts - completed, median_duration(durations),
                                 percentile(durations, 95), 100 * error_sessions / len(grouped))


def compare_experience(before: ExperienceMeasurement,
                       after: ExperienceMeasurement) -> ExperienceComparison:
    return ExperienceComparison(
        before, after, after.completion_rate_pct - before.completion_rate_pct,
        100 * (before.p95_completion_ms - after.p95_completion_ms) / before.p95_completion_ms,
        after.error_rate_pct - before.error_rate_pct,
    )


def evaluate_experience(comparison: ExperienceComparison) -> list[CriterionResult]:
    """Evaluate Part II's predeclared primary, secondary, and guardrail criteria."""
    criteria = (
        (comparison.completion_change_points, Criterion("completion_change_points", ">=", 5)),
        (comparison.p95_improvement_pct, Criterion("p95_improvement_pct", ">=", 20)),
        (comparison.error_change_points, Criterion("error_change_points", "<=", 0)),
    )
    return [evaluate(actual, criterion) for actual, criterion in criteria]
