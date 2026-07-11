# Paper project — informality in large-scale OLG fiscal models

*Working home: branch `explore/informality`. Reframed 2026-07-10: this work targets an
academic paper, NOT (for now) a method proposal to OG-Core. The experiments and method
notes elsewhere on this branch are the paper's raw material.*

## Research question and contribution

**Question:** How should informal economic activity be represented in large-scale
overlapping-generations fiscal models calibrated to developing countries, and what does
getting it wrong (or right) cost — in calibration accuracy, in revenue forecasts, and in
the welfare/output consequences of formalization policy?

**Claimed contributions:**
1. **A taxonomy of informality treatments** for OG-class models, ordered by structural
   demands: (0) implicit absorption into blended effective rates — the current universal
   practice; (A) household-side compliance heterogeneity using group-varying
   noncompliance/filer parameters; (B) firm-side informal industry (zero CIT/VAT sector);
   (C) dual labor market with sector choice. With the structural conditions each requires
   (single wage, no household-industry link, etc.).
2. **First implementation** of (A) — and, pending the multi-industry port, (A)+(B) — in
   the OG-Core model family (verified: zero precedent across PSLmodels/EAPD repos and
   public search, July 2026).
3. **A replicable calibration recipe for low-income countries**: anchor group-level
   compliance to revenue-by-instrument data (IMF fiscal tables) + informal employment
   shares (ILO), solving statutory-like rates from a revenue identity. Ethiopia as the
   worked case.
4. **Cost estimates** (the "what informality costs" results):
   - *Mis-calibration cost*: blended effective rates overstate distortions on 90% of
     households — steady-state output is ~7.5% higher once the tax boundary is drawn
     correctly; the wedge distribution and marginal incentives are qualitatively wrong
     in the blended baseline.
   - *Policy mis-pricing*: base-broadening vs rate increases are indistinguishable in a
     blended calibration but behave completely differently once informality is explicit
     (+0.64pp GDP revenue at ~99% static retention vs ~6pp formal labor-supply swings
     from marginal-rate changes).
   - *Formalization costs*: transition path — revenue arrives in step with compliance
     (no J-curve), output dips ≤0.6% and recovers.
   - *Welfare incidence*: *TO BE COMPUTED* — consumption-equivalent variation by
     lifetime-income group and cohort for the formalization reform (who pays for
     formalization?). This is the biggest missing piece for the paper.

## Section map (existing assets → paper sections)

| Paper section | Source material | Status |
|---|---|---|
| 1. Introduction & motivation | INFORMALITY.md §0–1 (Ethiopia facts, tax-boundary framing) | drafted in note form |
| 2. Literature | web-research findings: Medina & Schneider; IMF WP 22/82; SSA DSGE-informality; NBER 27429; IMF Global Informal Workforce; DIGNAR; La Porta-Shleifer | sources collected (paper/references.md); prose not written |
| 3. Model & the informality problem | INFORMALITY.md §2 (structural map: what OG models can/cannot express) | drafted in note form |
| 4. Taxonomy of treatments | INFORMALITY.md §5 + §2.3 (options 0/A/B/C, separability of household vs firm levers) | drafted |
| 5. Calibration method (Ethiopia) | experiments/optionA/METHOD.md + build_overlay.py (reproducible pipeline) | drafted |
| 6. Results: steady states | experiments/optionA/RESULTS.md (A-0/A-0b/A-1/A-2/final tables, sensitivity) | computed |
| 7. Results: formalization reform | RESULTS.md A5 sections (endpoint + transition) | computed |
| 8. Welfare analysis | — | **NOT DONE** |
| 9. The firm side (Option B) | experiments/optionB/SPEC.md | specced, blocked on multi-industry port |
| 10. Discussion: what current practice gets wrong | sibling-repo survey (BRA/PHL/ZAF/IDN/USA treatment table) | findings collected |
| Appendix: machinery had never been exercised | the two upstream bugs (SS diagnostic, TPI path slicing) as evidence | documented |

## Work plan (sequenced)

1. **Welfare module** (next substantive step, unblocked): CEV by group and cohort for
   the A5 reform — steady-state and, now that the TPI fix runs, transitional cohorts.
   This turns "output dips 0.6%" into "who gains and who pays," which is the paper's
   distributional punchline.
2. **Robustness battery** (unblocked): Frisch elasticity, sigma, informality boundary
   (85 vs 90%), e-matrix Gini concept (interacts with OG-ETH issue #33).
3. **Option B execution** — *dependency: the multi-industry port* (separate work,
   MULTI_INDUSTRY_PORTING.md). Then A+B combined and the VAT-reform experiment (demand
   reallocation toward untaxed goods), which completes the taxonomy empirically.
4. **Possibly one more country** for generality (PHL or ZAF — same machinery, sibling
   repos already surveyed) — decide after B.
5. Prose drafting, in the order 5→6→7→4→3→8→9→10→2→1.

## House rules for the paper phase

- Everything stays on `explore/informality` (or children); still no upstream OG-Core
  method proposal — the OG-Core PRs we file are bug fixes only, cited as findings.
- Exploration mode continues (methods over precision) until results freeze for the
  draft; then one reproducibility pass re-runs everything on a single pinned ogcore.
- Numbers in the paper regenerate from committed builders/runners — no hand-typed
  results.
- All revenue ratios carry the GDP-rebasing caveat (pre-rebase denominator).
