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


if __name__ == "__main__":
    main()
