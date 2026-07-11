# Paper project — informality and the fiscal state in developing economies

*Working home: branch `explore/informality`. Reframed 2026-07-10: this is a
development-economics paper on the role of informality in an economy and on assessing
fiscal/formalization policy in its presence. Large-scale OLG general equilibrium is the
**analytical tool**, not the subject. It is NOT a method proposal to OG-Core; upstream
contributions are bug fixes only. The experiments and method notes elsewhere on this
branch are the paper's raw material.*

## Research question and contribution

**Central question (positive):** What does informality do to the structure of a
developing economy and its fiscal state — to who bears the tax burden, to the incentives
households actually face, to the size of the taxable base, and to the government's room
for maneuver? The informal sector is real economic activity that lacks legal status; a
model that cannot see the formal/informal boundary cannot correctly describe the economy
it is meant to represent.

**Central question (normative/policy):** When informality is taken seriously, what do
the fiscal policies developing countries are actually pursuing — domestic revenue
mobilization, base-broadening, formalization drives — deliver, what do they cost, and
**who bears that cost across the income distribution and across generations?** The paper
positions dynamic GE with informality as a *policy-assessment instrument* for finance
ministries and development institutions, one that yields distributional incidence, not
just an aggregate revenue number.

**Ethiopia is the worked case, not the point.** It is a stress test — ~85% informal
employment, a tax/GDP ratio that has *fallen* to ~7.5% while the economy grew, and a
live IMF-program revenue-mobilization agenda — chosen because informality dominates the
economic question there. The apparatus is built to travel to other developing economies
(a second country is planned) so the findings speak to informality *in economies*,
plural, not to one calibration.

**Claimed contributions (economics first, method as enabler):**

1. **A positive account of how informality reshapes the fiscal picture of a developing
   economy.** Drawing the tax boundary where it actually falls — a small formal minority
   bearing near-statutory rates, an informal majority facing none — is not a refinement;
   it changes the model's description of the economy. Marginal incentives, the incidence
   of taxation, and measured output all move materially (~7.5% higher steady-state output
   once 90% of households are freed of a wedge the blended representation wrongly imposes
   on them). The standard practice of burying informality in a single blended effective
   rate is shown to *mis-describe the economy*, not merely to lose precision.

2. **Policy assessment: what formalization and revenue-mobilization actually buy, and for
   whom.** A stylized compliance/formalization reform (the kind an NMTRS or IMF program
   pursues) delivers ~+0.64pp of GDP in permanent revenue, retaining ~99% of the static
   arithmetic, with a transitional output cost under 0.7% and no revenue J-curve — because
   the newly reached income sits with households whose *marginal* wedge barely moves.
   Critically, the same model distinguishes base-broadening from rate increases, which a
   blended calibration cannot: raising marginal rates swings formal labor supply by ~6pp
   where broadening the base does not. This is a policy-relevant distinction current
   practice erases. **[Distributional incidence — CEV by income group and cohort — is the
   headline result still to be computed; see §8.]**

3. **A generalizable method and calibration recipe** enabling the above: a taxonomy of
   informality treatments for OLG-GE models ordered by structural demand — (0) blended
   effective rates (universal current practice), (A) household compliance heterogeneity,
   (B) informal-industry firm side, (C) dual labor market with sector choice — and a
   replicable recipe anchoring group-level compliance to revenue-by-instrument data (IMF
   fiscal tables) and informal-employment shares (ILO). First implementation of an
   explicit informal treatment in this model family (verified zero precedent across
   PSLmodels/EAPD, July 2026). Method is the apparatus; the economics above is the point.

## Section map (existing assets → paper sections)

Ordered so the economic-development question leads and the model apparatus serves it.

| Paper section | Source material | Status |
|---|---|---|
| 1. Introduction — informality and the fiscal state in development | INFORMALITY.md §0–1 (Ethiopia facts); the fallen tax/GDP ratio; the DRM policy agenda | note form; needs development-framing prose |
| 2. Informality in development & how models have (not) handled it | references.md: Medina & Schneider, Elgin et al., La Porta-Shleifer (development view); IMF WP 22/82, SSA DSGE, NBER 27429 (modeling); IMF Global Informal Workforce | sources collected; prose not written |
| 3. What informality does to the fiscal picture (positive core) | RESULTS.md steady-state tables + INFORMALITY.md §2 structural map, read as economics not code | computed; needs economic write-up |
| 4. Assessing policy under informality (normative core) | RESULTS.md A5 endpoint + transition; base-broadening vs rate-hike contrast | computed |
| 5. Distributional incidence — who bears formalization | — | **NOT DONE — the headline** |
| 6. Method & calibration (the tool) | METHOD.md + build_overlay.py; taxonomy 0/A/B/C; structural conditions each needs | drafted |
| 7. The firm side and general-equilibrium reallocation (Option B) | experiments/optionB/SPEC.md; VAT-reform demand shift | specced, blocked on multi-industry port |
| 8. What current practice gets wrong | sibling-repo survey (BRA/PHL/ZAF/IDN/USA); blended-rate critique | findings collected |
| 9. Generalizability / second country | (planned run) | not started |
| Appendix A. Calibration detail & reproducibility | METHOD.md, builders, anchors | done |
| Appendix B. The machinery had never been exercised | the two upstream OG-Core bugs as evidence | documented |

## Work plan (sequenced)

1. **Distributional incidence module** (the headline result; unblocked, next substantive
   step): consumption-equivalent variation by lifetime-income group and by birth cohort
   for the formalization reform — steady-state and, now that the TPI fix runs,
   transitional cohorts. Turns "output dips 0.6%" into "who gains, who pays, across the
   income distribution and across generations" — the paper's central normative payoff and
   what makes this a development/policy paper rather than a methods note.
2. **Robustness battery** (unblocked): Frisch elasticity, sigma, informality boundary
   (85 vs 90%), e-matrix Gini concept (interacts with OG-ETH issue #33) — how sensitive
   the economic and welfare conclusions are to the informality assumptions.
3. **Option B execution** — *dependency: the multi-industry port* (separate work,
   MULTI_INDUSTRY_PORTING.md). Then A+B combined and the VAT-reform experiment (demand
   reallocation toward untaxed goods) — this is where informality's effect on the
   *structure* of the economy (not just tax collection) shows up.
4. **Second country** for generality (PHL or ZAF — same machinery, sibling repos already
   surveyed) — so the claims are about informality in developing economies, not one case.
   Decide scope after B.
5. Prose drafting, economics-first order: 3 → 4 → 5 → 1(intro) → 2 → 6 → 7 → 8 → 9.

## House rules for the paper phase

- Everything stays on `explore/informality` (or children); still no upstream OG-Core
  method proposal — the OG-Core PRs we file are bug fixes only, cited as findings.
- Exploration mode continues (methods over precision) until results freeze for the
  draft; then one reproducibility pass re-runs everything on a single pinned ogcore.
- Numbers in the paper regenerate from committed builders/runners — no hand-typed
  results.
- All revenue ratios carry the GDP-rebasing caveat (pre-rebase denominator).
