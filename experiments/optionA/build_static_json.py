"""Freeze the Option A informality calibration into one static JSON.

Produces `ogeth_informality_default_parameters.json` at the branch root: the
packaged FY2024/25 base parameters with the A-2-final informality overlay
merged in. This file is self-contained — it can be loaded directly into an
OG-Core Specifications object with no overlay step, no Calibration class, and
no network.

Why this is complete on its own (verified): the packaged base JSON already
carries every large array (e, omega, rho, chi_n, ...), and
`Calibration(p, update_from_api=False)` only sets alpha_c=[1] and
io_matrix=[[1]] for the single-industry case, which already match the base
JSON. So base JSON + informality overlay is the entire calibration.
"""

import json
import os
from importlib.resources import files

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
OUT = os.path.join(
    CUR_DIR, "..", "..", "ogeth_informality_default_parameters.json"
)
OVERLAY = os.path.join(CUR_DIR, "optionA_overlay_2_final.json")


def main():
    with (
        files("ogeth").joinpath("ogeth_default_parameters.json").open("r") as f
    ):
        params = json.load(f)
    with open(OVERLAY) as f:
        overlay = json.load(f)

    # base JSON is flat ({param: value}); overwrite each overlaid key
    for key, value in overlay.items():
        params[key] = value

    with open(OUT, "w") as f:
        json.dump(params, f, indent=2)
    print("merged", len(overlay), "informality params into base:")
    for k in overlay:
        print("  ", k, "=", overlay[k])
    print("wrote", os.path.relpath(OUT, os.path.join(CUR_DIR, "..", "..")))


if __name__ == "__main__":
    main()
