import unittest

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from harbor_fcu.outcomes import (audience_report, classify_statement,
    estimate_business_value, outcome_dataset, success_criteria)


class BusinessImpactTest(unittest.TestCase):
    def test_cross_layer_relationship(self):
        d = outcome_dataset(); before, after = d["baseline"], d["after"]
        self.assertGreater(after["integration_success_pct"], before["integration_success_pct"])
        self.assertGreater(after["completion_pct"], before["completion_pct"])
        self.assertLess(after["error_rate_pct"], before["error_rate_pct"])
        self.assertLess(after["abandonment_pct"], before["abandonment_pct"])

    def test_business_value_labels_and_optional_assumptions(self):
        result = estimate_business_value({"manual_reviews_avoided": 350},
                                         {"minutes_per_review": 8, "labor_cost_per_hour": 30})
        self.assertEqual(set(result), {"MEASURED", "DERIVED", "ASSUMED", "ESTIMATED"})
        self.assertAlmostEqual(result["DERIVED"]["review_hours_avoided"], 46.6666667)
        self.assertAlmostEqual(result["ESTIMATED"]["labor_value_equivalent"], 1400)
        unsupported = estimate_business_value({"manual_reviews_avoided": 350}, {})
        self.assertEqual(unsupported["DERIVED"], {})
        self.assertEqual(unsupported["ESTIMATED"], {})

    def test_audience_reports_share_evidence_but_differ(self):
        reports = {name: audience_report(name) for name in ("engineer", "operations", "executive")}
        self.assertIn("p95 API latency", reports["engineer"])
        self.assertIn("Manual reviews", reports["operations"])
        self.assertIn("percentage points", reports["executive"])
        self.assertEqual(len(set(reports.values())), 3)

    def test_statement_classes_and_nonclaims(self):
        result = classify_statement("completion", 78, 88, "controlled lab", "errors fell")
        self.assertIn("78", result["SUPPORTED"][0])
        self.assertIn("revenue", result["NOT_ESTABLISHED"][0])
        without_downstream = classify_statement("latency", 10, 8, "lab")
        self.assertTrue(without_downstream["POTENTIAL"])

    def test_capstone_criteria_and_guardrail(self):
        d = outcome_dataset()
        self.assertTrue(all(success_criteria(d).values()))
        d["after"]["critical_error_pct"] = 3
        self.assertFalse(success_criteria(d)["Guardrails"])


if __name__ == "__main__":
    unittest.main()
