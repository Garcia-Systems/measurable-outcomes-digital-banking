import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_fcu.measurement import evaluate_measurement,load_observations,summarize
from harbor_fcu.scenarios import BASELINE,FAST_CANDIDATE,RELIABLE_CANDIDATE,SUCCESS_CRITERIA

class Part1ScenarioTest(unittest.TestCase):
    def test_baseline_is_derived_from_observations(self):
        m=summarize(load_observations(BASELINE))
        self.assertEqual((m.count,m.success_rate_pct,m.error_rate_pct),(20,90,10))
        self.assertEqual((m.p50_latency_ms,m.p95_latency_ms),(640,1250))

    def test_fast_candidate_fails_complete_contract(self):
        results=evaluate_measurement(summarize(load_observations(FAST_CANDIDATE)),SUCCESS_CRITERIA)
        self.assertEqual([r.passed for r in results],[True,False,False])

    def test_reliable_after_window(self):
        m=summarize(load_observations(RELIABLE_CANDIDATE))
        self.assertEqual(m.success_rate_pct,100)
        self.assertEqual(m.p95_latency_ms,760)
