"""Deterministic, network-free integration laboratory for fictional Harbor FCU."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class FailureCategory(str, Enum):
    SUCCESS = "SUCCESS"
    TIMEOUT = "TIMEOUT"
    TRANSIENT_ERROR = "TRANSIENT_ERROR"
    PERMANENT_ERROR = "PERMANENT_ERROR"
    INVALID_RESPONSE = "INVALID_RESPONSE"
    BUSINESS_REJECTION = "BUSINESS_REJECTION"


@dataclass(frozen=True)
class IntegrationObservation:
    operation_id: str
    vendor: str
    operation: str
    attempt: int
    error_category: FailureCategory
    duration_ms: int
    timestamp: str

    @property
    def succeeded(self) -> bool:
        return self.error_category is FailureCategory.SUCCESS


@dataclass(frozen=True)
class IntegrationResult:
    operation_id: str
    vendor: str
    operation: str
    status: FailureCategory
    duration_ms: int
    attempts: int


REST_SCENARIOS = {
    "success": (200, {"decision": "verified"}, 180),
    "slow_success": (200, {"decision": "verified"}, 1800),
    "temporary_failure": (503, {"error": "busy"}, 260),
    "timeout": (None, None, 2200),
    "invalid_response": (200, {"unexpected": True}, 140),
    "permanent_failure": (400, {"error": "invalid_request"}, 110),
    "business_rejection": (200, {"decision": "rejected"}, 170),
}

SOAP_SCENARIOS = {
    "success": ("OK", "<Account><Status>OPEN</Status></Account>", 240),
    "slow_success": ("OK", "<Account><Status>OPEN</Status></Account>", 1550),
    "temporary_failure": ("Server.Busy", None, 310),
    "timeout": ("TIMEOUT", None, 2200),
    "invalid_response": ("OK", "<Account>", 190),
    "permanent_failure": ("Client.InvalidAccount", None, 130),
}


def normalize_rest(status: int | None, body: dict | None) -> FailureCategory:
    if status is None:
        return FailureCategory.TIMEOUT
    if status >= 500:
        return FailureCategory.TRANSIENT_ERROR
    if status >= 400:
        return FailureCategory.PERMANENT_ERROR
    if not body or "decision" not in body:
        return FailureCategory.INVALID_RESPONSE
    return FailureCategory.SUCCESS if body["decision"] == "verified" else FailureCategory.BUSINESS_REJECTION


def normalize_soap(fault: str, payload: str | None) -> FailureCategory:
    if fault == "TIMEOUT":
        return FailureCategory.TIMEOUT
    if fault == "Server.Busy":
        return FailureCategory.TRANSIENT_ERROR
    if fault.startswith("Client."):
        return FailureCategory.PERMANENT_ERROR
    if not payload or not payload.endswith("</Account>"):
        return FailureCategory.INVALID_RESPONSE
    return FailureCategory.SUCCESS


class ClearVerifyAdapter:
    vendor = "ClearVerify"
    operation = "verify_member"

    def call(self, operation_id: str, scenario: str, attempt: int = 1) -> IntegrationObservation:
        status, body, duration = REST_SCENARIOS[scenario]
        return IntegrationObservation(operation_id, self.vendor, self.operation, attempt,
                                      normalize_rest(status, body), duration,
                                      f"2026-01-10T00:00:{int(operation_id.split('-')[-1]) % 60:02d}Z")


class HeritageCoreAdapter:
    vendor = "HeritageCore"
    operation = "account_status"

    def call(self, operation_id: str, scenario: str, attempt: int = 1) -> IntegrationObservation:
        fault, payload, duration = SOAP_SCENARIOS[scenario]
        return IntegrationObservation(operation_id, self.vendor, self.operation, attempt,
                                      normalize_soap(fault, payload), duration,
                                      f"2026-01-10T01:00:{int(operation_id.split('-')[-1]) % 60:02d}Z")


RETRYABLE = {FailureCategory.TIMEOUT, FailureCategory.TRANSIENT_ERROR}


def execute_with_retries(adapter, operation_id: str, scenarios: Iterable[str], max_attempts: int) -> list[IntegrationObservation]:
    """Execute a bounded scenario sequence; permanent/semantic failures stop immediately."""
    observations = []
    for attempt, scenario in enumerate(scenarios, 1):
        if attempt > max_attempts:
            break
        observation = adapter.call(operation_id, scenario, attempt)
        observations.append(observation)
        if observation.succeeded or observation.error_category not in RETRYABLE:
            break
    return observations


class NorthstarPaySimulator:
    """Tiny stateful demonstration of safe retry after a lost response."""
    def __init__(self):
        self.processed: dict[str, int] = {}

    def transfer(self, idempotency_key: str, amount_cents: int, lose_response: bool = False) -> FailureCategory:
        if idempotency_key not in self.processed:
            self.processed[idempotency_key] = amount_cents
        return FailureCategory.TIMEOUT if lose_response else FailureCategory.SUCCESS

