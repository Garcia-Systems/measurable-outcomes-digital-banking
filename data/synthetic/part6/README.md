# Part VI synthetic release observations

`release_history.csv` is a hand-authored, deterministic teaching fixture for the fictional Harbor FCU. Rows represent simulated candidates, not an actual institution, person, account, credential, security event, or deployment. Counts were selected to demonstrate release blocking and the validation-time/known-defect-escape tradeoff; they are not empirical benchmarks.

The executable capstone uses matching aggregate fixture values in `src/harbor_fcu/quality.py`. Keeping this small raw table lets learners inspect the observation schema without creating a CI/CD system. `deployment_result=blocked` is an intended gate decision, not a production deployment.
