import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_fcu.integrations import *
from harbor_fcu.integration_metrics import *

class IntegrationTests(unittest.TestCase):
 def test_success_rate_and_categories(self):
  rows=reliability_sample(); self.assertEqual(success_rate(rows),94); self.assertEqual(error_category_counts(rows)[FailureCategory.TIMEOUT],2)
 def test_nearest_rank_percentiles(self):
  values=list(range(1,101)); self.assertEqual(percentile(values,50),50); self.assertEqual(percentile(values,95),95); self.assertEqual(percentile(values,99),99)
 def test_normalization(self):
  self.assertEqual(normalize_rest(200,{'decision':'rejected'}),FailureCategory.BUSINESS_REJECTION)
  self.assertEqual(normalize_rest(200,{}),FailureCategory.INVALID_RESPONSE)
  self.assertEqual(normalize_soap('Server.Busy',None),FailureCategory.TRANSIENT_ERROR)
 def test_adapters(self):
  self.assertTrue(ClearVerifyAdapter().call('x-1','success').succeeded)
  self.assertEqual(HeritageCoreAdapter().call('x-1','permanent_failure').error_category,FailureCategory.PERMANENT_ERROR)
 def test_retry_and_eventual_success(self):
  rows=execute_with_retries(ClearVerifyAdapter(),'x-1',['temporary_failure','success'],2)
  self.assertEqual(len(rows),2); self.assertEqual(eventual_success_rate(rows),100); self.assertEqual(requests_per_operation(rows),2)
 def test_exhaustion(self):
  rows=execute_with_retries(ClearVerifyAdapter(),'x-1',['timeout','temporary_failure'],2)
  self.assertEqual(retry_exhaustions(rows,2),1)
 def test_permanent_failure_not_retried(self):
  rows=execute_with_retries(ClearVerifyAdapter(),'x-1',['permanent_failure','success'],2); self.assertEqual(len(rows),1)
 def test_idempotent_retry(self):
  pay=NorthstarPaySimulator(); self.assertEqual(pay.transfer('key',10000,True),FailureCategory.TIMEOUT); pay.transfer('key',10000); self.assertEqual(pay.processed,{'key':10000})
 def test_experiment_criteria(self):
  rows=experiment('after'); self.assertEqual(eventual_success_rate(rows),98); self.assertEqual(requests_per_operation(rows),1.06); self.assertTrue(all(evaluate_criteria(rows).values()))

if __name__=='__main__': unittest.main()
