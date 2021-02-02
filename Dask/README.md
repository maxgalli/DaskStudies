## DaskStudies

Small *vademecum* for the procedure to parallelize operations using [Dask](https://docs.dask.org/en/latest/index.html), [Dask.distributed](https://distributed.dask.org/en/latest/index.html) and [Dask-Jobqueue](https://jobqueue.dask.org/en/latest/index.html), using both local clusters and distributed batch systems.

### SLURM
```run_on_slurm.py``` runs a function that sleeps for 40 seconds on a list of 100 elements. 
It can be called with no arguments to run on a local cluster and in the following way to run on a SLURM distributed batch system:
```bash
$ python run_on_slurm.py --config_file config_environment.yaml
```
The results are as expected: 
* if we run locally on a machine with 72 cores, we get:
```
[########################################] | 100% Completed | 1min 20.2s
```
which is exactly 40 seconds * 2, since not all the operations can run in parallel

* if we submit 100 jobs, we get:
```
[########################################] | 100% Completed | 50.0s
```
