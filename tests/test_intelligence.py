import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from harbor_fcu.intelligence import (
    anomaly_scenario, compare_prioritizers, confusion_matrix, detect_anomalies,
    forecast_error, forecast_recent_average, forecast_trend, group_metrics,
    incident_scenario, intelligence_experiment, linear_trend, moving_average,
    operational_requests, rule_priority, score_priority, workflow_outcomes,
    workload_scenario,
)


class AnalyticsTests(unittest.TestCase):
    def test_grouping_exposes_localized_vendor_problem(self):
        grouped = group_metrics(operational_requests(), "vendor")
        self.assertEqual(grouped["ClearVerify"]["count"], 100)
        self.assertEqual(grouped["ClearVerify"]["error_rate_pct"], 1.0)
        self.assertEqual(grouped["NorthstarPay"]["error_rate_pct"], 8.0)

    def test_moving_average_and_trend(self):
        self.assertEqual(moving_average([1, 2, 3, 4], 2), [1.5, 2.5, 3.5])
        self.assertEqual(linear_trend([10, 20, 30]), 10)
        with self.assertRaises(ValueError): moving_average([1], 0)


class DetectionTests(unittest.TestCase):
    def test_manual_confusion_matrix_and_metrics(self):
        matrix = confusion_matrix([True, True, False, False], [True, False, True, False])
        self.assertEqual((matrix.true_positive, matrix.false_positive,
                          matrix.true_negative, matrix.false_negative), (1, 1, 1, 1))
        self.assertEqual(matrix.precision, .5)
        self.assertEqual(matrix.recall, .5)

    def test_detector_matches_known_ground_truth(self):
        values, truth = anomaly_scenario()
        matrix = confusion_matrix(truth, detect_anomalies(values, 10, 3))
        self.assertEqual((matrix.true_positive, matrix.false_positive,
                          matrix.true_negative, matrix.false_negative), (3, 0, 13, 0))

    def test_confusion_matrix_rejects_different_lengths(self):
        with self.assertRaises(ValueError): confusion_matrix([True], [])


class ForecastTests(unittest.TestCase):
    def test_forecasts_and_errors(self):
        history, actual = workload_scenario()
        self.assertEqual(forecast_recent_average(history, 3), [160, 160, 160])
        self.assertEqual(forecast_trend(history, 3), actual)
        self.assertEqual(forecast_error(actual, actual), {"mae": 0, "rmse": 0})
        error = forecast_error([2, 4], [1, 2])
        self.assertEqual(error["mae"], 1.5)
        self.assertAlmostEqual(error["rmse"], (2.5) ** .5)


class PrioritizationTests(unittest.TestCase):
    def test_rule_and_scoring_are_compared_on_same_rows(self):
        rows = incident_scenario(); compared = compare_prioritizers(rows)
        self.assertEqual(compared["rule"].true_positive, 3)
        self.assertEqual(compared["scoring"].true_positive, 7)
        self.assertGreater(compared["scoring"].recall, compared["rule"].recall)
        self.assertEqual(len([r for r in rows if rule_priority(r)]), 4)
        self.assertEqual(len([r for r in rows if score_priority(r)]), 8)

    def test_downstream_workflow_and_success_criteria(self):
        rows = incident_scenario()
        baseline, assisted = workflow_outcomes(rows, False), workflow_outcomes(rows, True)
        self.assertLess(assisted["median_investigation_minutes"], baseline["median_investigation_minutes"])
        self.assertGreaterEqual(assisted["critical_first_three"], baseline["critical_first_three"])
        result = intelligence_experiment()
        self.assertEqual(result["criteria"], {"detection": True, "prioritization": True,
                                               "workload_guardrail": True})


if __name__ == "__main__":
    unittest.main()
