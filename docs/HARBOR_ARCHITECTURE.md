# Harbor FCU laboratory architecture

**Harbor Federal Credit Union (Harbor FCU) is fictional.** Every identity, account, transaction, application, incident, release, telemetry record, and business measurement in this repository is synthetic. The laboratories use local standard-library simulations and contact no financial institution or vendor.

## System map

```text
Synthetic member journey
        |
Digital account-opening application (Harbor-owned)
        |-- ClearVerify REST adapter ---- member identity verification
        |-- HeritageCore SOAP adapter --- core member/account lookup
        `-- NorthstarPay adapter -------- idempotent transfer example
        |
Harbor application + SQLite laboratory datastore
        |
Structured telemetry -> reliability/incident analysis
                     -> delivery/security validation
                     -> analytics and decision support
                     -> evidence-bounded outcome reports
```

## Ownership and roles

- **Digital account-opening application** — Harbor-owned workflow used across member-experience and capstone scenarios.
- **ClearVerify** — fictional REST member-verification provider.
- **HeritageCore** — fictional SOAP core lookup provider.
- **NorthstarPay** — fictional state-changing transfer provider used to teach stable idempotency keys.
- **Harbor adapters** — translate vendor-specific transport and contract results into shared operation outcomes while retaining diagnostic detail.
- **SQLite datastore** — in-memory synthetic fixture for query-plan, query-count, correctness, concurrency, and performance lessons; it is not a production-system replica.
- **Telemetry and outcome fixtures** — deterministic observations reused across reliability, analytics, delivery, and business-communication lessons.

Vendor request success is not member-workflow success. Model performance is not workflow performance. Neither establishes a business outcome without the intervening measurements described in the [metrics reference](METRICS_REFERENCE.md).
