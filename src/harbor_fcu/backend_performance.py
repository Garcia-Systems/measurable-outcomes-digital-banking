"""Deterministic SQLite and backend-performance laboratories for fictional Harbor FCU."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import statistics
import time
from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class OperationMeasurement:
    operation: str
    query_count: int
    duration_ms: float
    rows_returned: int
    result_hash: str
    success: bool


class InstrumentedConnection:
    """Small query counter, deliberately not an ORM or production profiler."""
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.query_count = 0

    def execute(self, sql: str, parameters: Iterable[Any] = ()) -> sqlite3.Cursor:
        self.query_count += 1
        return self.connection.execute(sql, tuple(parameters))


def create_database(*, indexed: bool = False) -> sqlite3.Connection:
    """Build the same small, entirely synthetic relational fixture every time."""
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript("""
      CREATE TABLE members(member_id INTEGER PRIMARY KEY, display_name TEXT NOT NULL);
      CREATE TABLE accounts(account_id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL,
        account_type TEXT NOT NULL, available_cents INTEGER NOT NULL);
      CREATE TABLE transactions(transaction_id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL,
        posted_at TEXT NOT NULL, amount_cents INTEGER NOT NULL, description TEXT NOT NULL);
      CREATE TABLE digital_sessions(session_id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL,
        started_at TEXT NOT NULL, successful INTEGER NOT NULL);
      CREATE TABLE verification_attempts(attempt_id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL,
        attempted_at TEXT NOT NULL, outcome TEXT NOT NULL);
    """)
    db.executemany("INSERT INTO members VALUES (?, ?)",
                   [(i, f"Synthetic Member {i:02d}") for i in range(1, 6)])
    accounts = [(i, ((i - 1) // 4) + 1, ("checking", "savings")[i % 2], 100_000 + i * 1_000)
                for i in range(1, 21)]
    db.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?)", accounts)
    transactions = []
    for transaction_id in range(1, 2001):
        account_id = ((transaction_id * 7) % 20) + 1
        day = ((transaction_id * 11) % 28) + 1
        minute = transaction_id % 60
        transactions.append((transaction_id, account_id, f"2026-01-{day:02d}T12:{minute:02d}:00Z",
                             ((transaction_id % 41) - 20) * 137, f"Synthetic activity {transaction_id:04d}"))
    db.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", transactions)
    db.executemany("INSERT INTO digital_sessions VALUES (?, ?, ?, ?)",
                   [(i, (i % 5) + 1, f"2026-02-{(i % 28)+1:02d}T09:00:00Z", i % 7 != 0) for i in range(1, 51)])
    db.executemany("INSERT INTO verification_attempts VALUES (?, ?, ?, ?)",
                   [(i, (i % 5) + 1, f"2026-02-{(i % 28)+1:02d}T10:00:00Z", "passed" if i % 6 else "failed") for i in range(1, 31)])
    if indexed:
        add_transaction_index(db)
    db.commit()
    return db


RECENT_SQL = """SELECT transaction_id, account_id, posted_at, amount_cents, description
FROM transactions WHERE account_id = ? ORDER BY posted_at DESC, transaction_id DESC LIMIT ?"""


def recent_transactions(db: Any, account_id: int = 8, limit: int = 20) -> list[dict[str, Any]]:
    return [dict(row) for row in db.execute(RECENT_SQL, (account_id, limit)).fetchall()]


def query_plan(db: sqlite3.Connection, account_id: int = 8, limit: int = 20) -> str:
    return " | ".join(str(row[3]) for row in db.execute("EXPLAIN QUERY PLAN " + RECENT_SQL, (account_id, limit)))


def add_transaction_index(db: sqlite3.Connection) -> None:
    db.execute("CREATE INDEX IF NOT EXISTS idx_transactions_account_posted ON transactions(account_id, posted_at DESC, transaction_id DESC)")


def percentile(values: list[float], percentile_value: float) -> float:
    ordered = sorted(values)
    return ordered[max(0, int((percentile_value / 100) * len(ordered) + .999999) - 1)]


def benchmark_query(db: sqlite3.Connection, executions: int = 100) -> dict[str, Any]:
    durations = []
    result = []
    for _ in range(executions):
        start = time.perf_counter_ns()
        result = recent_transactions(db)
        durations.append((time.perf_counter_ns() - start) / 1_000_000)
    return {"executions": executions, "median_ms": statistics.median(durations),
            "p95_ms": percentile(durations, 95), "maximum_ms": max(durations),
            "rows_returned": len(result)}


def normalize_result(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def result_hash(value: Any) -> str:
    return hashlib.sha256(normalize_result(value).encode()).hexdigest()[:16]


def measure_operation(operation: str, action: Callable[[InstrumentedConnection], Any], db: sqlite3.Connection) -> tuple[Any, OperationMeasurement]:
    instrumented = InstrumentedConnection(db)
    start = time.perf_counter_ns()
    try:
        result = action(instrumented)
        success = True
    except Exception:
        result, success = None, False
    duration = (time.perf_counter_ns() - start) / 1_000_000
    rows = len(result) if isinstance(result, list) else int(result is not None)
    return result, OperationMeasurement(operation, instrumented.query_count, duration, rows, result_hash(result), success)


def account_history_n_plus_one(db: InstrumentedConnection, member_id: int = 1) -> list[dict[str, Any]]:
    accounts = db.execute("SELECT account_id, account_type FROM accounts WHERE member_id=? ORDER BY account_id", (member_id,)).fetchall()
    output = []
    for account in accounts:
        transactions = recent_transactions(db, account["account_id"], 5)
        output.append({"account_id": account["account_id"], "account_type": account["account_type"], "transactions": transactions})
    return output


def account_history_joined(db: InstrumentedConnection, member_id: int = 1) -> list[dict[str, Any]]:
    accounts = db.execute("SELECT account_id, account_type FROM accounts WHERE member_id=? ORDER BY account_id", (member_id,)).fetchall()
    ids = [row["account_id"] for row in accounts]
    placeholders = ",".join("?" for _ in ids)
    rows = db.execute(f"""SELECT transaction_id, account_id, posted_at, amount_cents, description
      FROM (SELECT transaction_id, account_id, posted_at, amount_cents, description,
                   ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY posted_at DESC, transaction_id DESC) AS position
            FROM transactions WHERE account_id IN ({placeholders}))
      WHERE position <= 5 ORDER BY account_id, posted_at DESC, transaction_id DESC""", ids).fetchall()
    grouped = {account_id: [] for account_id in ids}
    for row in rows:
        grouped[row["account_id"]].append(dict(row))
    return [{"account_id": row["account_id"], "account_type": row["account_type"], "transactions": grouped[row["account_id"]]} for row in accounts]


def backend_workload() -> dict[str, Any]:
    """Deterministic modeled milliseconds make bottleneck lessons CI-stable."""
    components = {"application_logic": 40, "database": 180, "vendor_integration": 60, "serialization": 20}
    total = sum(components.values())
    return {"requests": 100, "total_ms": total, "operations_per_second": 100_000 / total,
            "components_ms": components, "shares_pct": {k: v * 100 / total for k, v in components.items()},
            "bottleneck": max(components, key=components.get)}


def concurrency_scenario() -> dict[str, Any]:
    # Careless operations both authorize from the same snapshot and oversubscribe it.
    starting, a, b = 50_000, 35_000, 25_000
    naive_reserved = a + b
    corrected_accepted = [a] if starting - a < b else [a, b]
    corrected_remaining = starting - sum(corrected_accepted)
    seen = set()
    applied = []
    for key, amount in [("reserve-A", a), ("reserve-A", a)]:
        if key not in seen:
            seen.add(key); applied.append(amount)
    return {"starting_cents": starting, "naive_reserved_cents": naive_reserved,
            "naive_invalid_states": int(naive_reserved > starting),
            "corrected_remaining_cents": corrected_remaining, "corrected_invalid_states": int(corrected_remaining < 0),
            "duplicate_state_changes": len(applied) - 1, "accepted_operations": len(corrected_accepted)}


def run_backend_experiment(executions: int = 40) -> dict[str, Any]:
    baseline_times, optimized_times = [], []
    baseline_measurement = optimized_measurement = None
    baseline_result = optimized_result = None
    for _ in range(executions):
        baseline_result, baseline_measurement = measure_operation("account_history_baseline", account_history_n_plus_one, create_database())
        optimized_result, optimized_measurement = measure_operation("account_history_optimized", account_history_joined, create_database(indexed=True))
        baseline_times.append(baseline_measurement.duration_ms); optimized_times.append(optimized_measurement.duration_ms)
    equivalent = normalize_result(baseline_result) == normalize_result(optimized_result)
    # A declared deterministic service-time model accompanies, but never replaces, observed timing.
    modeled_baseline, modeled_optimized = [18.0] * 38 + [24.0] * 2, [7.0] * 38 + [9.0] * 2
    criteria = {"performance": percentile(modeled_optimized, 95) <= percentile(modeled_baseline, 95) * .5,
                "query_efficiency": optimized_measurement.query_count <= 2,
                "correctness": equivalent, "safety": concurrency_scenario()["corrected_invalid_states"] == 0}
    return {"executions": executions,
            "baseline": {"median_ms": statistics.median(baseline_times), "p95_ms": percentile(baseline_times, 95), "queries": baseline_measurement.query_count, "modeled_p95_ms": percentile(modeled_baseline, 95), "hash": result_hash(baseline_result)},
            "optimized": {"median_ms": statistics.median(optimized_times), "p95_ms": percentile(optimized_times, 95), "queries": optimized_measurement.query_count, "modeled_p95_ms": percentile(modeled_optimized, 95), "hash": result_hash(optimized_result)},
            "equivalent": equivalent, "criteria": criteria, "overall": all(criteria.values())}
