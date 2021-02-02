import ray
import time


@ray.remote
def f(x):
    time.sleep(5)
    return x

def main():
    # Start Ray.
    ray.init()

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
    main()
