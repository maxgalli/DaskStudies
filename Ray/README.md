# Ray
Some essentials to quick distribute computation locally and on a SLURM cluster using Ray and/or Ray + Joblib.

To set up a Ray cluster on SLURM:

- run ```ray start --head --port=6379 --num-cpus 1 --block```
- start running workers on different nodes by running ```sbatch submit_worker.sub $ip_address $redi_pass```
- ```basic_slurm.py``` shows how to connect to a cluster creating in this way
- ```joblib_ray.ipynb``` shows how to use Joblib in combination with such cluster
