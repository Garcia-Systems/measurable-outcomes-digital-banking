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
        }
        for script,expected in cases.items():
            with self.subTest(script=script):
                result=run(script); self.assertEqual(result.returncode,0,result.stderr); self.assertIn(expected,result.stdout)
    def test_metric_choice(self):
        good=run('scripts/choose_metric.py','--answer','completion_rate')
        bad=run('scripts/choose_metric.py','--answer','latency_p95')
        self.assertEqual(good.returncode,0); self.assertIn('Result: PASS',good.stdout)
        self.assertEqual(bad.returncode,1); self.assertIn('TRY AGAIN',bad.stdout)
