"""
See description of htmap_dummy_pxpy.py.
In this case we use Dask to parallelize the computation.
<n-workers> determines the number of workers we scale our cluster to (defaults to 10).
"""

import argparse
from distributed import Client
from dask_jobqueue import HTCondorCluster
import socket
import awkward as ak
import os
from time import time
from datetime import timedelta

import uproot


def dummy_extractor(file_name):
    """ Taking as input the name of a file with only a TTree inside, 
    return an awkward array with all the branches as columns
    """
    fl = uproot.open(file_name)
    tree = fl[fl.keys()[0]]
    return tree.arrays()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", type=str, required=True)
    parser.add_argument("--n-workers", type=int, default=10)

    return parser.parse_args()


def main(args):
    base_dir = args.base_dir
    n_workers = args.n_workers

    input_files = [base_dir + "/" + fl for fl in os.listdir(base_dir)]
    print("Found {} files in {}".format(len(input_files), base_dir))

    start = time()

    n_port = 8786
    with HTCondorCluster(
        cores=1,
        memory="500MB",
        disk="500MB",
        death_timeout="60",
        nanny=False,
        scheduler_options={
            "port": n_port,
            "host": socket.gethostname()
        },
        job_extra={
            "should_transfer_files": "Yes",
            "when_to_transfer_output": "ON_EXIT",
            "+JobFlavour": "espresso"
        },
        extra=["--worker-port {}".format(n_port)]
    ) as cluster:
        #print(cluster.job_script())
        with Client(cluster) as client:
            cluster.scale(n_workers)
            futures = client.map(dummy_extractor, input_files)
            arrays = client.gather(futures)

    end = time()

    final_arr = ak.concatenate(arrays)

    print("Done concatenating")
    print(final_arr.type)
    print("Computation time: {}".format(str(timedelta(seconds=int(end - start)))))


if __name__ == "__main__":
    args = parse_arguments()
    main(args)