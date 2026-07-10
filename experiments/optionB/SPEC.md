# Option B spec — formal/informal industry split (blocked on multi-industry port)

*Reconnaissance 2026-07-10. Executes only after the SAM-based M>1 calibration exists
(see MULTI_INDUSTRY_PORTING.md). This spec records the data verdict and the method so
Option B can start the day the port lands.*

## Data verdict (verified against the packaged SAM and its documentation)

The IFPRI **2022 Nexus SAM for Ethiopia** (`ogeth/data/IFPRI_SAM_ETH_2022_SAM.csv`,
108 accounts) contains **no formal/informal dimension anywhere**:
- 42 activities / 42 commodities are pure ISIC-style sectors; no registered/unregistered
  or self-employment tags.
- Labor factors are education-based only (low / medium / high schooling); households are
  rural/urban × consumption quintile; a single Enterprises account.
- Three tax accounts: direct (`dtax`), import (`mtax`), sales/excise/VAT (`stax`).
- The SAM's own 34-page technical documentation (IFPRI, Sept 2024) never uses the word
  "informal"; the nearest concepts are "household non-farm enterprises" and home (own)
  consumption, both folded into standard accounts. IFPRI's RIAPA/DCGE models on this SAM
  likewise carry no informality dimension.

So the split is a **documented judgment overlay** — as anticipated in INFORMALITY.md §5.

## Structural precedent

The **JRC Ethiopia 2015/16 SAM's Home-Production-Home-Consumption (HPHC) design**
(Aragie et al.): parallel household-production activities producing non-marketed
commodities alongside market activities producing the same goods. Not labeled
"informal," but structurally identical to what Option B needs. Method to mirror:
**split selected activities into formal/informal pairs feeding a single shared
commodity account**, so demand-side accounts don't need to know which activity
supplied the good.

## Split assignments (by informality intensity)

| Tier | Activities | Basis |
|---|---|---|
| Near-total informal | all crop/livestock/forestry/fishing | ~90% of rural employment; subsistence excluded even from the urban informality stat by definition |
| High informal | trade (`atrad`), hotels/food (`ahotl`), transport (`atran`), other services (`aosrv`) | World Bank (2021): sectors with high informality; urban own-account self-employment = 35% of urban employment |
| Mixed | construction, small-scale mining, low-end business services | day labor / artisanal segments |
| Near-zero informal | public admin, education, health, utilities, capital-intensive manufacturing | registered/public by construction |

## Calibration shares (judgment calls flagged)

1. **Aggregate anchor**: MIMIC ~37% of GDP for informal value added — GDP-side check
   only; MIMIC measures unrecorded output, not employment, and would overstate labor
   splits if applied literally.
2. **Sector employment shares**: ILOSTAT `SDG_0831_SEX_ECO_RT_A` (informal employment
   by ISIC sector) — to be pulled when Option B starts; bracket with UEUS 21.8% urban
   nonfarm informality (Feb 2022; range 16-27% across rounds; excludes subsistence
   agriculture) as floor and ~90% rural-agriculture as ceiling.
3. **Labor mapping** (biggest judgment): no informality-labor crosswalk exists; assume
   informal activities draw disproportionately on low-education labor (`flab-n`),
   formal on high-education (`flab-s`) + capital. Sensitivity-test this.
4. Apply all shares to **value added, not headcounts** (consistent with the port's
   missing-employment-data treatment).

## Model wiring (from the OG-Core structural map, INFORMALITY.md §2.3)

- Informal industry: `cit_rate[m] = 0`; informal consumption good: `tau_c[i] = 0`;
  formal good near the statutory 15% VAT, jointly reproducing the ~5.3% realized rate.
- **Migrate the informality haircut out of the economy-wide CIT multipliers**: with an
  explicit informal industry, re-derive `c_corp_share_of_assets` /
  `adjustment_factor_for_cit_receipts` so the FORMAL industries alone deliver ~2% of
  GDP in CIT — otherwise informality is double-counted (A-2-final currently carries it
  entirely in the multipliers: factor 0.385).
- Composes with Option A (household side) — the levers are independent by construction.
- Numeraire discipline from the port: the investment-good industry stays LAST; the
  informal industry must NOT be the numeraire.

## Acceptance test

Same VAT reform through (a) blended single-industry `tau_c` and (b) the B split: the
difference in revenue and consumption reallocation IS the deliverable — the demand
substitution toward untaxed informal goods that the blended rate cannot produce.
