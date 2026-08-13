"""Deterministic quality, security, and delivery measurements for fictional Harbor FCU."""

from dataclasses import dataclass
from typing import Iterable, Mapping


def rate(numerator: int, denominator: int) -> float:
    """Return a percentage, using 0 for an empty observed population."""
    if numerator < 0 or denominator < 0 or numerator > denominator:
        raise ValueError("counts must satisfy 0 <= numerator <= denominator")
    return 0.0 if denominator == 0 else numerator / denominator * 100


def test_metrics(results: Iterable[bool]) -> dict[str, int | float | bool]:
    observed = list(results)
    passed = sum(observed)
    failed = len(observed) - passed
    return {"tests_executed": len(observed), "tests_passed": passed,
            "tests_failed": failed, "pass_rate": rate(passed, len(observed)),
            "regression_detected": failed > 0}


def normalize_member_id(value: str) -> str:
    """The established behavior: ignore surrounding space and normalize case."""
    return value.strip().upper()


def regressed_normalize_member_id(value: str) -> str:
    """A deliberately broken candidate retained solely for the Chapter 25 lab."""
    return value.upper()


def regression_experiment(include_behavior_test: bool = True) -> dict[str, int | float | bool]:
    checks = [regressed_normalize_member_id("HF-100") == normalize_member_id("HF-100")]
    if include_behavior_test:
        checks.append(regressed_normalize_member_id(" hf-100 ") == "HF-100")
    return test_metrics(checks)


@dataclass(frozen=True)
class ReleaseRecord:
    release_id: str
    defect_types: tuple[str, ...]
    detected_pre_release: tuple[str, ...]

    @property
    def known(self) -> int:
        return len(self.defect_types)

    @property
    def detected(self) -> int:
        return len(self.detected_pre_release)


RELEASE_HISTORY = (
    ReleaseRecord("A", ("validation", "validation", "query", "authorization", "logging"),
                  ("validation", "validation", "query", "authorization")),
    ReleaseRecord("B", ("query", "logging", "logging", "validation"),
                  ("query", "validation", "logging")),
    ReleaseRecord("C", ("authorization", "logging", "validation"),
                  ("authorization", "validation")),
)


def defect_metrics(records: Iterable[ReleaseRecord]) -> dict[str, object]:
    rows = list(records)
    known = sum(r.known for r in rows)
    detected = sum(r.detected for r in rows)
    escaped_types: dict[str, int] = {}
    for record in rows:
        remaining = list(record.defect_types)
        for defect in record.detected_pre_release:
            remaining.remove(defect)
        for defect in remaining:
            escaped_types[defect] = escaped_types.get(defect, 0) + 1
    escaped = known - detected
    return {"known": known, "detected_pre_release": detected, "escaped": escaped,
            "detection_rate": rate(detected, known), "escape_rate": rate(escaped, known),
            "escaped_by_type": escaped_types}


SYNTHETIC_SECRET = "SYNTHETIC-TOKEN-DO-NOT-USE"
SECURITY_CASES = (
    {"name": "valid_transfer", "amount": 25, "operation": "transfer", "authorized": True, "expected": True},
    {"name": "negative_transfer_amount", "amount": -1, "operation": "transfer", "authorized": True, "expected": False},
    {"name": "zero_transfer_amount", "amount": 0, "operation": "transfer", "authorized": True, "expected": False},
    {"name": "oversized_transfer", "amount": 10001, "operation": "transfer", "authorized": True, "expected": False},
    {"name": "missing_amount", "amount": None, "operation": "transfer", "authorized": True, "expected": False},
    {"name": "unexpected_operation", "amount": 25, "operation": "export_all", "authorized": True, "expected": False},
    {"name": "unauthorized_operation", "amount": 25, "operation": "transfer", "authorized": False, "expected": False},
)


def transfer_allowed(case: Mapping[str, object]) -> bool:
    amount = case.get("amount")
    return (case.get("authorized") is True and case.get("operation") == "transfer"
            and isinstance(amount, (int, float)) and not isinstance(amount, bool)
            and 0 < amount <= 10_000)


def unsafe_log(payload: Mapping[str, object]) -> str:
    return "transfer " + " ".join(f"{key}={value}" for key, value in payload.items())


def safe_log(payload: Mapping[str, object]) -> str:
    allowed = ("request_id", "operation", "result")
    return "transfer " + " ".join(f"{key}={payload[key]}" for key in allowed if key in payload)


def prohibited_exposures(output: str, prohibited: Iterable[str]) -> list[str]:
    return [value for value in prohibited if value in output]


def security_validation() -> dict[str, object]:
    outcomes = [transfer_allowed(case) == case["expected"] for case in SECURITY_CASES]
    unsafe = unsafe_log({"request_id": "req-7", "token": SYNTHETIC_SECRET})
    safe = safe_log({"request_id": "req-7", "operation": "transfer", "token": SYNTHETIC_SECRET})
    exposures = prohibited_exposures(safe, (SYNTHETIC_SECRET,))
    invalid = [case for case in SECURITY_CASES if not case["expected"]]
    rejected = sum(not transfer_allowed(case) for case in invalid)
    return {"cases_tested": len(SECURITY_CASES), "cases_passed": sum(outcomes),
            "case_pass_rate": rate(sum(outcomes), len(outcomes)),
            "invalid_cases": len(invalid), "rejected_correctly": rejected,
            "accepted_incorrectly": len(invalid) - rejected,
            "unsafe_exposures_detected": len(prohibited_exposures(unsafe, (SYNTHETIC_SECRET,))),
            "safe_exposures_detected": len(exposures)}


CANDIDATES = {
    "valid": {"formatting": True, "unit": True, "integration": True, "security": True,
              "regression": True, "artifacts": True, "intentionally_invalid": False},
    "invalid": {"formatting": True, "unit": True, "integration": True, "security": False,
                "regression": False, "artifacts": True, "intentionally_invalid": True},
}


def release_gate(candidate: Mapping[str, bool]) -> dict[str, object]:
    names = ("formatting", "unit", "integration", "security", "regression", "artifacts")
    checks = {name: candidate.get(name, False) is True for name in names}
    return {"checks": checks, "checks_passed": sum(checks.values()),
            "pass_rate": rate(sum(checks.values()), len(checks)), "ready": all(checks.values())}


DELIVERY = {
    "before": {"defined_checks": 8, "caught": 4, "escaped": 8, "security_blocked": 2,
               "invalid_total": 3, "invalid_blocked": 1, "duration_seconds": 120,
               "deployments": 4, "successful_deployments": 2, "valid_candidate_passed": True},
    "after": {"defined_checks": 19, "caught": 10, "escaped": 2, "security_blocked": 7,
              "invalid_total": 3, "invalid_blocked": 3, "duration_seconds": 360,
              "deployments": 1, "successful_deployments": 1, "valid_candidate_passed": True},
}


def delivery_experiment() -> dict[str, object]:
    before, after = DELIVERY["before"].copy(), DELIVERY["after"].copy()
    for row in (before, after):
        row["escape_rate"] = rate(row["escaped"], row["caught"] + row["escaped"])
        row["release_gate_pass_rate"] = rate(row["invalid_blocked"], row["invalid_total"])
        row["deployment_success_rate"] = rate(row["successful_deployments"], row["deployments"])
    criteria = {"quality": after["escape_rate"] < before["escape_rate"],
                "security": after["security_blocked"] == 7,
                "release_blocking": after["invalid_blocked"] == after["invalid_total"],
                "valid_candidate_guardrail": after["valid_candidate_passed"] is True}
    return {"before": before, "after": after, "criteria": criteria, "success": all(criteria.values())}
