"""Solve the Option A-0 steady state (formal/informal split via filer flags).

Mirrors examples/run_og_eth.py's baseline setup exactly, then applies the
A-0 overlay (built by build_overlay.py) and solves the steady state only.
Output goes to experiments/optionA/OUTPUT_A0 (untracked).
"""

import multiprocessing
from distributed import Client
import os
import json
import time
from importlib.resources import files
from ogeth.calibrate import Calibration
from ogcore.parameters import Specifications
from ogcore.execute import runner
from ogeth.utils import is_connected
import dask

dask.config.set(scheduler="synchronous")

CUR_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    num_workers = min(multiprocessing.cpu_count(), 7)
    client = Client(n_workers=num_workers, threads_per_worker=1)
    print("Number of workers = ", num_workers)

    out_dir = os.path.join(CUR_DIR, "OUTPUT_A0")

    p = Specifications(
        baseline=True,
        num_workers=num_workers,
        baseline_dir=out_dir,
        output_base=out_dir,
    )
    with (
        files("ogeth")
        .joinpath("ogeth_default_parameters.json")
        .open("r") as file
    ):
        defaults = json.load(file)
    p.update_specifications(defaults)
    if is_connected():
        c = Calibration(p, update_from_api=False)
        p.update_specifications(c.get_dict())

    # Apply the Option A-0 overlay on top of the untouched baseline
    with open(os.path.join(CUR_DIR, "optionA_overlay.json")) as f:
        overlay = json.load(f)
    p.update_specifications(overlay)
    print("A-0 overlay applied:", overlay)

    start_time = time.time()
    runner(p, time_path=False, client=client)
    print("run time = ", time.time() - start_time)
    client.close()


if __name__ == "__main__":
    main()
