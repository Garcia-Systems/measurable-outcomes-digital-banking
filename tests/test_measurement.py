import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_fcu.measurement import (Criterion, Observation, compare, error_rate, evaluate,
    percentage_improvement, percentile, success_rate, summarize)

def obs(ok=True, latency=100): return Observation('2026-01-01T00:00:00Z','test',ok,latency)

class MeasurementTest(unittest.TestCase):
    def test_rates_and_summary(self):
        rows=[obs(True,100),obs(True,200),obs(False,300),obs(True,400)]
        self.assertEqual(success_rate(rows),75); self.assertEqual(error_rate(rows),25)
        result=summarize(rows)
        self.assertEqual((result.count,result.successes),(4,3))
        self.assertEqual(result.mean_latency_ms,250)
        self.assertEqual(result.p50_latency_ms,200)
        self.assertEqual(result.p95_latency_ms,400)

    def test_nearest_rank_percentile(self):
        self.assertEqual(percentile(range(1,21),95),19)
        self.assertEqual(percentile([9],50),9)
        for values,p in [([],95),([1],0),([1],101)]:
            with self.assertRaises(ValueError): percentile(values,p)

    def test_empty_rates_and_summary_are_rejected(self):
        for operation in (success_rate,error_rate,summarize):
            with self.assertRaises(ValueError): operation([])

    def test_comparisons_and_improvement_direction(self):
        result=compare('success',94,98,'percent')
        self.assertEqual(result.absolute_change,4)
        self.assertAlmostEqual(result.relative_change_pct,4.255319,places=6)
        self.assertAlmostEqual(percentage_improvement(1250,760,True),39.2)
        with self.assertRaises(ValueError): compare('metric',0,1)

    def test_threshold_boundaries_and_invalid_operator(self):
        self.assertTrue(evaluate(99,Criterion('success','>=',99)).passed)
        self.assertFalse(evaluate(1,Criterion('errors','<',1)).passed)
        with self.assertRaises(ValueError): evaluate(1,Criterion('x','!=',2))
