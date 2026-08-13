import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from harbor_fcu.api_metrics import measure_api_requests


class ApiMetricsTest(unittest.TestCase):
    def test_synthetic_baseline(self):
        result = measure_api_requests(ROOT / "data/synthetic/api_requests.csv")
        self.assertEqual(result.request_count, 20)
        self.assertEqual(result.success_rate_pct, 90.0)
        self.assertAlmostEqual(result.mean_latency_ms, 275.25)
        self.assertEqual(result.p95_latency_ms, 476)


if __name__ == "__main__":
    unittest.main()
