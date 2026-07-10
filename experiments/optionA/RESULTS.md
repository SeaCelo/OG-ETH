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

## A-0b — statutory-like marginal rate on filers (run 2026-07-10, 50 s, FOC ~1e-12)

Same as A-0 except `mtrx_params` 0.20 → 0.35 for labor income (filers only, since the
filer flag zeroes the MTR for everyone else). Average rate (7.68%) and revenue identity
unchanged by construction; `mtry` left at 0.20.

| | Baseline | A-0 (MTR 20%) | A-0b (MTR 35%) |
|---|---|---|---|
| Y | 0.5601 | 0.6010 | 0.5929 |
| L | 0.4015 | 0.4221 | 0.4162 |
| K | 1.6638 | 1.8608 | 1.8369 |
| PIT revenue (% of Y) | 2.46 | 1.41 | 1.35 |
| Total tax (% of Y) | 9.20 | 8.13 | 8.06 |
| Formal groups' hours vs baseline | — | +3.1 / +3.3% | **−3.3 / −3.1%** |
| Informal groups' hours vs baseline | — | +5.6% | +5.7% |

Reading:
1. **The marginal rate alone swings formal labor supply by ~6.4pp** (from +3% to −3%
   vs baseline) with the average tax bill held fixed — this is the "high marginal rates
   on a narrow formal base discourage work/formalization" mechanism from IMF SIP
   2025/189 ¶14, now live in the model.
2. **Behavioral revenue erosion appears**: PIT lands at 1.35% of Y (vs 1.41 in A-0,
   target 1.5) because formal earnings shrink under the higher wedge. Restoring the
   target under MTR 35% requires ETR ≈ 8.5% — the erosion itself is a finding (a
   ~4% base loss from the marginal-rate increase).
3. A-0b is the more faithful representation of Ethiopia's actual PIT design (top
   statutory rate binds at modest formal incomes) and gives the reform experiments the
   margin they need. Leading candidate for preferred variant, pending A-1.

## A-1 — graded noncompliance (run 2026-07-10, 47 s, FOC ~1e-12)

Everyone files; noncompliance by group = [1,1,1,1,1,0.5,0] on both labor and capital
income (equal rates, so the upstream SS.py diagnostic bug is moot). ETR solved on the
compliance-weighted base: 13.32%. MTR left at baseline 0.20 to isolate the compliance
parameterization.

| | Baseline | A-0 | A-0b | A-1 |
|---|---|---|---|---|
| Y | 0.5601 | 0.6010 | 0.5929 | **0.6064** |
| L | 0.4015 | 0.4221 | 0.4162 | 0.4253 |
| K | 1.6638 | 1.8608 | 1.8369 | 1.8832 |
| PIT revenue (% of Y) | 2.46 | 1.41 | 1.35 | **1.46** |
| Total tax (% of Y) | 9.20 | 8.13 | 8.06 | 8.16 |

A-1's effective average rates by group come out 0 / 0 / 0 / 0 / 0 / 6.7% / 13.3% — a
smooth progressive schedule emerges from one statutory rate times compliance, and the
solved 13.3% is much closer to plausible effective rates on real formal earners than
A-0's 7.7%. Revenue lands nearest the target (1.46 vs 1.5). All groups' hours rise vs
baseline (informal: wedge removed; group 6: *halved* marginal wedge via evasion — hiding
half your income halves your effective marginal rate, which is the actual economics of
evasion; group 7: pure income effect).

## Preferred-variant decision

- **A-1's compliance structure wins for the reform program**: the A5 formalization
  reform IS a compliance path — noncompliance rates falling over 10–15 years — which is
  continuous and natural in A-1, but lumpy in A-0 (whole groups flip filer status at
  once). It also fits the revenue target best and yields realistic effective rates.
- **A-0b's marginal-rate realism should be added to it**: A-1 at MTR 0.20 understates
  the wedge on fully compliant formal earners (statutory top rate is 35% and binds at
  modest formal incomes).
- **Proposed preferred variant "A-2" = graded compliance + `mtrx_params` 0.35**, with
  the ETR re-solved on the compliance-weighted base. To be built and validated next,
  then used as the platform for the A5 formalization reform.

## A-2 — the preferred variant, validated (run 2026-07-10, 49 s, FOC ~1e-12)

Graded compliance [1,1,1,1,1,0.5,0] + statutory 35% MTR on labor income, ETR 13.32%.

| | Baseline | A-2 |
|---|---|---|
| Y | 0.5601 | 0.6021 (+7.5%) |
| L | 0.4015 | 0.4222 (+5.2%) |
| K | 1.6638 | 1.8705 (+12.4%) |
| PIT revenue (% of Y) | 2.46 | 1.42 (target 1.5) |
| Total tax (% of Y) | 9.20 | 8.12 (data 7.8) |
| Avg income-tax rate by j | 3% flat | 0×5 / 6.7% / 13.3% |
| Hours vs baseline by j | — | +5.6–5.8% informal / +3.4% semi / +0.3% top |

The hours pattern is the economics working: the informal majority gains from losing a
wedge it never really faced; the semi-compliant group faces 17.5% at the margin (35% ×
its 50% visibility) — slightly *below* the old 20%, plus an income effect, so it works
more; the fully compliant top 1% faces the full 35% marginal wedge and comes out
essentially flat (substitution and income effects offsetting). PIT lands 5% below
target from the same behavioral erosion A-0b showed; ETR ≈ 14.1% would close it —
recorded as a refinement option, not applied.

**Decision: A-2 is the Option A platform.** The A5 formalization reform runs on it.
