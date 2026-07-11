# Seed bibliography (collected during the exploration, 2026-07)

*To be converted to BibTeX when drafting starts. Grouped by paper section.*

## Informality measurement (Ethiopia and general)
- ILO (2023), Youth Country Brief Ethiopia — informal employment 85.2% (2021).
  https://www.ilo.org/media/362676/download
- Ethiopian Statistical Service (2022), Urban Employment/Unemployment Survey, 1st round
  — urban informal sector 21.8% (definition excludes subsistence agriculture).
  https://ess.gov.et/wp-content/uploads/2024/09/2022_1st-Round-UEUS-Key-Findings.pdf
- Medina, L. & F. Schneider (2018), "Shadow Economies Around the World," IMF WP 18/17
  — MIMIC method; Ethiopia ~37% of GDP.
- Elgin, Kose, Ohnsorge & Yu (2021), "Understanding Informality," CEPR DP 16497.
- World Bank (2021), "Employment in Urban and Rural Ethiopia" — sectoral informality,
  ~90% rural agricultural employment, urban own-account 35%.

## Ethiopia fiscal data (calibration anchors)
- IMF (2025), "Ethiopia's Tax System: Structure, Performance, and Benchmarking,"
  Selected Issues Paper 2025/108 (= CR 25/189) — PIT 1.4% / CIT 1.7% of GDP
  (FY2021/22–23/24 avg, text-stated ¶9); tax potential ~17% vs ~8% actual; ¶14 on
  marginal rates and formalization disincentives.
- IMF (2026), Country Report 26/20 — Fourth ECF Review; Table 2b general-government
  operations (direct 3.5% of GDP FY24/25; program revenue path to 10.9% by 2029/30).
- IFS/TaxDev (2025), "Ethiopia's tax-to-GDP ratio has fallen…" — 12.4%→7.5%
  (2014/15–2022/23); ~1.8pp attributed to compliance decline.
- UNU-WIDER Government Revenue Dataset — Ethiopia PIT/CIT split ends 2007 (1.05/1.39);
  used as historical corroboration only.

## Informality in structural models
- IMF (2021), "The Global Informal Workforce: Priorities for Inclusive Growth" (IMF/ILO
  volume).
- Colombo, Furceri, Pizzuto & Tirelli (2022→2025), "Fiscal Multipliers and Informality,"
  IMF WP 22/82 (publ. Int. Economics and Economic Policy) — NK-DSGE with informal
  sector for SSA; official-sector tax shocks reallocate demand/factors to informal.
- Cogent Economics & Finance (2022), "A DSGE model of fiscal stabilizers and informality
  in Sub-Sahara Africa" — tax hikes → evasion and factor reallocation to shadow sector.
- Bachas, Gadenne & Jensen (2024), "Informality, Consumption Taxes, and Redistribution"
  (NBER 27429 / REStud) — firm-heterogeneity GE with informality/evasion margins.
- IMF DIG/DIGNAR family (LIC public-investment DSGEs) — phase-3 informality extension
  claimed; specific implementation unverified (flagged).
- Gollin (2002), "Getting Income Shares Right" — self-employment/mixed-income correction
  (used in our gamma calibration and the OG-PHL SAM rescale).
- La Porta & Shleifer (2014), "Informality and Development," JEP — dual-economy view
  (Option C's theoretical frame).

## Model framework
- DeBacker, Evans et al. — OG-Core framework (github.com/PSLmodels/OG-Core), v0.16.3;
  tax noncompliance parameters added in OG-Core PR #816.
- OG-ETH (EAPD-DRB/OG-ETH) — Ethiopia calibration; FY2024/25 baseline commit 15f424f.
- IFPRI (2024), "2022 Social Accounting Matrix for Ethiopia: A Nexus Project SAM" —
  no informality dimension (verified).
- JRC (2020), Ethiopia SAM 2015/16 — Home-Production-Home-Consumption accounts (Aragie
  et al.); structural precedent for the Option B split.

## Findings of this project citable as evidence
- Zero informality precedent in PSLmodels/EAPD OG repos (live search, July 2026).
- OG-Core SS diagnostic bug (PR #1171) and TPI compliance-path bug (fix branch
  `fix-tpi-noncompliance-path`) — evidence the compliance machinery was previously
  unexercised.
