import subprocess
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(*args): return subprocess.run([sys.executable,*args],cwd=ROOT,text=True,capture_output=True)
class CliLabsTest(unittest.TestCase):
    def test_chapter_commands_are_deterministic(self):
        cases={
          'scripts/introduce_measurement.py':'Verification success rate: 90.0%',
          'scripts/measure_baseline.py':'p95 latency: 1250 ms',
          'scripts/evaluate_candidate.py':'Overall: FAIL',
          'scripts/run_experiment.py':'Relative change: +11.11%',
          'scripts/measure_completion.py':'Completion rate: 69.1%',
          'scripts/analyze_funnel.py':'Largest drop-off: before verification_completed',
          'scripts/analyze_completion_time.py':'p95 completion: 16.18 minutes',
          'scripts/compare_experience.py':'completion_change_points: PASS',
          'scripts/classify_claims.py':'UNSUPPORTED CAUSAL CLAIM',
          'scripts/measure_api_reliability.py':'Success rate: 94.0%',
          'scripts/analyze_api_latency.py':'Largest p99 contributor: ClearVerify',
          'scripts/simulate_retries.py':'processed transfers=1',
          'scripts/compare_integrations.py':'Normalized REST/SOAP comparison',
          'scripts/run_integration_experiment.py':'permanent-failure safety       PASS',
          'scripts/measure_reliability.py':'/transfers   failures=2 error_rate=25.0%',
          'scripts/explore_observability.py':'component=NorthstarPay',
          'scripts/investigate_incident.py':'diagnosis intentionally withheld',
          'scripts/measure_incident_response.py':'MTTR: 32.0 min',
          'scripts/run_reliability_experiment.py':'Overall: PASS',
        }
        for script,expected in cases.items():
            with self.subTest(script=script):
                result=run(script); self.assertEqual(result.returncode,0,result.stderr); self.assertIn(expected,result.stdout)
    def test_metric_choice(self):
        good=run('scripts/choose_metric.py','--answer','completion_rate')
        bad=run('scripts/choose_metric.py','--answer','latency_p95')
        self.assertEqual(good.returncode,0); self.assertIn('Result: PASS',good.stdout)
        self.assertEqual(bad.returncode,1); self.assertIn('TRY AGAIN',bad.stdout)
