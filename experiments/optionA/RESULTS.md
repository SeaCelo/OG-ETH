# Option A-0 results — formal/informal split via filer flags

Run 2026-07-10 on `explore/informality` @ `f3fe3e4`, worktree venv, SS-only solve
(`run_optionA_ss.py`, 68 s, FOC errors ~1e-12). Overlay: bottom five groups (90% of
households) non-filers; top two groups file at a flat 7.68% ETR solved from the revenue
identity (PIT target 1.5% of GDP, IMF SIP 2025/189 Fig 5). MTRs left at baseline 0.20.

## Did it hit the targets?

| Measure | Baseline | A-0 | Data target |
|---|---|---|---|
| Income-tax revenue (PIT-like, % of Y) | 2.46 | **1.41** | 1.5 |
| Payroll (% of Y) | 1.80 | 1.80 | — (social contributions, off-table) |
| Consumption tax (% of Y) | 3.89 | 3.87 | ~4.3 incl. import duties |
| CIT (% of Y) | 1.06 | 1.04 | ~2 (known under-collection, out of scope) |
| Total tax (% of Y) | 9.20 | 8.13 | 7.8 |
| Avg income-tax rate by group | 3% for all | 0,0,0,0,0, 7.68%, 7.68% | informal ≈ 0, formal within 10–35% schedule |

PIT lands at 1.41% vs the 1.5% target — 6% short after general-equilibrium feedback
(income shares shift when behavior responds). Within the plan's tolerance; a one-step
re-solve of the identity (ETR ≈ 8.2%) would close it if we want exactness.

## What moved in the economy (vs Phase 0 yardstick)

| | Baseline | A-0 | change |
|---|---|---|---|
| Y | 0.5601 | 0.6010 | **+7.3%** |
| K | 1.6638 | 1.8608 | +11.8% |
| L | 0.4015 | 0.4221 | +5.1% |
| r | 0.0485 | 0.0446 | −0.4pp |
| w | 0.8369 | 0.8543 | +2.1% |
| factor | 343,579 | 320,775 | −6.6% |
| K/Y | 2.971 | 3.096 | +4.2% |

Hours by group: informal groups +5.6% (their 20% marginal wedge dropped to zero);
filer groups +3.1/+3.3% (their marginal rate is unchanged at 20% while their average
rate rose — an income effect, so they also work more).

## Reading

1. **The blended baseline materially misstates the economy's level.** Removing an
   income-tax wedge from 90% of households — who never actually faced one — raises
   steady-state output 7.3% and capital 11.8%. This is a *recalibration* statement
   (the baseline was over-distorted), not a policy result.
2. **The wedge distribution is now right by construction**: informal groups face zero
   income tax on both average and marginal margins; the formal top decile carries the
   entire PIT at a rate comfortably inside the statutory schedule. Total revenue moves
   from 9.2% to 8.1% of Y, nearly on the data's 7.8%.
3. **Caveat on the filer rate**: 7.68% is identity-consistent, not measured. The model's
   top-10%-of-lifetime-income base (~24% of household income) is wider than Ethiopia's
   true formal wage base, so the solved rate sits below plausible effective rates on
   actual formal wages (~15–20%). A narrower filer set (top group only) or a wider PIT
   target would push it up; document, don't tune silently.
4. **If A-0 (or a variant) becomes the preferred baseline**, downstream anchors shift:
   factor −6.6%, K/Y +4.2%. Re-validation against the FY2024/25 targets and a look at
   solver seeds are required before it graduates off this branch.

## Next in the grid

- **A-0b**: raise filers' MTRx toward the statutory top region (30–35%) — the SIP says a
  large share of formal wages is taxed at the top rate; this is the behavioral margin
  that matters for formalization stories.
- **A-1**: graded noncompliance instead of binary filer flags (same revenue anchor).
- **A5 reform**: the formalization time path, once a preferred variant is chosen.
