import unittest

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from harbor_fcu.quality import (CANDIDATES, RELEASE_HISTORY, SECURITY_CASES, SYNTHETIC_SECRET,
    defect_metrics, delivery_experiment, prohibited_exposures, rate, regression_experiment,
    release_gate, safe_log, security_validation, test_metrics as measure_tests,
    transfer_allowed, unsafe_log)


class QualityDeliveryTest(unittest.TestCase):
    def test_test_measurement_and_regression_detection(self):
        self.assertAlmostEqual(measure_tests([True, True, False])["pass_rate"], 200 / 3)
        self.assertTrue(regression_experiment(True)["regression_detected"])
        self.assertFalse(regression_experiment(False)["regression_detected"])

    def test_rate_rejects_impossible_counts(self):
        with self.assertRaises(ValueError):
            rate(2, 1)

    def test_defect_rates_and_escape_type(self):
        result = defect_metrics(RELEASE_HISTORY)
        self.assertEqual((result["known"], result["detected_pre_release"], result["escaped"]), (12, 9, 3))
        self.assertEqual(result["detection_rate"], 75.0)
        self.assertEqual(result["escape_rate"], 25.0)
        self.assertEqual(result["escaped_by_type"]["logging"], 3)

    def test_input_and_authorization_fixtures(self):
        for case in SECURITY_CASES:
            with self.subTest(case=case["name"]):
                self.assertEqual(transfer_allowed(case), case["expected"])

    def test_sensitive_log_detection_and_omission(self):
        payload = {"request_id": "req-7", "operation": "transfer", "token": SYNTHETIC_SECRET}
        self.assertEqual(prohibited_exposures(unsafe_log(payload), [SYNTHETIC_SECRET]), [SYNTHETIC_SECRET])
        output = safe_log(payload)
        self.assertEqual(prohibited_exposures(output, [SYNTHETIC_SECRET]), [])
        self.assertIn("request_id=req-7", output)

    def test_security_summary_preserves_valid_guardrail(self):
        result = security_validation()
        self.assertEqual(result["cases_passed"], result["cases_tested"])
        self.assertEqual(result["accepted_incorrectly"], 0)
        self.assertEqual(result["safe_exposures_detected"], 0)

    def test_release_gate_accepts_valid_and_rejects_invalid(self):
        self.assertTrue(release_gate(CANDIDATES["valid"])["ready"])
        rejected = release_gate(CANDIDATES["invalid"])
        self.assertFalse(rejected["ready"])
        self.assertFalse(rejected["checks"]["security"])

    def test_before_after_delivery_experiment(self):
        result = delivery_experiment()
        self.assertTrue(result["success"])
        self.assertGreater(result["before"]["escape_rate"], result["after"]["escape_rate"])
        self.assertGreater(result["after"]["duration_seconds"], result["before"]["duration_seconds"])
        self.assertEqual(result["after"]["invalid_blocked"], result["after"]["invalid_total"])


if __name__ == "__main__":
    unittest.main()
