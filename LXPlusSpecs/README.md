# HTMap

Adapting [htmap](https://github.com/htcondor/htmap) to work correctly on LXPlus is an ongoing effort at the moment of writing (01.06.2021). 
## Setup

htmap seems to work with both the following configurations:

- ```/usr/bin/python3``` and htmap installed with the following procedure:
```
git clone --branch afs_log https://github.com/luisfdez/htmap.git
cd htmap
/usr/bin/python3 setup.py install --user
```
- htmap installed like explained before in a conda environment (at the moment, the environment created with [this](https://github.com/maxgalli/dask-dimuon-analysis-rdf/blob/lxplus/environment.yml) file has been tested)

## Tests

- ```htmap_double_example.py``` contains the htmap basic tutorial with the necessary changes to run on lxplus
