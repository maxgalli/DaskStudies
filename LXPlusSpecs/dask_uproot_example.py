""" A very basic example that submits on HTCondorCluster a function that reads a 
remote file and returns the first 100 events for a single branch
"""

from distributed import Client
from dask_jobqueue import HTCondorCluster
import socket
import uproot
import os
import sys

def read_remote_file(inp_file):
    f = uproot.open(inp_file)
    tree = f["Events"]
    arr = t.arrays("Electron_phi")[:100]
    return arr

def main():
    n_port = 8786
    workers_port_range = "10000:10100"
    input_file = "root://redirector.t2.ucsd.edu//store/user/hmei/nanoaod_runII/HHggtautau/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_v0.6_20201021/test_nanoaod_1.root"
    proxy_path = "/afs/cern.ch/user/g/gallim/x509up_u123478"
    with HTCondorCluster(
            cores=1,
            memory='2000MB',
            disk='1000MB',
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
                'when_to_transfer_output': 'ON_EXIT',
                'transfer_input_files': '{}'.format(proxy_path)
                },
            env_extra=["export X509_USER_PROXY={}".format(proxy_path)],
            extra=['--worker-port {}'.format(workers_port_range)]
            ) as cluster:
        print("Started HTCondorCluster")
        print(cluster.job_script())
        with Client(cluster) as client:
            cluster.scale(1)
            future = client.submit(read_remote_file, input_file)
            print('Array is {}'.format(future.result()))

if __name__ == '__main__':
    main()
