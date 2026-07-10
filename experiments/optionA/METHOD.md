# Calibrating informality in OG-ETH — method note (draft for the docs chapter)

*Draft 2026-07-10, branch `explore/informality`. This is the write-up that would
accompany a `feature/` PR; it condenses INFORMALITY.md and RESULTS.md into the method
as adopted.*

## Why

About 85% of Ethiopian employment is informal (ILO, 2021) and roughly 37% of GDP is
produced outside the recorded economy (MIMIC estimates). Because OG-ETH's macro
calibration rests on national-accounts data — which imputes informal activity into GDP
— the model already *contains* the informal economy's output, capital, and labor. What
the previous calibration missed is the tax boundary: it applied one blended flat rate
(ETR 3%, MTR 20%) to every household, spreading Ethiopia's income-tax burden over an
economy where, in reality, a small formal minority pays close to statutory rates and
the informal majority pays nothing. That misstates who faces which incentives, and it
cannot express the reform Ethiopia is actually pursuing (base-broadening under the
Medium-Term Revenue Strategy), which changes *who is taxed*, not the rates.

## How

OG-Core 0.16.3 ships the needed machinery (added upstream in PR #816):
`labor/capital_income_tax_noncompliance_rate[t,j]` and `income_tax_filer[t,j]`, which
scale both average and marginal income-tax rates by lifetime-income group. We use the
noncompliance rates, graded by group:

- **Compliance vector**: noncompliance = [1, 1, 1, 1, 1, 0.5, 0] across the seven
  lifetime-income groups (population weights 25/25/20/10/10/9/1%). The bottom five
  groups (90% of households; ILO measures 85% informal employment) pay none of what
  they owe; group six — partly visible high earners — pays half; the top 1% complies
  fully. Labor and capital rates are set equal.
- **Statutory-like ETR = 13.13%**, solved from the revenue identity: applied to the
  compliance-weighted income base, it reproduces PIT collections of 1.4% of GDP
  (IMF SIP 2025/108 ¶9, avg FY2021/22–2023/24), including a measured ~6% behavioral
  feedback correction.
- **MTR on labor = 35%** — the statutory top rate, which binds at modest formal
  incomes (SIP ¶14). Compliance scales it per group, so the semi-visible group faces
  17.5% at the margin and informal groups face zero.
- **CIT collections factor = 0.327** (`adjustment_factor_for_cit_receipts`), solved so
  business-tax revenue hits CIT collections of 1.7% of GDP (same source). The firm
  side's informality lives in this factor and in `c_corp_share_of_assets` (0.55) until
  a multi-industry informal sector exists — at which point it must migrate into the
  industry structure to avoid double-counting.
- Unchanged: `tau_payroll` = 0.03 (statutory 18% × formal pension coverage) and
  `tau_c` = 0.06 (collections-based), both already informality-adjusted in the base
  calibration and documented in taxes.md.

## What it delivers

| Instrument (% of GDP) | Model | Data (SIP/CR 26/20) |
|---|---|---|
| PIT | 1.39 | 1.4 |
| CIT | 1.71 | 1.7 |
| PIT+CIT | 3.10 | 3.1 |
| Effective avg rate by group | 0×5 / 6.6 / 13.1% | informal ≈ 0; formal within 10–35% schedule |

Relative to the blended calibration, steady-state output is ~7% higher — the blended
rates imposed a work/saving distortion on 90% of households that Ethiopia's actual tax
system does not impose. Group-level results: informal households supply ~6% more labor;
the semi-visible group slightly more; the fully compliant top is nearly unchanged.

**The reform this enables**: formalization as a time path of compliance. The long-run
(steady-state) experiment — compliance permanently at [1,1,1,1,.9,.25,0] — raises PIT
by **+0.64pp of GDP, retaining ~99% of the static-arithmetic gain**, at a long-run
output cost of −0.7%. Compliance-led revenue mobilization is close to non-distortionary
in this model because the newly reached income belongs mostly to groups whose marginal
wedge barely changes. Contrast A-0b: raising the *marginal rate* swings formal labor
supply by ~6pp — rate increases and base broadening are very different animals, and the
calibration now distinguishes them.

## Limitations (stated, not hidden)

1. **j is lifetime income, not sector.** Low lifetime income ≈ informal is a strong but
   defensible approximation for Ethiopia; high-income informality is not representable.
2. **One wage, no sector choice** — no formal/informal wage gap or switching margin
   (OG-Core extension; see INFORMALITY.md Option C).
3. **Group-6 grading (0.5) is a judgment call** — shown macro-irrelevant (±0.3% of Y)
   under re-anchored ETRs; it moves only the required statutory-like rate (12–16%).
4. **Transition paths are blocked** by an upstream OG-Core bug (TPI applies year-0
   compliance/filer values to the whole path's revenue accounting; fix PR in review).
   All steady-state results are unaffected. Rerun A5's transition when it merges.
5. **Anchors predate the GDP rebasing** (~2026, +20–40% nominal GDP expected): every
   revenue/GDP target shrinks mechanically on the new denominator; re-anchor then.
6. Payroll/property taxes (~0.4% of GDP within the fiscal table's "direct taxes") are
   not separately modeled; the model's payroll instrument represents pension
   contributions, which sit outside GFS tax revenue.

## Provenance

- Ethiopia facts and modeling options: `INFORMALITY.md` (root of this branch).
- Experiment record with all variants: `experiments/optionA/RESULTS.md`.
- Reproducibility: `experiments/optionA/build_overlay.py` (computes every derived
  parameter from stated targets) + `run_optionA_ss.py` (applies overlays to the
  untouched base JSON).
- Revenue anchors: IMF SIP 2025/108 ¶9 (text-stated); IMF CR 26/20 Table 2b; UNU-WIDER
  GRD as historical corroboration only (Ethiopia split ends 2007).
- Upstream issues found by this work: OG-ETH #71 (undocumented rates, orphaned chi_n);
  OG-Core SS.py mtry_ss diagnostic bug; OG-Core TPI year-0 compliance bug (PR pending).
