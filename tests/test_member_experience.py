import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from harbor_fcu.member_experience import (AnalyticsEvent, compare_experience,
    completion_durations, evaluate_experience, funnel_counts, largest_dropoff,
    load_events, median_duration, stage_abandonment, stage_conversion,
    step_durations, summarize_experience, task_completion_rate)
from harbor_fcu.measurement import percentile


class MemberExperienceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = ROOT / "data/synthetic/part2"
        cls.before_events = load_events(data / "application_before.csv")
        cls.after_events = load_events(data / "application_after.csv")

    def test_completion_and_incomplete_sessions(self):
        measurement = summarize_experience(self.before_events)
        self.assertEqual((measurement.sessions, measurement.starts, measurement.completions), (60, 55, 38))
        self.assertAlmostEqual(task_completion_rate(self.before_events), 100 * 38 / 55)
        self.assertEqual(measurement.incomplete_sessions, 17)

    def test_funnel_conversion_abandonment_and_dropoff(self):
        counts = funnel_counts(self.before_events)
        self.assertEqual(list(counts.values()), [58, 55, 51, 43, 41, 38])
        self.assertIsNone(stage_conversion(counts)["application_viewed"])
        self.assertAlmostEqual(stage_conversion(counts)["verification_completed"], 100 * 43 / 51)
        self.assertAlmostEqual(stage_abandonment(counts)["verification_completed"], 100 * 8 / 51)
        self.assertEqual(largest_dropoff(counts)[:2], ("verification_completed", 8))

    def test_duration_percentiles_and_stage_timing(self):
        durations = completion_durations(self.before_events)
        measurement = summarize_experience(self.before_events)
        self.assertEqual(len(durations), 38)
        self.assertEqual(measurement.p95_completion_ms, percentile(durations.values(), 95))
        self.assertEqual(median_duration([1, 3, 8, 10]), 5.5)
        self.assertGreater(percentile(step_durations(self.before_events)["verification"], 95), 400_000)

    def test_before_after_comparison_and_criteria(self):
        comparison = compare_experience(summarize_experience(self.before_events),
                                        summarize_experience(self.after_events))
        self.assertAlmostEqual(comparison.completion_change_points, 100 * 44 / 55 - 100 * 38 / 55)
        self.assertGreater(comparison.p95_improvement_pct, 0)
        self.assertLess(comparison.error_change_points, 0)
        self.assertEqual([result.passed for result in evaluate_experience(comparison)], [True, False, True])

    def test_edge_cases(self):
        event = AnalyticsEvent("session_1", "application_viewed", "2026-01-01T00:00:00Z", "view", "ok", 0)
        with self.assertRaises(ValueError): task_completion_rate([event])
        with self.assertRaises(ValueError): median_duration([])
        self.assertEqual(stage_conversion({"viewed": 0, "started": 0})["started"], 0)
        with self.assertRaises(ValueError): largest_dropoff({"viewed": 1})


if __name__ == "__main__":
    unittest.main()
