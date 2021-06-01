from distributed import Client
from dask_jobqueue import HTCondorCluster
import socket


def main():
    n_port = 8786
    with HTCondorCluster(
            cores=1,
            memory='100MB',
            disk='100MB',
            death_timeout = '60',
            nanny = True,
            scheduler_options={
                'port': n_port,
                'host': socket.gethostname()
                },
            job_extra={
                'should_transfer_files': 'Yes',
                'when_to_transfer_output': 'ON_EXIT'
                },
            extra = ['--worker-port {}'.format(n_port)]
            ) as cluster:
        with Client(cluster) as client:
            cluster.scale(1)
            future = client.submit(lambda x: x + 1, 10)
            print('Result is {}'.format(future.result()))

if __name__ == '__main__':
    main()
