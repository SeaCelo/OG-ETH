# Calibrating informality in an OG-Core country model — a portable recipe

*Derived from the OG-ETH Option A work (branch `explore/informality`). This generalizes
that method to any OG-Core country calibration (OG-ZAF, OG-KEN, OG-NGA, OG-IDN, …). It is
the household-side ("Option A") treatment: it makes the personal income tax fall where it
actually falls in a high-informality economy, using machinery already in OG-Core. It
needs no model changes.*

## 0. The idea in one paragraph

Your country's macro calibration rests on national-accounts data, which already imputes
informal activity into GDP. So the model **already contains** the informal economy's
output, capital, and labor. What a standard calibration gets wrong is the **tax
boundary**: applying one blended effective rate to every household spreads the income-tax
burden across an economy where, in reality, a small formal minority pays near-statutory
rates and the informal majority pays almost nothing. Informality here is a
**tax-wedge-distribution and coverage problem, not a missing-output problem** — and OG-Core
can express it directly.

## 1. Prerequisites

- A working single-industry country calibration that **solves to steady state** (your
  `og<xxx>_default_parameters.json` + the country `Calibration` class).
- ogcore **≥ 0.16.x** (the by-group noncompliance/filer parameters were added upstream in
  OG-Core PR #816). Confirm they exist: `labor_income_tax_noncompliance_rate`,
  `capital_income_tax_noncompliance_rate`, `income_tax_filer`.
- Nothing else. This is an overlay on your base calibration; never edit the base file.

## 2. The OG-Core machinery you will use

Three parameters, all indexed by time `t` and lifetime-income group `j`:

| Parameter | Meaning |
|---|---|
| `labor_income_tax_noncompliance_rate[t,j]` | share of labor-income tax **owed** that goes unpaid |
| `capital_income_tax_noncompliance_rate[t,j]` | same, capital income |
| `income_tax_filer[t,j]` | binary: is group `j` subject to income tax at all (non-filers still pay payroll tax) |

They enter as `tau = ETR(income) × (1 − noncompliance) × filer`, applied to **both the
average and the marginal rate** (`ogcore/tax.py`, `ETR_income` and `MTR_income`). That is
the economically correct behavior: an informal household contributes no revenue **and**
faces no income-tax wedge on its labor-supply and saving decisions.

You will also use one firm-side dial:

| Parameter | Meaning |
|---|---|
| `adjustment_factor_for_cit_receipts` | scales the effective corporate tax so CIT revenue matches actual collections; absorbs firm-side informality/exemptions |

**Structural limits to respect (properties of OG-Core, not your country):**
- **One economy-wide wage, no household sector choice.** You cannot represent a
  formal/informal wage gap or sector switching without extending OG-Core. This recipe uses
  *lifetime-income group* as a proxy for formality — a strong but defensible approximation
  where informality is concentrated in low-income, own-account activity.
- **Tax-function parameters cannot vary by `j`** — only the noncompliance/filer dials do.
  Groups differ in tax rate only through income level and these dials.
- **Non-filers still pay payroll tax**, and pensions assume universal coverage. Handle
  payroll informality in `tau_payroll` (statutory rate × formal coverage share) and, if a
  pension system is on, consider `replacement_rate_adjust[t,j] ≈ 0` for informal groups.

## 3. Data to collect for your country

Five inputs. Fill these in; the worked ETH values are in parentheses.

1. **Informal employment share** — ILO "informal employment" (ETH: 85%). Sets how many
   lifetime-income groups are informal.
2. **PIT revenue, % of GDP** — from IMF fiscal tables / Selected Issues Papers / GRD
   (ETH: 1.4%). The revenue anchor for the household side.
3. **CIT revenue, % of GDP** (ETH: 1.7%). The revenue anchor for the firm side.
4. **Statutory top personal income tax rate** (ETH: 35%). The marginal rate compliant
   formal workers face.
5. **Your model's lifetime-income group weights `lambdas`** — already in your base JSON
   (ETH: `[0.25,0.25,0.20,0.10,0.10,0.09,0.01]`, J=7). Used to map the informal share
   onto groups.

(Payroll/pension and consumption-tax informality are usually already handled in
`tau_payroll` and `tau_c` if your base calibration set those to effective, not statutory,
rates — check, and document.)

## 4. The recipe (step by step)

**Step 1 — Baseline reference.** Solve your existing baseline (SS only) and record, from
the solved `SS_vars.pkl`: aggregate `Y`, `K`, `L`, `r`, `factor`, and **revenue by
instrument as a share of Y** (income tax, payroll, CIT, consumption). Also compute
**before-tax income by group** `by_j = Σ_s (income × ω_s × λ_j)`. This is your yardstick
and the base for the revenue identity.

**Step 2 — Choose the compliance vector.** Order groups by lifetime income (they already
are, low `j` → low income). Walk the cumulative population share `Σλ` from the bottom until
it reaches your informal employment share; those groups are informal (noncompliance = 1).
Give the next group up a partial value (a judgment call — ETH used 0.5 for the group
straddling the boundary) and the top group(s) full compliance (0). Set **labor and capital
noncompliance equal** — this also sidesteps the SS diagnostic bug in §6.
*ETH: `[1,1,1,1,1,0.5,0]` — bottom 5 groups (90% of population) informal, close to the 85%
ILO figure.*

**Step 3 — Solve the ETR from the revenue identity.** The compliant base is
`eff_base = Σ_j by_j × (1 − noncompliance_j)`. A flat effective rate that raises the PIT
target is:

```
ETR = PIT_target_share_of_Y × Y / eff_base
```

This is a starting value — behavior will respond. **Iterate once:** apply it, solve, read
realized PIT, and rescale `ETR ← ETR × (PIT_target / PIT_realized)`. One pass closes it to
~1% (ETH: naive 13.3% → converged ~13.1% after the feedback correction).

**Step 4 — Set the marginal rate.** Set `mtrx_params` to your statutory top rate (ETH:
0.35). Compliance scales it per group automatically, so a half-compliant group faces
half the statutory marginal rate and informal groups face zero. This is what gives the
model the "high marginal rates on a narrow formal base discourage formalization" channel.
Leave `mtry_params` (capital) at your base value unless you have a reason to change it.

**Step 5 — Anchor the firm side.** With CIT realized at `X`% of Y under your base
`adjustment_factor_for_cit_receipts`, rescale it: `factor ← factor × (CIT_target / X)`.
(ETH: 0.2 → 0.327 to hit 1.7%.) This carries firm-side informality/exemptions until/unless
you build an explicit informal industry (the multi-industry "Option B", out of scope here).

**Step 6 — Apply, solve, verify.** Put Steps 2–5 into an **overlay dict** and
`update_specifications` it on top of your base (never edit the base file). Solve SS.
Verify:
- **Revenue by instrument** vs your data anchors — PIT and CIT should hit targets; total
  should land near actual tax/GDP.
- **Effective rate by group** — informal groups ≈ 0, formal groups within the statutory
  schedule.
- **GE drift** vs Step 1 — expect output to *rise* (you removed a wedge from the informal
  majority that a blended rate wrongly imposed; ETH: +7.5%). Document what moved and why;
  retune `initial_guess_*` if the solver needs it.

**Step 7 (optional) — Freeze to a static JSON.** If your base JSON is self-contained
(carries `e`, `omega`, `chi_n`, etc.) and your `Calibration` class only sets structural
defaults, you can merge the overlay into a single standalone file that loads with no
overlay step and no network. Verify a solve from the frozen file reproduces the overlay
run exactly. (See `experiments/optionA/build_static_json.py` for the pattern.)

## 5. Running a formalization / revenue-mobilization reform

The payoff experiment. Model formalization as a **time path of the compliance vector**:
noncompliance falling over 5–15 years toward a more-formal target, **statutory rates
unchanged** — this is a base-broadening reform, not a rate change. Run it as a baseline
(your calibrated compliance) vs reform (the improving path) transition (`time_path=True`).
Read the revenue and output paths and the welfare incidence by group and cohort.

ETH result, for calibration of expectations: +0.64pp of GDP permanent revenue, ~99% of
the static-arithmetic gain retained, transitional output cost < 0.7%, no revenue J-curve —
because the newly reached income sits with groups whose *marginal* wedge barely moves.

## 6. Known pitfalls (verified in ogcore 0.16.3)

- **SS diagnostic bug** — `ogcore/SS.py` tiles the capital-noncompliance array from the
  *labor* rate. Harmless to the solution (the FOCs use the right values) but corrupts the
  post-solve `mtry_ss` diagnostic whenever labor ≠ capital noncompliance. **Keep the two
  rates equal (Step 2) and it never bites.** (OG-Core PR to fix in flight.)
- **TPI path bug — this one blocks reforms.** `ogcore/TPI.py` computes path-wide household
  taxes with year-0 compliance/filer values for *every* period. Any **time-varying**
  compliance reform (§5) then produces internally inconsistent transition output:
  households respond, but measured revenue and the debt path use frozen year-0 values.
  **Steady states are unaffected.** Fix branch: `fix-tpi-noncompliance-path` (OG-Core);
  layer it in for transition runs until it merges. Symptom if you forget: reform revenue
  tracks the baseline exactly while labor supply moves — that is the bug, not a result.

## 7. Limitations to state in any write-up

1. Lifetime-income group is a **proxy for formality**, not the same thing — high-income
   informality is not representable.
2. **One wage, no sector choice** — no formal/informal wage gap or switching margin.
3. The partial-compliance group value (Step 2) is a **judgment call** — sensitivity-test
   it; in ETH it was macro-irrelevant (±0.3% of Y).
4. Revenue anchors sit on the **current GDP vintage** — flag any pending rebasing.
5. This is the **household side only**. Firm-side informality is carried by the CIT factor;
   an explicit informal industry needs the multi-industry structure (Option B).

## 8. Reference implementation (OG-ETH)

- Method & results: `experiments/optionA/METHOD.md`, `experiments/optionA/RESULTS.md`.
- Overlay builder (the revenue identity in code): `experiments/optionA/build_overlay.py`.
- SS runner: `experiments/optionA/run_optionA_ss.py`.
- Formalization reform: `experiments/optionA/run_A5_reform.py`.
- Frozen static JSON pattern: `experiments/optionA/build_static_json.py`.
- Structural map of OG-Core's informality entry points: `INFORMALITY.md` §2.
