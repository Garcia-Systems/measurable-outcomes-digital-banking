"""Locations and success criteria for the shared fictional Harbor scenarios."""

from pathlib import Path

from .measurement import Criterion

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "synthetic" / "part1"
BASELINE = DATA / "verification_baseline.csv"
FAST_CANDIDATE = DATA / "verification_fast_candidate.csv"
RELIABLE_CANDIDATE = DATA / "verification_reliable_candidate.csv"

SUCCESS_CRITERIA = (
    Criterion("p95_latency_ms", "<", 800),
    Criterion("error_rate_pct", "<", 1),
    Criterion("success_rate_pct", ">=", 99),
)
