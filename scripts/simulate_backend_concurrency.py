#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.backend_performance import concurrency_scenario

r = concurrency_scenario()
print("Harbor FCU Synthetic Reservation Scenario")
print("Starting available amount: $500.00; A=$350.00; B=$250.00")
print(f"Careless read/authorize invalid final states: {r['naive_invalid_states']}")
print(f"Atomic corrected remaining: ${r['corrected_remaining_cents']/100:.2f}")
print(f"Corrected invalid final states: {r['corrected_invalid_states']}")
print(f"Duplicate-operation state changes: {r['duplicate_state_changes']}")
print("FAST + WRONG = FAILURE; correctness and idempotency are performance guardrails.")
