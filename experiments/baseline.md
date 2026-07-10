# Phase 0 — Baseline reference dashboard

Run 2026-07-10 on `explore/informality` @ `0b27c7a` (FY2024/25 baseline, unmodified),
worktree venv (`uv sync --extra dev`), ogcore 0.16.3, via `uv run python
examples/run_og_eth.py` (full baseline + example reform, ~7 min). Preflight: `ogeth` and
`ogcore` both asserted to resolve inside this worktree. Outputs in
`examples/OG-ETH-Example/` (untracked, not committed).

## Steady-state aggregates

| Quantity | Model SS |
|---|---|
| r | 0.0485 |
| r_p | 0.0778 |
| w | 0.8369 |
| factor | 343,579 |
| K/Y | 2.971 |
| L | 0.4015 |
| D/Y | 0.300 (= `debt_ratio_ss` target) |
| K_f/K | 0.099 |
| TR/Y | 0.040 (= `alpha_T`) |
| I_g/Y | 0.050 |

## Revenue by instrument — model vs data

Data: IMF CR 26/20 Table 2b, FY2024/25 projections, % of GDP. Model: SS shares of Y.
Bookkeeping note: `frac_tax_payroll = 0`, so the entire income+payroll block is reported
as `iit_revenue` (the `tau_payroll = 0.03` revenue is inside it); pension outlays are 0,
so payroll here is a pure tax.

| Instrument | Model (% of Y) | Data (% of GDP) | Notes |
|---|---|---|---|
| Income + payroll taxes | 4.26 | — | flat ETR 3% + payroll 3% on labor income |
| Business (CIT) | 1.06 | — | cit 30% × `adjustment_factor_for_cit_receipts` 0.2 |
| **Direct total** | **5.32** | **3.5** | model over-collects ~1.8pp |
| Consumption (tau_c) | 3.89 | 4.3 (indirect incl. import duties) | taxes.md targeted this total; model slightly under |
| **Total tax revenue** | **9.20** | **7.8** | model over-collects ~1.4pp overall |

## Reading for the experiments

1. The baseline **over-collects direct taxes by ~1.8pp of GDP** relative to CR 26/20.
   The Option A revenue identity should anchor to the data (3.5% direct, split PIT/CIT —
   split still to be sourced from Table 2a / MoF), not to the current model level; some of
   Phase A's re-anchoring will therefore also *correct* the baseline's direct-tax level,
   not just redistribute it.
2. Consumption-tax revenue (3.89% vs 4.3%) is close; the blended `tau_c = 0.06` behaves
   as documented. This is the margin Phase B decomposes, not a Phase A concern.
3. Pension outlays are zero and payroll is a pure tax — the §5 Option A caveat about
   benefit-coverage mismatch is moot in the current configuration (nothing to mismatch)
   until a pension system is turned on.
4. These numbers are the drift reference for A4: factor 343,579, K/Y 2.971, L 0.4015,
   r 0.0485. Expect movement when the wedge distribution changes; document what and why.
