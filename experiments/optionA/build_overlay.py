"""Build the Option A-0 overlay: formal/informal split via filer flags.

Reads the Phase 0 baseline steady state and computes the flat ETR that the
filing (formal) groups must face so that model personal-income-tax revenue
matches the data anchor (PIT as a share of GDP, IMF SIP 2025/189 Figure 5).
Writes experiments/optionA/optionA_overlay.json.

Design (see INFORMALITY.md §9, Phase A):
- Bottom 5 lifetime-income groups (90% of households) are non-filers:
  no income tax owed and no income-tax wedge on their decisions. They keep
  paying the coverage-adjusted payroll rate (0.03) and consumption taxes.
- Top 2 groups (10% of households) file at a flat ETR solved from the
  revenue identity below. MTRs are left at the baseline 0.20 so A-0 changes
  one thing at a time (a-la-carte MTR sensitivity is variant A-0b).
"""

import json
import os
import numpy as np
from ogcore.utils import safe_read_pickle

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_SS = os.path.join(
    CUR_DIR, "..", "..", "examples", "OG-ETH-Example", "OUTPUT_BASELINE"
)
PIT_TARGET_SHARE_OF_Y = 0.015  # IMF SIP 2025/189 Fig 5: PIT ~1.5% of GDP
FILER = [0, 0, 0, 0, 0, 1, 1]  # bottom 90% informal (ILO: 85.2% informal)


def main():
    ss = safe_read_pickle(os.path.join(BASE_SS, "SS", "SS_vars.pkl"))
    p = safe_read_pickle(os.path.join(BASE_SS, "model_params.pkl"))
    inc = ss["before_tax_income"]
    om = p.omega_SS.reshape(p.S, 1)
    lam = p.lambdas.reshape(1, p.J)
    by_j = (inc * om * lam).sum(axis=0)
    filer_income = (by_j * np.array(FILER)).sum()
    etr_filers = PIT_TARGET_SHARE_OF_Y * ss["Y"] / filer_income

    overlay = {
        "income_tax_filer": [[float(f) for f in FILER]],
        "etr_params": [[[round(float(etr_filers), 4)]]],
        # mtrx/mtry deliberately unchanged (baseline 0.20, now filers-only)
    }
    out = os.path.join(CUR_DIR, "optionA_overlay.json")
    with open(out, "w") as f:
        json.dump(overlay, f, indent=2)
    print("filer income share of household income:", round(filer_income / (by_j.sum()), 4))
    print("solved filer ETR:", round(float(etr_filers), 4))
    print("wrote", out)

    # A-0b: same filers, same average rate, but a statutory-like marginal
    # rate on labor income (35%: IMF SIP 2025/189 notes the top PIT rate
    # applies at relatively modest formal incomes). mtry stays at 0.20.
    overlay_b = dict(overlay)
    overlay_b["mtrx_params"] = [[[0.35]]]
    out_b = os.path.join(CUR_DIR, "optionA_overlay_b.json")
    with open(out_b, "w") as f:
        json.dump(overlay_b, f, indent=2)
    print("wrote", out_b)

    # A-1: graded compliance instead of a binary filer line. Everyone
    # nominally files; noncompliance falls with lifetime income (1.0 =
    # nothing owed is paid). Group 6's 0.5 is a judgment call (partly
    # visible high earners); labor and capital rates are set EQUAL, which
    # also sidesteps the upstream SS.py mtry_ss diagnostic bug. ETR is
    # solved from the same revenue identity on the compliance-weighted base.
    NC = [1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0]
    eff_base = (by_j * (1 - np.array(NC))).sum()
    etr_a1 = PIT_TARGET_SHARE_OF_Y * ss["Y"] / eff_base
    overlay_1 = {
        "income_tax_filer": [[1.0] * 7],
        "labor_income_tax_noncompliance_rate": [NC],
        "capital_income_tax_noncompliance_rate": [NC],
        "etr_params": [[[round(float(etr_a1), 4)]]],
        # mtrx kept at baseline 0.20 so A-1 vs A-0 isolates the compliance
        # parameterization; a graded+35%-MTR combination comes after.
    }
    out_1 = os.path.join(CUR_DIR, "optionA_overlay_1.json")
    with open(out_1, "w") as f:
        json.dump(overlay_1, f, indent=2)
    print("A-1 compliance-weighted income base share:", round(eff_base / by_j.sum(), 4))
    print("A-1 solved ETR:", round(float(etr_a1), 4))
    print("wrote", out_1)

    # A-2 (preferred candidate): A-1's graded compliance + A-0b's
    # statutory-like 35% marginal rate on labor income.
    overlay_2 = dict(overlay_1)
    overlay_2["mtrx_params"] = [[[0.35]]]
    out_2 = os.path.join(CUR_DIR, "optionA_overlay_2.json")
    with open(out_2, "w") as f:
        json.dump(overlay_2, f, indent=2)
    print("wrote", out_2)

    # A-2-final: close the remaining gaps observed in the solved A-2 SS.
    # (i) ETR scaled by target/realized PIT (1.50/1.42) to offset the
    # behavioral feedback; (ii) CIT collections factor scaled so business
    # tax hits its ~2.0% of GDP anchor (realized 1.04% at factor 0.2).
    overlay_2f = dict(overlay_2)
    overlay_2f["etr_params"] = [[[round(float(etr_a1) * 1.5 / 1.42, 4)]]]
    overlay_2f["adjustment_factor_for_cit_receipts"] = [
        round(0.2 * 2.0 / 1.04, 3)
    ]
    out_2f = os.path.join(CUR_DIR, "optionA_overlay_2_final.json")
    with open(out_2f, "w") as f:
        json.dump(overlay_2f, f, indent=2)
    print("A-2-final ETR:", overlay_2f["etr_params"][0][0][0],
          " CIT factor:", overlay_2f["adjustment_factor_for_cit_receipts"][0])
    print("wrote", out_2f)


if __name__ == "__main__":
    main()
