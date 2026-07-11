# `ogeth_informality_default_parameters.json` — frozen Option A calibration

A single, self-contained parameter file: the OG-ETH FY2024/25 base calibration with
the Option A informality treatment (the "A-2-final" platform) baked in. Load it directly
— no overlay step, no `Calibration` class, no network.

## Use

```python
import json
from ogcore.parameters import Specifications
from ogcore.execute import runner

p = Specifications(baseline=True, output_base="OUT", baseline_dir="OUT")
with open("ogeth_informality_default_parameters.json") as f:
    p.update_specifications(json.load(f))
runner(p, time_path=False)   # steady state; time_path=True for the transition
```

`experiments/optionA/run_static_json.py` does exactly this and is the reproducibility
check.

## What differs from the base `ogeth/ogeth_default_parameters.json`

Six parameters, all on the household/firm tax side (everything else — demographics,
earnings `e`, `chi_n`, macro ratios — is copied verbatim from the base):

| Parameter | Base | This file | Meaning |
|---|---|---|---|
| `labor_income_tax_noncompliance_rate` | zeros | [1,1,1,1,1,0.5,0] | bottom 5 groups pay no income tax; group 6 half; top complies |
| `capital_income_tax_noncompliance_rate` | zeros | [1,1,1,1,1,0.5,0] | same, capital income |
| `income_tax_filer` | ones | ones | (unchanged; informality carried by noncompliance) |
| `etr_params` | 0.03 | 0.1313 | statutory-like average rate on the compliant base |
| `mtrx_params` | 0.20 | 0.35 | statutory top marginal rate on labor |
| `adjustment_factor_for_cit_receipts` | 0.2 | 0.327 | CIT collections factor anchored to 1.7% of GDP |

## Verified

A steady-state solve from this file alone reproduces the A-2-final experiment exactly
(Y, K, L, r, factor to 5 digits; PIT 1.39% and CIT 1.71% of GDP). Revenue matches the
Ethiopian data anchors: PIT 1.4, CIT 1.7, direct 3.1% of GDP (IMF SIP 2025/108; CR 26/20
Table 2b).

## Caveats

- **Exploration artifact**, not a packaged default — it belongs to the paper project
  (`paper/OUTLINE.md`), not to OG-ETH's shipped calibration.
- The **transition path** (`time_path=True`) needs the OG-Core TPI-noncompliance fix
  (branch `fix-tpi-noncompliance-path`); released ogcore 0.16.3 mis-accounts revenue
  along the path. Steady-state runs are unaffected.
- Rebuild with `python experiments/optionA/build_static_json.py` after any change to the
  base JSON or the overlay.
- Revenue ratios use the pre-GDP-rebasing denominator (see METHOD.md).
