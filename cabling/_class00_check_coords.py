# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 14:42:31 2024

@author: dvezinet
"""


import itertools as itt


import numpy as np


#############################################
#############################################
#       coordinates for devices
#############################################


def _dcoords(coll, which, key, dcoords):

    # --------------
    # trivial
    # -------------

    if dcoords is None:
        return

    # ------------
    # error
    # -------------

    elif not isinstance(dcoords, dict):
        _dcoords_err(which, key, dcoords)

    # ---------------
    # conformity
    # ---------------

    else:

        # -----------------
        # known cases

        dok = {
            '3d': ['x', 'y', 'z'],
        }


        for k0, v0 in dcoords.items():

            # -----------------
            # preliminary check

            c0 = (
                isinstance(k0, str)
                and isinstance(v0, (dict, tuple, list, np.ndarray))
            )

            if not c0:
                _dcoords_err(which, key, dcoords)

            # -----------
            # known cases

            lok = dok.get(k0, ['x', 'y'])
            if not isinstance(v0, dict):
                if len(v0) == len(lok):
                    dcoords[k0] = {ok: v0[ii] for ii, ok in enumerate(lok)}
                else:
                    _dcoords_err(which, key, dcoords, k0, lok)

            if sorted(dcoords[k0].keys()) != lok:
                _dcoords_err(which, key, dcoords, k0, lok)

        # --------------------
        # format as np.ndarray

        for k0, v0 in dcoords.items():
            for k1, v1 in v0.items():
                if not np.isscalar(v1):
                    dcoords[k0][k1] = np.asarray(v1).ravel()

    return dcoords


# ##################
#       error
# ##################


def _dcoords_err(which, key, dcoords, k0=None, lok=None):
    if lok is None:
        gap = (
            "\t- '3d': {'x': float, 'y': float, 'z': float}\n"
            "\t- 'key0': {'x': float, 'y': float}\n"
            "\t- 'key1': {'x': float, 'y': float}\n"
        )
    else:
        lstr = "{" + ", ".join([f"{kk}: float" for kk in lok]) + "}"
        gap = f"\t- '{k0}': {lstr}\n"
    msg = (
        f"For {which} '{key}', arg 'dcoords' must be a dict of the form:\n"
        f"{gap}"
        f"Provided:\n\t{dcoords}"
    )
    raise Exception(msg)


#############################################
#############################################
#       coordinates for connectors
#############################################


def _dcoords_connector(coll, which, key, dcon, dcoords):

    # --------------------------------------------
    # get list of coords provided by both devices
    # --------------------------------------------

    wdev = coll._which_device
    if all([vv['flag'] == 'ok' for vv in dcon.values()]):
        lcoords_dev = sorted(set(itt.chain.from_iterable([
            coll.dobj[wdev][vv[wdev][0]].get('dcoords', {}).keys()
            for vv in dcon.values()
        ])))
        if len(lcoords_dev) == 0:
            lcoords_dev = None
    else:
        lcoords_dev = None

    # ---------------------
    # return
    # ---------------------

    if lcoords_dev is None:
        return dcoords

    # ---------------------
    # add coord inner keys
    # ---------------------

    dcoords_dev = {
        k1: sorted(set(itt.chain.from_iterable([
            list(coll.dobj[wdev][vv[wdev][0]].get('dcoords', {}).get(k1, {}).keys())
            for vv in dcon.values()
        ])))
        for k1 in lcoords_dev
    }

    # ---------------------------------
    # check match to connected devices
    # ---------------------------------

    if dcoords is None:
        dcoords = {}

    lkcon= sorted(dcon.keys())
    for kcoord in lcoords_dev:

        if kcoord not in dcoords.keys():
            dcoords[kcoord] = {
                k1: np.array([
                    coll.dobj[wdev][dcon[kcon][wdev][0]]['dcoords'][kcoord][k1]
                    for kcon in lkcon
                ])
                for k1 in dcoords_dev[kcoord]
            }

    return dcoords