# TimesheetSeal

**Local-first crew timesheet and hours evidence sealer for field operators.**

Offline. Deterministic. Pay once. Compatible with QuantumGuard CONTRACT-v1, DailySeal, JobSeal, and the Operator Pages suite.

## Why TimesheetSeal?

Field operators lose money when clients dispute crew hours, overtime, or "who was on site that day."  
TimesheetSeal captures a structured daily timesheet (crew members, roles, hours, breaks, overtime, job codes) and seals it into a client-verifiable QuantumGuard evidence bundle.

- No SaaS. No subscription. Runs completely offline after key setup.
- Clients (or their auditors) verify the pack with the free QuantumGuard verifier (`qg verify`).
- Pairs with DailySeal for progress context, JobSeal for job scope, and Chaser for invoicing.
- Deterministic: same inputs → same sealed pack.

## Quick Start

```bash
# Recommended for real Ed25519 signatures
pip install cryptography

python3 src/timesheetseal.py --demo
python3 src/timesheetseal.py --json samples/timesheet-001.json --out sealed-timesheet.json
```

Verify the output with the QuantumGuard CLI (from the quantumguard repo):

```bash
qg verify sealed-timesheet.json
```

Expected verdict: **PASS**.

## What you can sell

| SKU       | Price | Includes                                      |
|-----------|-------|-----------------------------------------------|
| Operator  | $39   | CLI + sample templates + key setup guide + 1-year email support |
| Command   | $129  | + batch mode + CSV/Excel export + reseller rights for client packs |
| Agency    | $349  | + white-label + multi-site key management + design partner onboarding |

Purchase / access: danpennic@gmail.com  
Or use the Operator Pages Stripe checkout flow.

Source remains free under Apache-2.0 OR MIT. Commercial Operator Pack sold separately.

## Stack Fit

- Python CLI (same family as DailySeal, FieldSeal, JobSeal, MediaSeal, SafetySeal)
- Emits QuantumGuard CONTRACT-v1 bundles (Ed25519, deterministic canonical JSON)
- Local key storage (PEM)
- Designed to drop into the Operator Pages field stack
- Ready for future HTML/JS logger and Chaser CSV export

## License

Apache-2.0 OR MIT
