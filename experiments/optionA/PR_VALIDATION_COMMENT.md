# Draft comment for the OG-Core TPI-noncompliance PR (paste when the PR is open)

---

I validated this fix end-to-end with a full country calibration (OG-ETH, Ethiopia),
which is where the bug originally surfaced.

The experiment: a base-broadening reform in which income-tax noncompliance rates fall
linearly over five years (informality/compliance calibration by lifetime-income group)
while statutory rates stay fixed. This is exactly the time-varying use of
`labor/capital_income_tax_noncompliance_rate` these parameters were designed for.

On the released code, household behavior responded to the reform but revenue never
did — the transition path applied year-0 noncompliance to all periods, so measured
collections tracked only the shrinking base and the reform looked revenue-*negative*.
On this branch, the same run produces internally consistent results: revenue climbs in
step with the compliance ramp and settles at its new steady-state level.

Macro results from the OG-ETH run on this branch (reform vs its own baseline):

| Year of transition | 1 | 3 | 5 (ramp end) | 12 |
|---|---|---|---|---|
| Income+payroll revenue, % of GDP (baseline) | 3.20 | 3.20 | 3.21 | 3.23 |
| Income+payroll revenue, % of GDP (reform) | 3.33 | 3.59 | 3.84 | 3.87 |
| Total tax revenue, % change vs baseline | +2.3 | +4.2 | +6.7 | +6.6 |
| GDP, % change vs baseline | +0.1 | −0.3 | −0.6 | −0.4 |
| Labor, % change vs baseline | +0.1 | −0.3 | −0.7 | −0.5 |
| Capital, % change vs baseline | +0.1 | −0.5 | −0.6 | −0.5 |

The revenue path now matches the model's own steady-state endpoint for the same
reform (+0.64pp of GDP), computed independently of the transition code — path and
endpoint agree, which they structurally could not before this fix. Both TPI legs
converged with default damping.

---

*Posting note: numbers come from `explore/informality` in OG-ETH, commit `6558a5d`
(experiments/optionA/RESULTS.md, "A5 — formalization transition"), run with ogcore
layered from commit `2e0bdde11`.*
