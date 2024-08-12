# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 07:50:00 2024

@author: dvezinet
"""


import numpy as np


from .inputs import _config


# ###########################################################
# ###########################################################
#                  main
# ###########################################################


def main(
    coll=None,
    dsystems=None,
):

    # -------------
    # check inputs
    # -------------

    dsystems = _check(
        coll=coll,
        dsystems=dsystems,
    )

    # -------------
    # select
    # -------------

    dout = {}
    for which in [coll._which_device, coll._which_connector]:
        dout[which] = _select(
            coll=coll,
            which=which,
            dsystems=dsystems,
        )

    return dout


# ###########################################################
# ###########################################################
#                  check
# ###########################################################


def _check(
    coll=None,
    dsystems=None,
):

    # -----------------------
    # trivial
    # -----------------------

    if dsystems is None:
        return {}

    # -----------------------
    # trivial
    # -----------------------

    c0 = (
        isinstance(dsystems, dict)
        and all([
            k0 in _config._SYSTEMS
            and isinstance(v0, (str, list, tuple))
            for k0, v0 in dsystems.items()
        ])
    )
    if not c0:
        _err_dsystems(dsystems)

    # -----------------------
    # check each key / value pair
    # -----------------------

    lk = list(dsystems.keys())
    for k0 in lk:
        if isinstance(dsystems[k0], str):
            dsystems[k0] = [dsystems[k0]]

        c0 = all([isinstance(ss, str) for ss in dsystems[k0]])
        if not c0:
           _err_dsystems(dsystems)

    return dsystems


def _err_dsystems(dsystems):
    lstr = [
        f"\t- '{k0}': None, str, list (include) or tuple (exclude) of str"
        for k0 in _config._SYSTEMS
    ]
    msg = (
        "Arg dsystems must be a dict with keys:\n"
        + "\n".join(lstr)
        + f"\nProvided:\n\t{dsystems}"
    )
    raise Exception(msg)


# ###########################################################
# ###########################################################
#                  select
# ###########################################################


def _select(
    coll=None,
    which=None,
    dsystems=None,
):

    # -------------
    # include
    # -------------

    lkeys = list(coll.dobj[which].keys())
    ind = np.ones((len(lkeys),), dtype=bool)
    for k0, v0 in dsystems.items():

        if v0 is None:
            continue

        indi = np.array([
            coll.dobj[which][key]['systems'].get(k0) in v0
            for ii, key in enumerate(lkeys)
        ], dtype=bool)

        # -------------
        # effect on ind

        if isinstance(v0, list):
            ind &= indi
        else:
            ind &= (~indi)

    return np.array(lkeys)[ind].tolist()