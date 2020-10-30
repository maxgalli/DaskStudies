import argparse

from dask.distributed import Client, LocalCluster, progress
from dask_jobqueue import SLURMCluster

from tasks import dummy_function, sleep_more

import yaml

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run simple jobs locally or in a distributed environment")

    parser.add_argument(
        "--config_file",
        type=str,
        help="Full path to cluster config file")

    return parser.parse_args()

def main(args):
    config_file = args.config_file

    # Configure on cluster
    if config_file:
        stream = open(config_file, 'r')
        inp = yaml.load(stream)
        cores = inp['jobqueue']['slurm']['cores']
        memory = inp['jobqueue']['slurm']['memory']
        jobs = inp['jobqueue']['slurm']['jobs']
        cluster = SLURMCluster(
                cores = cores,
                memory = memory,
                )
        cluster.scale(jobs = jobs)

    # Configure locally
    else:
        cluster = LocalCluster()

    client = Client(cluster)
    raised_futures = client.map(sleep_more, range(100))
    progress(raised_futures)
    raised = client.gather(raised_futures)
    print('\n', raised)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
