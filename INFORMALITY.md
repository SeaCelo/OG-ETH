# Informal labor in OG-ETH — assessment and treatment options

*Exploration branch `explore/informality`, July 2026. Base: `calib/single-industry-refresh`
(FY2024/25 baseline, commit `15f424f`). Code citations are to ogcore 0.16.3 (the pinned
version) and to this repo at that commit.*

**Status (2026-07-10): Option A COMPLETE — steady states and transition.** Platform:
graded compliance + statutory 35% MTR, all direct-tax anchors hit
(`experiments/optionA/RESULTS.md`); method note drafted (`experiments/optionA/METHOD.md`);
formalization reform validated in levels and dynamics (+0.64pp of GDP revenue, ~99% of
static gain, transition run under the OG-Core TPI fix branch pending its merge). Option B
specced and blocked on the multi-industry port (`experiments/optionB/SPEC.md`). Option C
remains a scoping item. Upstream: OG-Core PR #1171 (SS diagnostic), TPI-slicing fix PR
in preparation, OG-ETH issue #71 (documentation cleanup).

**Reframing (2026-07-10): this work now targets a development-economics paper** on the
role of informality in an economy and on assessing fiscal/formalization policy in its
presence — see `paper/OUTLINE.md`. Large-scale OLG general equilibrium is the analytical
tool, not the subject; the economics of informality-and-development and the
distributional incidence of policy are the point. It is NOT (for now) a method proposal
to OG-Core; upstream contributions are limited to the bug fixes. References to "graduation
to a feature/ PR" elsewhere in this document should be read through that lens: the
graduation target is the paper's replication package, not an OG-ETH feature PR.

## 0. The question and the short answer

Informality is real economic activity that lacks legal status. Roughly 85% of Ethiopian
employment is informal and something like 37–39% of GDP is produced in the shadow economy.
Can a fiscal OLG model just wish that away?

The short answer: **the model does not wish away the activity — it wishes away the tax
boundary.** Because every macro ratio in OG-ETH (debt/GDP, alpha_T, alpha_G, K/Y, the
`factor` anchor) is calibrated to national-accounts data, and the SNA imputes informal
activity into GDP, the model's output, capital, and labor already *include* the informal
economy. What the model gets wrong is not the amount of activity but **who pays taxes on
it**: OG-ETH currently taxes 100% of model income at low flat "blended" rates, when in
reality a small formal minority pays something close to statutory rates and the informal
majority pays approximately nothing. Informality in this model class is therefore a
**tax-wedge distribution problem and a coverage problem, not a missing-output problem.**

That distinction dictates the fix. We do not need to add output; we need to reallocate the
tax wedge — and OG-Core already ships the machinery to do it (§2.2).

## 1. Ethiopia facts (what we are calibrating to)

| Fact | Value | Source |
|---|---|---|
| Informal employment share | **85.2%** of total employment (2021); 87.4% women, 87.3% youth | ILO Youth Country Brief Ethiopia (2023), ILO harmonized microdata |
| Urban informal sector (narrow, registration-based definition) | 21.8% of urban employed (2022) | ESS Urban Employment/Unemployment Survey 2022 (not independently verified) |
| Shadow economy share of GDP | ~37–39% (MIMIC, model-imputed) | Medina & Schneider (IMF WP 18/17) via aggregators; primary country table not verified |
| Tax revenue / GDP | 12.4% (2014/15) → **7.5%** (2022/23); ~6–8% range in 2023–25 vintages | IFS/TaxDev (2025) |
| Tax potential vs actual | ~17% of GDP potential vs ~8% actual — Ethiopia collects about half its frontier | IMF SIP 2025/189 (stochastic frontier) |
| Compliance component of the decline | ~1.8pp of the ~4.9pp fall not explained by structural change | IFS/TaxDev |
| Program context | ECF 5th review completed Jul 2026; DRM anchored on the Medium-Term Revenue Strategy and VAT Proclamation 1341/2024 (base-broadening + compliance) | IMF press releases |
| GDP coverage of informality | SNA 2008 imputes non-observed activity into GDP; ETH rebasing (in progress) may raise measured GDP substantially, partly by capturing informal/services activity | SNA/NOE manual; ETH-specific NOE methodology **not found** — open item |

Two definitional regimes coexist: the ILO's broad measure (~85%, counts smallholder
agriculture and own-account work) and the ESS urban registration-based measure (~22% of
urban employment). For a national one-sector model the broad measure is the relevant one.

## 2. What OG-Core offers (theory and code entry points)

OG-Core has no vocabulary for informality — the string "informal" appears **zero times** in
the entire upstream repository. But its structure constrains and enables specific
treatments.

### 2.1 Hard structural constraints

- **One wage, one labor market.** The wage `w_t` is a single economy-wide price
  (`ogcore/firm.py:get_w`; theory docs state firms take one `w_t` as given, and market
  clearing sums a single labor pool `L_t = Σ ω λ e n` in `ogcore/aggregates.py:get_L`).
  Households supply one scalar `n_{j,s,t}` with no industry index — nobody chooses a sector
  of employment. **A formal/informal wage gap or a sector-choice margin is not representable
  without extending OG-Core itself** (a second labor-market clearing condition and a new
  state variable).
- **Tax functions cannot vary by ability type.** `etr_params`/`mtrx_params`/`mtry_params`
  are (T, S, #coeffs) — time and age only. Different j groups face different rates only
  through their income levels on a common schedule.
- **Ability is permanent.** `e(j,s)` is deterministic; there is no transition between
  formal and informal status over the life cycle. Group membership at birth is the only
  heterogeneity.
- **Pensions assume universal coverage.** All four pension systems compute benefits from
  every household's full `w·e·n` history (`ogcore/pensions.py`). The dials that vary by j
  are `theta` (replacement rate) and `replacement_rate_adjust[t,j]`.

### 2.2 The machinery that already exists (the key finding)

OG-Core ships three parameters, all indexed **by time t and lifetime-income group j**,
added upstream in OG-Core PR #816 and present in our pinned 0.16.3:

| Parameter | Meaning | OG-ETH today |
|---|---|---|
| `labor_income_tax_noncompliance_rate[t,j]` | share of labor-income taxes owed that go unpaid | all zeros |
| `capital_income_tax_noncompliance_rate[t,j]` | same, capital income | all zeros |
| `income_tax_filer[t,j]` | binary: group j subject to income tax at all (non-filers still pay payroll tax) | all ones |

Mechanics (`ogcore/tax.py:121` and `:193`):
`tau = ETR(income) × (1 − noncompliance) × filer`, applied to **both the average and the
marginal rate**. This is the economically correct behavior: an informal household doesn't
just contribute no revenue, it also faces **no income-tax wedge on its labor-supply and
saving margins**. Setting `income_tax_filer[j] = 0` for a group removes both the revenue
and the distortion, inside the household FOCs (`ogcore/household.py:FOC_labor`,
`FOC_savings`).

Limits of the machinery, verified in code:

- Non-filers **still pay `tau_payroll`** (by design, per the parameter docs). Payroll
  informality must be handled in `tau_payroll` itself — which OG-ETH already does
  (statutory 18% × formal coverage share ≈ 0.03, `taxes.md`).
- The receipt side is already fully flexible: transfers `eta[t,s,j]` and remittances
  `eta_RM[t,s,j]` can vary freely by group, so "informal households receive different
  transfers/remittances" needs no machinery at all.
- **Upstream bug**: `ogcore/SS.py:915-918` tiles `capital_noncompliance_rate_2D` from the
  *labor* noncompliance rate (copy-paste error). The household FOCs and TPI use the correct
  parameters, so the solution is unaffected, but the post-solve `mtry_ss` diagnostic is
  computed with the wrong rate exactly when labor ≠ capital noncompliance — the
  configuration an informality calibration would use. File upstream before relying on
  `mtry_ss` output.

### 2.3 The firm side (multi-industry)

`cit_rate` varies by industry (T×M) and `tau_c` by consumption good (T×I). A zero-CIT,
zero-VAT "informal industry/good" is representable **today** — this is exactly the
committed OG-IDN UN-tutorial demo (§3). But because households do not choose a sector of
employment, an informal industry **cannot exempt the labor income earned in it** from the
personal income tax. Firm-side and household-side informality are separable levers: the
industry split carries the CIT/VAT margin, the filer/noncompliance dials carry the PIT
margin.

## 3. What the sibling models do

Surveyed locally: OG-PHL, OG-ZAF, OG-IDN, OG-BRA, OG-USA (checkout HEADs recorded in the
exploration notes). Confirmed by live search of the PSLmodels GitHub org: **no one has
publicly extended OG-Core or any country calibration with an explicit informal sector**
(July 2026). Zero precedent — whatever we do here is new.

- **OG-BRA** is the only repo whose *committed* calibration names informality: `taxes.md`
  justifies a 12% effective PIT rate (vs 27.5% statutory top) by "the broad exemption and
  large informal sector." Implicit absorption, but documented.
- **OG-IDN** has the richest explicit treatment — a UN-tutorial script
  (`run_og_idn_informal.py`) hand-builds an M=2 formal/informal economy (informal:
  `cit_rate=0`, `tau_c=0`, lower gamma, ~36% of consumption) and runs a "formalization"
  reform. Copied near-verbatim into OG-PHL and OG-BRA example scripts. Always a demo with
  assumed splits, never data-calibrated, and firm-side taxes only.
- **OG-PHL**'s self-employed mixed-income correction to SAM capital shares (the Gollin
  rescale) lives only on an unmerged feature branch. **OG-ETH's `gamma` adjustment in
  `firms.md` is currently the only *shipped* version of that idea in the family.**
- **OG-USA** never mentions informality because its microdata tax functions are estimated
  on near-universal filer coverage — the contrast that defines the problem.
- Cross-family blind spot we inherit: every developing-country repo (including ours) builds
  `e(j,s)` from the US earnings-profile shape, Gini-tilted, with no informal-earnings
  information.

The DSGE literature (IMF WP 22/82 and related SSA papers) explains what the blended-rate
shortcut costs: when the formal sector bears the full statutory burden, tax hikes push
factors and demand toward the informal sector — a first-order response margin in
high-informality countries that a single effective rate cannot produce.

## 4. What OG-ETH currently assumes (audit of `15f424f`)

The FY2024/25 refresh already made informality explicit and quantified in three places:

| Parameter | Value | Informality treatment |
|---|---|---|
| `gamma` = 0.30 | raw ILOSTAT labor share 0.385 rejected as self-employment-biased; Gollin-adjusted labor share 0.60 | explicit, documented (`firms.md`) |
| `tau_payroll` = 0.03 | statutory 18% × formal coverage share of wage bill | explicit, documented (`taxes.md`) |
| `tau_c` = 0.06 | FY2024/25 indirect collections / private consumption ≈ 5.3%, vs 15% statutory VAT; "large informal and subsistence economy" named | explicit, documented (`taxes.md`) |

Where the treatment is missing or inconsistent:

1. **`etr_params` = 3%, `mtrx_params` = `mtry_params` = 20% — undocumented.** Cut from
   22%/25%/31% in commit `c58c972` (Nov 2025) with no rationale in the message and no doc
   update. Presumably informality-adjusted effective rates in the same spirit as payroll,
   but nothing says so. This is both a documentation gap and a substantive one: a flat 3%
   ETR gives *every* household the same blended rate — the formal top under-taxed, the
   informal majority over-taxed, and a 20% marginal wedge applied to subsistence farmers
   who actually face none.
2. **Noncompliance/filer dials present in our JSON and zeroed** — informality absorbed
   into the low flat rates instead of the purpose-built parameters sitting next to them.
3. **`cit_rate` = 0.30 statutory** — defensible (only formal corporations exist in the
   model's CIT base), but revenue consistency should be checked against actual CIT
   collections given `adjustment_factor_for_cit_receipts = 0.2` (also undocumented).
4. **`chi_n` is orphaned**: `ogeth/labor.py` still points at South African QLFS files that
   don't exist and `test_est_chi_n.py` imports a module that was never written. No
   Ethiopian hours data — formal or informal — stands behind labor supply.
5. **`e(j,s)` is the OG-USA profile tilted to Ethiopia's Gini (31.1)** — contains no
   Ethiopian earnings structure. (In-flight WID/NTA work in the main checkout may improve
   this; note WID/NTA are compilations, not ETH informal-sector surveys.)
6. All macro ratios sit on an informal-inclusive GDP denominator, which the docs already
   flag as likely to change with the 2026 rebasing.

## 5. Treatment options

Ordered by cost. These compose — A is the near-term move, B adds the firm-side margin when
the multi-industry port lands, C is the long-run structural answer.

### Option 0 — Status quo, documented (do regardless)

Keep blended effective rates but document the PIT numbers the way `taxes.md` already
documents payroll and VAT: reconcile 3%/20% against actual PIT collections/GDP and the
formal-coverage logic, or correct them. Also document
`adjustment_factor_for_cit_receipts`. Cost: prose. This is the OG-BRA standard and we are
currently below it on PIT.

### Option A — Formal/informal split via the built-in dials (recommended first experiment)

Map lifetime-income groups to formality status. Our `lambdas` =
[0.25, 0.25, 0.20, 0.10, 0.10, 0.09, 0.01]: flagging the bottom five groups as non-filers
makes **90% of households informal — strikingly close to ILO's 85%** (treat the gap as a
calibration choice: e.g., partial noncompliance in group 5 instead of full non-filer
status).

Concretely:
- `income_tax_filer = [0, 0, 0, 0, 0, 1, 1]` (or a softer version using
  `labor_income_tax_noncompliance_rate` for intermediate groups);
- re-anchor the *filers'* ETR/MTR toward statutory-effective formal rates (progressive
  schedule up to 35%), chosen so **aggregate PIT revenue still matches collections** —
  same total revenue, correct wedge distribution;
- optionally make `tau_payroll` = statutory 18% × a *time-varying* coverage path instead
  of a frozen 3%;
- formalization/base-broadening reforms (the ECF DRM agenda, the new VAT law) become
  **time paths of `income_tax_filer[t,j]` and noncompliance rates** — a reform class the
  current calibration literally cannot express, and arguably the most policy-relevant one
  for Ethiopia right now.

Zero model changes; every dial exists in ogcore 0.16.3 and in our JSON.

Honest caveats:
- j indexes *lifetime income*, not sector. The mapping "low lifetime income ≈ informal" is
  a strong but defensible approximation for Ethiopia (informality is overwhelmingly
  smallholder/own-account and low-income). It cannot represent high-income informality
  (successful unregistered traders).
- Single wage still — no compensating-differential or sector-choice margin.
- Changing who faces which wedge **changes the baseline equilibrium** (labor supply and
  savings by group, aggregate L, K, factor). The baseline must be re-validated against the
  FY2024/25 targets after the switch; expect to retune solver guesses.
- The `SS.py` diagnostic bug (§2.2) becomes live the moment labor ≠ capital noncompliance;
  file/patch upstream first or avoid interpreting `mtry_ss`.
- Pension side: with `tau_payroll` coverage-adjusted but benefits universal, there is a
  mismatch; consider `replacement_rate_adjust[t,j]` ≈ 0 for informal groups so uncovered
  households neither contribute nor collect.

### Option B — Informal industry in the multi-industry port (firm-side margin)

When the SAM-based M>1 calibration lands, add a formal/informal dimension: informal
industry with `cit_rate = 0`, informal consumption good with `tau_c = 0` and the formal
good at (or near) the statutory 15% VAT. This endogenizes the demand-reallocation margin
(tax hikes shift consumption toward untaxed informal goods) that the blended `tau_c = 0.06`
cannot produce — the central mechanism in the fiscal-multipliers-with-informality
literature. Combine with Option A for the household side.

Data reality: the IFPRI 2022 Ethiopia SAM disaggregates activities and education-based
labor but has **no formal/informal split** (per available documentation — verify against
the full technical companion). The split would be a documented judgment overlay (e.g.,
agriculture + informal-heavy services shares from ESS/ILO), in the same spirit as the rest
of the multi-industry port: faithful where data allow, documented judgment where they
don't.

### Option C — True dual labor market (upstream extension, long-run)

Sector choice per household, two wages, endogenous formalization margin — the
Rauch/La Porta-Shleifer structure inside an OLG model. Requires new state variables and a
second labor-market clearing condition in OG-Core itself. No precedent anywhere in the
PSLmodels/EAPD family; a research project to coordinate with upstream maintainers, not a
calibration task. Options A+B capture most of the fiscal-policy content (wedge
distribution, base-broadening reforms, consumption reallocation) without it; C adds the
wage-gap and sector-switching margins.

## 6. Validation plan (when we test ideas on this branch)

1. **Revenue decomposition check**: model PIT, VAT, CIT, payroll revenue as % of GDP vs
   actual FY2024/25 collections, instrument by instrument — not just total revenue.
2. **Wedge distribution check**: average and marginal rates by j group vs what we know
   about formal-sector taxation (formal top decile should face ~statutory-effective rates,
   bottom groups ~0).
3. **Baseline re-validation** after any Option A switch: factor, K/Y, aggregate L, r
   against the FY2024/25 targets (same dashboard discipline as the single↔multi
   compatibility work).
4. **A named reform experiment**: a stylized DRM/formalization path (filer share and
   noncompliance improving over 10–15 years, consistent with the Medium-Term Revenue
   Strategy) — the reform this whole exercise exists to price.

## 7. Housekeeping found along the way

- `imf_cr2620.pdf` (repo root, untracked, main checkout) was a failed download — a 480-byte
  Akamai "Access Denied" page. **Fixed 2026-07-10**: replaced with the verified CR 26/20
  (4.5 MB, IMF eLibrary), identity confirmed from the title page. Its Table 2b is the
  revenue anchor for the experiments (§9.2).
- Upstream OG-Core issue to file: `SS.py:915-918` capital-noncompliance tiling bug (§2.2).
- Commit `c58c972`'s PIT rate changes need retroactive documentation (§4.1) regardless of
  which option proceeds.

## 8. Branch organization

- `explore/informality` (this branch, worktree `../OG-ETH.informality`): assessment +
  future experiments. Based on `calib/single-industry-refresh` so experiments run against
  the FY2024/25 baseline; rebase onto `main` after that branch merges.
- Option A experiments stay here until they earn a `feature/` branch.
- Option B belongs to the multi-industry effort (see `MULTI_INDUSTRY_PORTING.md`) and
  should be specified there when that work starts, referencing this document.

## 9. Experiment plan (A → B → C, in turn)

House rules for every phase: experiments live in `experiments/` on this branch; the base
JSON is never touched (overlays / `updated_params` only); model outputs stay out of git
(summary tables go in markdown); every solve gets the import-path preflight; runs are
proposed here and launched by Marcelo. Graduation rule: an experiment that survives its
acceptance checks gets a `feature/` branch and a proper PR; everything else remains
documented exploration.

### Phase 0 — Baseline reference (prerequisite, ~one short run)

1. `uv sync --extra dev` in this worktree; preflight `uv run python -c "import ogeth,
   ogcore; print(ogeth.__file__, ogcore.__file__)"` and assert both resolve here/in this
   venv.
2. Solve the FY2024/25 baseline SS **on this branch, unmodified**, and record the reference
   dashboard in `experiments/baseline.md`: r, K/Y, aggregate L, factor, and — the part the
   existing dashboard lacks — **revenue by instrument as % of GDP** (income tax, payroll,
   tau_c, CIT) to compare against CR 26/20 Table 2b.
3. Acceptance: the baseline solves and the recorded numbers reproduce the calibration
   targets. This is the yardstick every experiment is measured against.

### Phase A — Formal/informal split via filer/noncompliance dials

**A1. Data anchors** (no model work):
- Revenue targets from CR 26/20 Table 2b (FY2024/25 proj., % of GDP): tax revenue 7.8,
  direct taxes 3.5, domestic indirect 2.0, import duties 2.3. Split direct into PIT vs CIT
  from Table 2a (birr) or MoF data — open item.
- Statutory PIT schedule (0–35%), **as amended by the July 2025 Income Tax Proclamation
  amendments effective FY25/26** (CR 26/20 ¶ on the income-tax SB — brackets were adjusted;
  use the new schedule for the formal-sector anchor).
- Formal-worker share: ILO informal employment 85.2% (2021); pension-coverage share already
  embedded in `tau_payroll`. Map to `lambdas` cutoffs.

**A2. Design grid** (run in this order; each is one overlay dict):
- **A-0 "binary"**: `income_tax_filer = [0,0,0,0,0,1,1]` (90% informal); filers' ETR/MTR
  re-anchored to the formal effective schedule such that aggregate PIT revenue ≈ the A1
  anchor. Simplest, sharpest contrast with the blended baseline.
- **A-1 "graded"**: everyone files, but `labor_income_tax_noncompliance_rate` declines in
  j (e.g., 1.0 for the bottom five groups, partial for group 6, ~0 for the top). Same
  revenue anchor. Tests whether the softer parameterization matters for aggregates.
- **A-2 "capital side"**: add `capital_income_tax_noncompliance_rate` > 0 (interest/capital
  income taxation in Ethiopia is thin) — after the upstream `SS.py` fix lands, since this
  is the configuration that trips the `mtry_ss` diagnostic bug (§2.2). Until then, labor ≠
  capital rates are usable for solving but `mtry_ss` output must not be interpreted.
- Parked for a later pass: time-varying `tau_payroll` coverage path;
  `replacement_rate_adjust[t,j] ≈ 0` for informal groups (pension coverage consistency).

**A3. Implementation**: `experiments/optionA/` — a small builder that computes the filers'
rate from the revenue identity (given lambdas, e, and baseline incomes) plus a runner
script applying the overlay via `updated_params`. Non-destructive throughout.

**A4. Validation per variant** (the §6 dashboard, made concrete):
- Revenue decomposition vs Table 2b, instrument by instrument — not just total revenue.
- Wedge distribution: average and marginal rates by j (bottom groups ~0, top groups near
  the formal effective schedule).
- GE drift vs Phase 0: factor, K/Y, L, r — expect movement (the baseline equilibrium
  changes); document what moved, why, and retune `initial_guess_*` if the solver needs it.
- Decision: pick A-0 or A-1 as the preferred informality baseline, with written reasons.

**A5. The reform that motivates all of this**: a stylized DRM/formalization path —
`income_tax_filer[t,j]` and noncompliance improving over 10–15 years consistent with the
Medium-Term Revenue Strategy — run as a TPI reform against the preferred A variant.
Acceptance: sensible revenue path, converging TPI (adjust `nu` if it oscillates), and a
story we can defend about the GE effects of formalization.

### Phase B — Informal industry (blocked on the multi-industry port)

Spec now, execute when `feature/multi-industry-calibration` exists:
- Verify first (open item from §5): does the IFPRI 2022 SAM technical documentation
  really have no formal/informal split? If none, the split is a documented judgment
  overlay (agriculture + informal-heavy services from ESS/ILO shares; MIMIC ~37–39% of
  GDP as a cross-check).
- Structure: informal industry `cit_rate = 0`; informal consumption good `tau_c = 0` with
  the formal good near statutory 15%, jointly reproducing the ~5.3% realized effective
  rate. Start from the OG-IDN demo shape, ETH-calibrated.
- Test: the demand-reallocation margin — a VAT reform through blended-`tau_c` single
  industry vs the B split; the difference in revenue and consumption responses IS the
  finding.
- B composes with A (firm-side and household-side levers are separable); the combined
  configuration is the candidate "informality-aware" calibration.

### Phase C — Dual labor market (scoping only, trigger-gated)

Trigger: only if A+B leave reform questions we care about unanswerable (wage gaps,
endogenous sector switching). Deliverable is a 1–2 page proposal for the OG-Core
maintainers (new state variable, second market clearing, calibration data needs), not code
in this repo. No precedent exists anywhere in the family (§3) — this is a research project
to coordinate upstream, not a calibration task.

### Comparison harness (runs across phases)

One fixed reform (the A5 formalization path, or a simple VAT change) pushed through:
baseline (blended) → A (household split) → A+B (both margins). Same-signs/similar-
magnitudes discipline as the single↔multi compatibility work; divergences between
configurations are the result, not a bug — but each one needs a written mechanism.
