# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 07:50:00 2024

@author: dvezinet
"""


import itertools as itt


import numpy as np


# ###########################################################
# ###########################################################
#                  main
# ###########################################################


def main(
    coll=None,
    include=None,
    exclude=None,
):

    # -------------
    # check inputs
    # -------------

    dinex = _check(
        coll=coll,
        include=include,
        exclude=exclude,
    )

    # -------------
    # select
    # -------------

    dout = {}
    for which in [coll._which_device, coll._which_connector]:
        dout[which] = _select(
            coll=coll,
            which=which,
            dinex=dinex,
        )

    return dout


# ###########################################################
# ###########################################################
#                  check
# ###########################################################


def _check(
    coll=None,
    include=None,
    exclude=None,
):

    # -----------------------
    # prepare unique systems
    # -----------------------

    dsystems = {}

    # from devices
    wdev = coll._which_device
    dsystems[wdev] = {
        'unique': list(set(itt.chain.from_iterable([
            v0['systems'] for v0 in coll.dobj[wdev].values()
            if v0.get('systems') is not None
        ])))
    }

    # from connectors
    wcon = coll._which_connector
    dsystems[wcon] = {
        'unique': list(set(itt.chain.from_iterable([
            v0['systems'] for v0 in coll.dobj[wcon].values()
            if v0.get('systems') is not None
        ])))
    }

    systems_all_parts = list(set(dsystems[wdev]['unique'] + dsystems[wcon]['unique']))
    systems_all = list(set(
        [
            v0['systems'] for v0 in coll.dobj[wdev].values()
            if v0.get('systems') is not None
        ]
        + [
            v0['systems'] for v0 in coll.dobj[wcon].values()
            if v0.get('systems') is not None
        ]
    ))

    # --------------
    # prepare
    # --------------

    dinex = {'include': include, 'exclude': exclude}
    for k0, v0 in dinex.items():

        if v0 is None:
            continue

        if isinstance(v0, str):
            if v0 not in systems_all_parts:
                msg = (
                    "In arg '{k0}' is a str, it must be a valid system level\n"
                    f"\t- provided: {v0}\n\n"
                    f"Available system levels:\n{systems_all_parts}"
                )
                raise Exception(msg)
            dinex[k0] = [v0]

        elif isinstance(v0, tuple):
            if v0 not in systems_all:
                msg = (
                    "In arg '{k0}' is a tuple, it must be a valid system\n"
                    f"\t- provided: {v0}\n\n"
                    f"Available system levels:\n{systems_all}"
                )
                raise Exception(msg)

        elif isinstance(v0, list):
            lout = [
                ss for ss in v0 if not (
                    isinstance(ss, str)
                    and ss in systems_all_parts
                )
            ]
            if len(lout) > 0:
                msg = (
                    "In arg '{k0}' is a list, it must be a list of valid system level\n"
                    f"\t- provided: {v0}\n\n"
                    f"Available system levels:\n{systems_all_parts}"
                )
                raise Exception(msg)

    return dinex


# ###########################################################
# ###########################################################
#                  select
# ###########################################################


def _select(
    coll=None,
    which=None,
    dinex=None,
):

    # -------------
    # include
    # -------------

    lkeys = list(coll.dobj[which].keys())
    lsystems = [coll.dobj[which][k0]['systems'] for k0 in lkeys]

    ind = np.ones((len(lkeys),), dtype=bool)
    for k0, v0 in dinex.items():

        if v0 is None:
            continue

        for ss in v0:

            if isinstance(ss, str):
                indi = np.array(
                    [
                        isinstance(sys, tuple)
                        and ss in sys
                        for sys in lsystems
                    ],
                    dtype=bool,
                )

            else:
                indi = np.array(
                    [
                        isinstance(sys, tuple)
                        and sys == ss
                        for sys in lsystems
                    ],
                    dtype=bool,
                )

            # -------------
            # effect on ind

            if k0 == 'include':
                ind &= indi
            else:
                ind &= (~indi)

    return np.array(lkeys)[ind].tolist()