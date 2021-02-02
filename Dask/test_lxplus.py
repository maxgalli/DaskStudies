from distributed import Client
from dask_jobqueue import HTCondorCluster
import socket

import logging
logger = logging.getLogger("")

def setup_logging(output_file, level=logging.DEBUG):
    logger.setLevel(level)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = logging.FileHandler(output_file, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def main():
    n_port = 8786
    with HTCondorCluster(
            cores=1,
            memory='100MB',
            disk='100MB',
            death_timeout = '60',
            nanny = False,
            scheduler_options={
                'port': n_port,
                'host': socket.gethostname()
                },
            job_extra={
                'log': 'dask_job_output.log',
                'output': 'dask_job_output.out',
                'error': 'dask_job_output.err',
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
    #setup_logging('prototype.log', logging.INFO)
    #setup_logging('test_basic2.log') # debug
    main()
