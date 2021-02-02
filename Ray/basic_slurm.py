import time
import ray
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description = 'Run trivial functions on a SLURM Ray cluster')

    parser.add_argument(
        "-cl",
        "--cluster_id",
        required=True,
        type=str,
        help="")

    return parser.parse_args()


@ray.remote
def f(x):
    time.sleep(5)
    return x


def main(args):
    ip_head = args.cluster_id
    ray.init(address=ip_head)

    print("Nodes in the Ray cluster:")
    print(ray.nodes())

    # Start 4 tasks in parallel.
    result_ids = []
    start = time.time()
    for i in range(4):
        result_ids.append(f.remote(i))

    # Wait for the tasks to complete and retrieve the results.
    results = ray.get(result_ids)
    end = time.time()

    print('Results {} computed in {} seconds'.format(results, end - start))

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
