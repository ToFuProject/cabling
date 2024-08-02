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


def main(coll=None, pfe=None, verb=None):

    # -------------
    # check inputs
    # --------------

    dpfe, verb = _check(pfe, verb)

    # --------------
    # verb
    # --------------

    if verb >= 1:
        msg = (
            "\n----------------------------------------------------------\n"
            "Populating with Connections, Connectors, Devices from json"
        )
        print(msg)

    # --------------
    # loop on files
    # --------------

    for k0, v0 in dpfe.items():

        # ----------
        # open file

        with open(v0['pfe']) as json_file:
            din = json.load(json_file)
            ntot = len(din)

            # ----------
            # verb

            if verb >= 1:
                msg = (
                    f"\n\t| File {v0['pfe']}"
                    f"\n\t|\t {v0['which']}: {ntot} items"
                )
                if verb >= 2:
                    msg += "\n\t|"
                print(msg)

            # -------------
            # loop on items

            for ii, (k1, v1) in enumerate(din.items()):

                # verb
                if verb >= 2:
                    msg = f"\t|\t- item {ii+1}/{ntot}: \t'{k1}'"
                    print(msg)

                # add to Collection
                getattr(coll, f"add_{v0['which']}")(k1, **v1)

    # --------------
    # verb
    # --------------

    if verb >= 1:
        msg = '\n--------------------------------------------------------\n'
        print(msg)

    return


#############################################
#############################################
#      check
#############################################


def _check(pfe=None, verb=None):

    # ------------------
    # preliminary
    # -------------------

    # ------------
    # files

    pfe = ds.get_files(pfe)
    pfe = [pp for pp in pfe if pp.endswith('.json')]

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
                    'pfe': os.path.abspath(pp),
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

    # ------------------
    # verb
    # -------------------

    verb_def = 1
    verb = ds._generic_check._check_var(
        verb, 'verb',
        types=(bool, int),
        default=verb_def,
        allowed=[True, False, 0, 1, 2],
    )

    if verb is True:
        verb = verb_def
    elif verb is False:
        verb = 0

    return dpfe, verb