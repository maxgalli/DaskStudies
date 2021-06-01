#!/usr/bin/python3

#
#lxplus.cern.ch$ ./htmap_double_example.py
#[CREDD] Adding user credentials to credd daemon
#Map(tag = tiny-harsh-city)
#[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
#

import htcondor
import htmap

def double(x):
    return 2 * x

# Send credentials
credd = htcondor.Credd()
print ("[CREDD] Adding user credentials to credd daemon")
credd.add_user_cred(htcondor.CredTypes.Kerberos, None)

mapped = htmap.map(double, range(10), map_options = htmap.MapOptions(custom_options={"MY.SendCredential": "true"}))
print(mapped)
doubled = list(mapped)
print(doubled)
