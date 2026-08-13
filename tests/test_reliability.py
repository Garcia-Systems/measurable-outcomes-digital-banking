import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from harbor_fcu.reliability import (
    Alert, AlertWindow, alert_false_positive_rate, compare_reliability,
    detection_duration, endpoint_error_rates, evaluate_alerts,
    evaluate_part4_success, experiment_scenarios, incident_logs,
    mttd, mttr, observed_availability, reconstruct_timeline,
    recovery_duration, reliability_requests, request_success_rate,
    response_incidents,
)


class ReliabilityMeasurementTest(unittest.TestCase):
    def test_request_reliability_and_endpoint_errors(self):
        rows = reliability_requests()
        self.assertEqual(len(rows), 20)
        self.assertEqual(request_success_rate(rows), 85.0)
        self.assertEqual(observed_availability(rows), 85.0)
        rates = endpoint_error_rates(rows)
        self.assertEqual(rates["/balances"], 0.0)
        self.assertAlmostEqual(rates["/verify"], 100 / 6)
        self.assertEqual(rates["/transfers"], 25.0)

    def test_empty_request_population_is_rejected(self):
        with self.assertRaises(ValueError):
            observed_availability([])


class ObservabilityTest(unittest.TestCase):
    def test_correlation_and_chronological_timeline(self):
        events = reconstruct_timeline(incident_logs(), operation_id="transfer-0017")
        self.assertEqual(len(events), 4)
        self.assertTrue(all(event.request_id == "req-transfer-017" for event in events))
        self.assertEqual([event.timestamp for event in events], sorted(event.timestamp for event in events))
        self.assertEqual({event.component for event in events}, {"banking-api", "transfer-adapter", "NorthstarPay"})

    def test_timeline_filters_component_and_incident(self):
        events = reconstruct_timeline(incident_logs(), incident_id="inc-017", component="banking-api")
        self.assertEqual(len(events), 4)


class AlertTest(unittest.TestCase):
    def test_strict_threshold_requires_consecutive_windows(self):
        windows = [AlertWindow(f"2026-02-03T08:{minute:02d}:00Z", rate, True)
                   for minute, rate in enumerate([4, 6, 5, 7, 8, 9])]
        alerts = evaluate_alerts(windows, 5, 3)
        self.assertEqual([alert.timestamp for alert in alerts], ["2026-02-03T08:05:00Z"])

    def test_alert_resets_and_false_positive_rate(self):
        windows = [AlertWindow(f"2026-02-03T09:0{i}:00Z", rate, active)
                   for i, (rate, active) in enumerate([(8, False), (1, False), (9, True)])]
        alerts = evaluate_alerts(windows, 5, 1)
        self.assertEqual(len(alerts), 2)
        self.assertEqual(alert_false_positive_rate(alerts), 50.0)
        self.assertEqual(alert_false_positive_rate([]), 0.0)


class IncidentResponseTest(unittest.TestCase):
    def test_durations_and_aggregate_definitions(self):
        incidents = response_incidents()
        self.assertEqual(detection_duration(incidents[0]), 8)
        self.assertEqual(recovery_duration(incidents[0]), 32)
        self.assertEqual(mttd(incidents), 8)
        self.assertEqual(mttr(incidents), 32)

    def test_experiment_comparison_and_success_criteria(self):
        before, after, before_alerts, after_alerts = experiment_scenarios()
        result = compare_reliability(before, after, before_alerts, after_alerts, 12, 5)
        self.assertEqual(result.before_mttd_minutes, 12)
        self.assertEqual(result.after_mttd_minutes, 4)
        self.assertEqual(result.before_mttr_minutes, 42)
        self.assertEqual(result.after_mttr_minutes, 22)
        self.assertAlmostEqual(result.detection_improvement_pct, 66.6666667)
        self.assertAlmostEqual(result.recovery_improvement_pct, 47.6190476)
        self.assertEqual(result.before_false_positive_rate_pct, 50)
        self.assertEqual(result.after_false_positive_rate_pct, 25)
        self.assertTrue(all(evaluate_part4_success(result).values()))


if __name__ == "__main__":
    unittest.main()
