"""A5 — the formalization reform on the A-2 platform.

Baseline: the A-2 calibration (graded compliance [1,1,1,1,1,0.5,0], statutory
35% MTR, ETR 13.32%) solved with its full transition path.

Reform: compliance improves linearly over five years and then holds —
noncompliance falls to [1,1,1,1,0.9,0.25,0]. Group 5 becomes 10% visible,
group 6 goes from half to three-quarters visible, the top group is already
fully compliant. Statutory rates NEVER change: this is a pure base-broadening
/ compliance reform, the National Medium-Term Revenue Strategy in stylized
form. Static arithmetic: the compliance-weighted base grows ~47%, taking PIT
from ~1.4 to ~2.1% of GDP before behavior responds — in the neighborhood of
the IMF program's direct-tax path (3.5 -> 4.7% of GDP by 2029/30, CR 26/20
Table 2b, which includes CIT gains we do not model here).

Mirrors examples/run_og_eth.py's two-phase structure. Output (untracked):
OUTPUT_A5_BASELINE / OUTPUT_A5_REFORM under experiments/optionA/.
"""

import multiprocessing
from distributed import Client
import os
import json
import time
import numpy as np
from importlib.resources import files
from ogeth.calibrate import Calibration
from ogcore.parameters import Specifications
from ogcore.execute import runner
from ogcore.utils import safe_read_pickle
from ogeth.utils import is_connected
import dask

dask.config.set(scheduler="synchronous")

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

NC_START = [1.0, 1.0, 1.0, 1.0, 1.0, 0.50, 0.0]
NC_END = [1.0, 1.0, 1.0, 1.0, 0.9, 0.25, 0.0]
RAMP_YEARS = 5


def compliance_path():
    """Linear ramp from NC_START to NC_END over RAMP_YEARS, then constant."""
    rows = []
    for t in range(RAMP_YEARS + 1):
        frac = t / RAMP_YEARS
        rows.append(
            [
                round(s + frac * (e - s), 4)
                for s, e in zip(NC_START, NC_END)
            ]
        )
    return rows


def make_spec(baseline, out_dir, base_dir, num_workers):
    p = Specifications(
        baseline=baseline,
        num_workers=num_workers,
        baseline_dir=base_dir,
        output_base=out_dir,
    )
    with (
        files("ogeth")
        .joinpath("ogeth_default_parameters.json")
        .open("r") as file
    ):
        p.update_specifications(json.load(file))
    if is_connected():
        c = Calibration(p, update_from_api=False)
        p.update_specifications(c.get_dict())
    with open(os.path.join(CUR_DIR, "optionA_overlay_2_final.json")) as f:
        p.update_specifications(json.load(f))
    return p


def main():
    num_workers = min(multiprocessing.cpu_count(), 7)
    client = Client(n_workers=num_workers, threads_per_worker=1)
    base_dir = os.path.join(CUR_DIR, "OUTPUT_A5_BASELINE")
    reform_dir = os.path.join(CUR_DIR, "OUTPUT_A5_REFORM")

    # Phase 1: A-2 baseline with transition path
    p = make_spec(True, base_dir, base_dir, num_workers)
    start = time.time()
    runner(p, time_path=True, client=client)
    print("baseline run time =", time.time() - start)

    # Phase 2: formalization reform
    p2 = make_spec(False, reform_dir, base_dir, num_workers)
    path = compliance_path()
    p2.update_specifications(
        {
            "labor_income_tax_noncompliance_rate": path,
            "capital_income_tax_noncompliance_rate": path,
        }
    )
    print("reform compliance path (noncompliance by year):")
    for r in path:
        print("  ", r)
    start = time.time()
    runner(p2, time_path=True, client=client)
    print("reform run time =", time.time() - start)
    client.close()

    # Quick readout: revenue and macro paths, reform vs baseline
    bt = safe_read_pickle(os.path.join(base_dir, "TPI", "TPI_vars.pkl"))
    rt = safe_read_pickle(os.path.join(reform_dir, "TPI", "TPI_vars.pkl"))
    for k in ["Y", "total_tax_revenue", "iit_payroll_tax_revenue", "L", "K"]:
        b = np.asarray(bt[k])[:12]
        r = np.asarray(rt[k])[:12]
        print(f"{k} % change (first 12 years):", np.round(100 * (r / b - 1), 2))


if __name__ == "__main__":
    main()
