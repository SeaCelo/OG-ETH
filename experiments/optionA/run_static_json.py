"""Solve the frozen informality calibration from the static JSON alone.

Loads ONLY `ogeth_informality_default_parameters.json` — no overlay, no
Calibration class, no network — to prove the file is self-contained and runs.
Output: experiments/optionA/OUTPUT_STATIC (untracked).
"""

import multiprocessing
from distributed import Client
import os
import json
import time
from ogcore.parameters import Specifications
from ogcore.execute import runner
import dask

dask.config.set(scheduler="synchronous")

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_JSON = os.path.join(
    CUR_DIR, "..", "..", "ogeth_informality_default_parameters.json"
)


def main():
    num_workers = min(multiprocessing.cpu_count(), 7)
    client = Client(n_workers=num_workers, threads_per_worker=1)
    out_dir = os.path.join(CUR_DIR, "OUTPUT_STATIC")

    p = Specifications(
        baseline=True,
        num_workers=num_workers,
        baseline_dir=out_dir,
        output_base=out_dir,
    )
    with open(STATIC_JSON) as f:
        p.update_specifications(json.load(f))
    print("loaded static JSON only (no Calibration, no network)")

    start = time.time()
    runner(p, time_path=False, client=client)
    print("run time =", time.time() - start)
    client.close()


if __name__ == "__main__":
    main()
