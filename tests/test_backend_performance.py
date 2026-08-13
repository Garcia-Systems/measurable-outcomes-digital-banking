import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.backend_performance import (
    InstrumentedConnection, account_history_joined, account_history_n_plus_one,
    add_transaction_index, backend_workload, concurrency_scenario, create_database,
    measure_operation, query_plan, recent_transactions, result_hash,
    run_backend_experiment,
)


class DatabaseFixtureTest(unittest.TestCase):
    def test_fixture_is_deterministic_and_complete(self):
        first, second = create_database(), create_database()
        expected = {"members": 5, "accounts": 20, "transactions": 2000,
                    "digital_sessions": 50, "verification_attempts": 30}
        for table, count in expected.items():
            self.assertEqual(first.execute(f"SELECT count(*) FROM {table}").fetchone()[0], count)
        self.assertEqual(result_hash(recent_transactions(first)), result_hash(recent_transactions(second)))

    def test_recent_results_are_limited_filtered_and_sorted(self):
        rows = recent_transactions(create_database(), 8, 20)
        self.assertEqual(len(rows), 20)
        self.assertEqual({row["account_id"] for row in rows}, {8})
        keys = [(row["posted_at"], row["transaction_id"]) for row in rows]
        self.assertEqual(keys, sorted(keys, reverse=True))

    def test_index_changes_plan_without_changing_result(self):
        db = create_database(); before_result = recent_transactions(db); before = query_plan(db)
        add_transaction_index(db); after_result = recent_transactions(db); after = query_plan(db)
        self.assertIn("SCAN", before.upper())
        self.assertIn("INDEX", after.upper())
        self.assertEqual(before_result, after_result)


class BackendInstrumentationTest(unittest.TestCase):
    def test_n_plus_one_is_five_queries_and_batch_is_two(self):
        baseline, bm = measure_operation("baseline", account_history_n_plus_one, create_database())
        optimized, om = measure_operation("optimized", account_history_joined, create_database(indexed=True))
        self.assertEqual((bm.query_count, om.query_count), (5, 2))
        self.assertEqual(baseline, optimized)
        self.assertEqual(bm.result_hash, om.result_hash)
        self.assertTrue(bm.success and om.success)

    def test_counter_counts_each_execute(self):
        db = InstrumentedConnection(create_database())
        db.execute("SELECT 1"); db.execute("SELECT 2")
        self.assertEqual(db.query_count, 2)

    def test_workload_calculation_and_bottleneck(self):
        workload = backend_workload()
        self.assertEqual(workload["total_ms"], 300)
        self.assertAlmostEqual(sum(workload["shares_pct"].values()), 100)
        self.assertEqual(workload["bottleneck"], "database")
        self.assertAlmostEqual(workload["operations_per_second"], 100000 / 300)


class CorrectnessAndCapstoneTest(unittest.TestCase):
    def test_concurrency_and_idempotency_guardrails(self):
        scenario = concurrency_scenario()
        self.assertEqual(scenario["naive_invalid_states"], 1)
        self.assertEqual(scenario["corrected_invalid_states"], 0)
        self.assertEqual(scenario["corrected_remaining_cents"], 15000)
        self.assertEqual(scenario["duplicate_state_changes"], 0)

    def test_capstone_equivalence_and_declared_criteria(self):
        report = run_backend_experiment(5)
        self.assertTrue(report["equivalent"])
        self.assertEqual(report["baseline"]["queries"], 5)
        self.assertEqual(report["optimized"]["queries"], 2)
        self.assertEqual(report["baseline"]["hash"], report["optimized"]["hash"])
        self.assertTrue(all(report["criteria"].values()))
        self.assertTrue(report["overall"])


if __name__ == "__main__":
    unittest.main()
