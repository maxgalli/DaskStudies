"""
This is meant to be run over the dummy files produced with:
https://github.com/maxgalli/UsefulHEPScripts/blob/master/samples/fill_dummy_samples_multibranch.py

The only (required) argument <base-dir> is the path to the directory where the above mentioned
files are stored.

Use htmap to submit one job per file and return an awkward array with all the branches read.

In the end, print info about the concatenated array.
"""

import argparse
import os
import awkward as ak
import htcondor
import htmap
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

    return parser.parse_args()


def main(args):
    base_dir = args.base_dir

    input_files = [base_dir + "/" + fl for fl in os.listdir(base_dir)]
    print("Found {} files in {}".format(len(input_files), base_dir))

    # Send credentials
    credd = htcondor.Credd()
    print ("[CREDD] Adding user credentials to credd daemon")
    credd.add_user_cred(htcondor.CredTypes.Kerberos, None)

    mapped_arrays = htmap.map(
        dummy_extractor, 
        input_files, 
        map_options = htmap.MapOptions(custom_options={"MY.SendCredential": "true"})
        )
    mapped_arrays.wait(show_progress_bar = True)

    arrays = list(mapped_arrays)
    final_arr = ak.concatenate(arrays)

    print("Done concatenating")
    print(final_arr.type)



if __name__ == "__main__":
    args = parse_arguments()
    main(args)