# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:31:37 2024

@author: dvezinet
"""


import warnings


import datastock as ds


from . import _class00_def_dict as _def_dict


#############################################
#############################################
#       connector type
#############################################


def connector_type(
    coll=None,
    key=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    wcont = coll._which_connector_type
    lout = list(coll.dobj.get(wcont, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _kwdargs(
        coll,
        key,
        kwdargs,
        defdict=_def_dict.get_connector_type_kwdargs(),
    )

    # ---------------------
    # store
    # ---------------------

    coll.add_obj(
        which=wcont,
        key=key,
        harmonize=True,
        **kwdargs,
    )

    return


#############################################
#############################################
#       connector model
#############################################


def connector_model(
    coll=None,
    key=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    wcont = coll._which_connector_type
    lout = list(coll.dobj.get(wcont, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _kwdargs(
        coll,
        key,
        kwdargs,
        defdict=_def_dict.get_connector_model_kwdargs(),
    )

    # ---------------------
    # store
    # ---------------------

    coll.add_obj(
        which=wcont,
        key=key,
        harmonize=True,
        **kwdargs,
    )

    return


#############################################
#############################################
#       connector
#############################################


def connector(
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

    ptA, ptB = _ptAB(coll, key, ptA, ptB)

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _kwdargs(
        coll,
        which=wcon,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_kwdargs(),
    )

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


def _kwdargs(coll, which=None, key=None, kwdargs=None, defdict=None):

    # -----------------------
    # loop on default kwdargs
    # -----------------------

    for k0, v0 in defdict.items():

        # -----------------------
        # type checking + default

        kwdargs[k0] = ds._generic_check._check_var(
            kwdargs.get(k0), k0,
            types=v0.get('types'),
            default=v0.get('def'),
        )

        # -----------
        # as type

        if v0.get('astype') is not None:
            kwdargs[k0] = eval(f"{v0['astype']}({kwdargs[k0]})")

        # -----------------
        # can be None ?

        wcon = coll._which_connector
        if v0.get('can_be_None') is False and kwdargs[k0] is None:
            msg = (
                f"For {wcon} '{key}', arg '{k0}' must be provided!"
            )
            raise Exception(msg)

        # ----------
        # unique

        if v0.get('unique') is True and kwdargs[k0] is not None:
            lv = [
                k1 for k1, v1 in coll.dobj[which].items()
                if v1[k0] == kwdargs[k0]
            ]
            if len(lv) > 0:
                msg = (
                    f"Arg for {which} '{key}', attribute '{k0}' must be unique!\n"
                    f"\t- Provided: {kwdargs[k0]}\n"
                    f"\t- already exists in {which} {lv}\n"
                )
                raise Exception(msg)

        # ---------------
        # unique_all

        if v0.get('unique_all') is True and kwdargs[k0] is not None:
            dv = {
                ww: [
                    k1 for k1, v1 in coll.dobj[ww].items()
                    if v1[k0] == kwdargs[k0]
                ]
                for ww in coll.dobj.keys()
            }
            dv = {kw: vw for kw, vw in dv.items() if len(vw) > 0}
            if len(dv) > 0:
                lstr = [f"\t\t- {kw}: {vw}" for kw, vw in dv.items()]
                msg = (
                    f"Arg for {which} '{key}', attribute '{k0}' must be unique!\n"
                    f"\t- Provided: {kwdargs[k0]}\n"
                    f"\t- already exists in:\n{lstr}\n"
                )
                raise Exception(msg)

        # ---------------
        # refer to other which

        if v0.get('unique_all') is not None:

            w2 = v0.get('unique_all')
            if w2 not in coll.dobj.keys():
                msg = (
                    "Unknow which: {w2}\n"
                )
                warnings.warn(msg)

            else:
                if kwdargs[k0] not in coll.dobj[w2].keys():
                    msg = (
                        f"{which} '{key}' refers to unknwown {w2}: {kwdargs[k0]}\n"
                    )
                    raise Exception(msg)

    return kwdargs