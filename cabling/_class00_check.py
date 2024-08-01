# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:31:37 2024

@author: dvezinet
"""


import datastock as ds


from . import _class00_def_dict as _def_dict


#############################################
#############################################
#       main
#############################################


def main(
    coll=None,
    key=None,
    ptA=None,
    ptB=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    wcon = coll._which_connector
    lout = list(coll.dobj.get(wcon, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ---------------------
    # ptA, ptB
    # ---------------------

    _ptAB(coll, key, ptA, ptB)

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _kwdargs(coll, key, kwdargs)

    # ---------------------
    # store
    # ---------------------

    coll.add_obj(
        which=wcon,
        key=key,
        ptA=ptA,
        ptB=ptB,
        harmonize=True,
        **kwdargs,
    )

    return


#############################################
#############################################
#       ptA and ptB
#############################################


def _ptAB(coll, key, ptA, ptB):

    # -----------------
    # available devices
    # -----------------

    wdev = coll._which_device
    lok = list(coll.dobj.get(wdev, {}))

    if ptA is not None:
        ptA = ds._generic_check._check_var(
            ptA, 'ptA',
            types=str,
            allowed=lok,
        )

    if ptB is not None:
        ptB = ds._generic_check._check_var(
            ptB, 'ptB',
            types=str,
            allowed=lok,
        )

    return ptA, ptB


#############################################
#############################################
#       identifiers
#############################################


def _kwdargs(coll, key, kwdargs):

    for k0, v0 in _def_dict.get_def().items():

        # type checking + default
        kwdargs[k0] = ds._generic_check._check_var(
            kwdargs.get(k0), k0,
            types=v0.get('types'),
            default=v0.get('def'),
        )

        # as type
        if v0.get('astype') is not None:
            kwdargs[k0] = eval(f"{v0['astype']}({kwdargs[k0]})")

        # can be None
        wcon = coll._which_connector
        if v0.get('can_be_None') is False and kwdargs[k0] is None:
            msg = (
                "For {wcon} '{key}', arg '{k0}' must be provided!"
            )
            raise Exception(msg)

    return kwdargs