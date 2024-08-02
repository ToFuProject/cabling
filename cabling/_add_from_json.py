# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 17:40:55 2024

@author: dvezinet
"""

import os
import json


import datastock as ds


#############################################
#############################################
#       main
#############################################


def main(coll=None, pfe=None):


    # -------------
    # check inputs
    # --------------

    dpfe = _check(pfe)

    # --------------
    # add
    # --------------

    for k0, v0 in dpfe.items():

        with open(v0['pfe']) as json_file:
            din = json.load(json_file)
            for k1, v1 in din.items():
                getattr(coll, f"add_{v0['which']}")(k1, **v1)

    return


#############################################
#############################################
#      check
#############################################


def _check(pfe=None):

    # ------------------
    # preliminary
    # -------------------

    # ------------
    # files

    pfe = ds.get_files(pfe)
    pfe = [pp for pp in pfe if pp.endswith('.json')]
    print(pfe)

    # -------------------
    # which testing order

    lw = [
        'connection_type',
        'connection_model',
        'connection',
        'device_type',
        'device_model',
        'device'
    ]


    # ------------------
    # check fileby file
    # -------------------

    dpfe = {}
    derr = {}
    for ii, pp in enumerate(pfe):

        key = f"file{ii}"

        # ---------------
        # check validity

        if not os.path.isfile(pp):
            derr[key] = f'Not valid file: {pp}'
            continue

        # -------------
        # extract which

        for jj, ww in enumerate(lw):
            if ww in pp:
                dpfe[key] = {
                    'pfe': pp,
                    'which': ww,
                }
                break

    # ------------------
    # raise exception
    # -------------------

    if len(derr) > 0:
        lstr = [f"\t- {k0}: {v0}" for k0, v0 in derr.items()]
        msg = (
            "The following files could not be identified:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    return dpfe