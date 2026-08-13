# Synthetic data catalog

All data in this directory is invented for the fictional Harbor Federal Credit
Union teaching environment. `part1/` contains the implemented verification
baseline and experiment windows; see its README for schema and provenance.
`api_requests.csv` is the original 20-observation synthetic balance-API fixture.
No fixture contains member identifiers or real financial data. Future generators
must use deterministic seeds and document their schemas here.

Part III observations are generated in memory from explicit scenario tables in
`src/harbor_fcu/integrations.py`. Fixed operation IDs and UTC timestamps make the
records reproducible and inspectable; no vendor data or network response is used.

Part IV operational requests, structured logs, alert windows, and incident records
are generated from explicit fixtures in `src/harbor_fcu/reliability.py`. They use
UTC timestamps and opaque request/operation identifiers. They contain no names,
account numbers, credentials, balances, request bodies, or production telemetry.
