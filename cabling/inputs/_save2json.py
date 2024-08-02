# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 11:47:42 2024

@author: dvezinet
"""


import os
import json


#############################################
#############################################
#        DEFAULTS
#############################################


_PATH_HERE = os.path.dirname(__file__)


#############################################
#############################################
#    Connection types
#############################################

def main(path=None, dout=None, which=None):

    # ---------------
    # save to json
    # ---------------

    if path is None:
        path = os.path.abspath(_PATH_HERE)

    pfe = os.path.join(path, f'{which}.json')

    with open(pfe, "w") as outfile:
        json.dump(dout, outfile, indent=4)

    msg = f"Saved in:\n\t{pfe}"
    print(msg)

    return dout