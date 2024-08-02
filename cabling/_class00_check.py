# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:31:37 2024

@author: dvezinet
"""


import copy
import warnings


import datastock as ds


from . import _class00_def_dict as _def_dict


#############################################
#############################################
#       plug type
#############################################


def plug_type(
    coll=None,
    key=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    wcont = coll._which_plug_type
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
        coll=coll,
        which=wcont,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_plug_type_kwdargs(),
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
#       connector family
#############################################


def connector_family(
    coll=None,
    key=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    wcont = coll._which_connector_family
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
        coll=coll,
        which=wcont,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_connector_family_kwdargs(),
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
#       connector type
#############################################


def connector_type(
    coll=None,
    key=None,
    connections=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    which = coll._which_connector_type
    lout = list(coll.dobj.get(which, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _kwdargs(
        coll=coll,
        which=which,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_connector_type_kwdargs(),
    )

    # ---------------------
    # connection plug types
    # ---------------------

    _check_connections_types(
        coll=coll,
        which=which,
        key=key,
        connections=connections,
        lcon=['ptA', 'ptB'],
    )

    # ---------------------
    # store
    # ---------------------

    coll.add_obj(
        which=which,
        key=key,
        harmonize=True,
        **kwdargs,
    )

    return


#############################################
#############################################
#       connections type
#############################################


def _check_connections_types(
    coll=None,
    which=None,
    key=None,
    connections=None,
    lcon=None,
):

    # ----------------
    # preliminary
    # ----------------

    # list of keys
    wplug = coll._which_plug_type
    if not isinstance(connections, dict):
        _err_connections(which, key, connections, wplug)

    if lcon is None:
        lcon = list(connections.keys())

    # ----------------
    # plug types
    # ----------------

    lok = sorted(coll.dobj[wplug].keys())
    c0 = all([
        isinstance(connections.get(pt), dict)
        and connections[pt].get(wplug) in lok
        for pt in lcon
    ])
    if not c0:
        _err_connections(which, key, connections, wplug, lok, lcon)

    return


def _err_connections(which, key, connections, wplug, lok=[], lcon=[]):
    lstr = [f"\t- '{cc}': '{wplug}': <a known '{wplug}'>\n" for cc in lcon]
    msg = (
        f"{which} '{key}' must be provided with a 'connections' dict:\n"
        + "\n".join(lstr)
    )
    if len(lok) > 0:
        msg += f"Available '{wplug}':\n\t{lok}\n"
    msg += f"Provided:\n{connections}"
    raise Exception(msg)


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

    wcont = coll._which_connector_model
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
        coll=coll,
        which=wcont,
        key=key,
        kwdargs=kwdargs,
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
    consistency=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    # key
    wcon = coll._which_connector
    lout = list(coll.dobj.get(wcon, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # consistency
    consistency = ds._generic_check._check_var(
        consistency, 'consistency',
        types=bool,
        default=True,
    )

    # ---------------------
    # ptA, ptB
    # ---------------------

    _ptAB(coll, key, ptA, ptB)

    # update connections
    wcm = coll._which_connector_model
    wdev = coll._which_device
    kcm = kwdargs[wcm]
    connections = copy.deepcopy(coll.dobj[wcm][kcm]['connections'])
    connections['ptA'][wdev] = ptA
    connections['ptB'][wdev] = ptB

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _kwdargs(
        coll=coll,
        which=wcon,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_connector_kwdargs(),
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

    # --------------------
    # consistency check
    # --------------------

    if consistency is True:

        coll.check_consistency(
            verb=None,
            returnas=None,
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

    din = {'ptA': ptA, 'ptB': ptB}
    for pt in ['ptA', 'ptB']:

        if din[pt] is not None:

            c0 = (
                isinstance(din[pt], tuple)
                and len(din[pt]) == 2
                and all([isinstance(ss, str) for ss in din[pt]])
            )

            if not c0:
                msg = (
                    "Arg 'ptA' and 'ptB' must each be tuple of the form:\n"
                    "(<device name>, <plug name>)\n"
                    f"Provided '{pt}': {din[pt]}"
                )
                raise Exception(msg)

    return ptA, ptB


#############################################
#############################################
#       identifiers
#############################################


def _kwdargs(coll, which=None, key=None, kwdargs=None, defdict=None):

    if kwdargs is None:
        kwdargs = {}

    # -----------------------
    # loop on default kwdargs
    # -----------------------

    for k0, v0 in defdict.items():

        # -----------------------
        # type checking + default

        if v0.get('can_be_None') is False:
            kwdargs[k0] = ds._generic_check._check_var(
                kwdargs.get(k0), k0,
                types=v0.get('types'),
                default=v0.get('def'),
            )
        elif kwdargs.get(k0) is None:
            continue

        # -----------
        # as type

        if v0.get('astype') is not None:
            kwdargs[k0] = v0['astype'].__class__(kwdargs[k0])

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

        w2 = v0.get('which')
        if w2 is not None:

            if isinstance(w2, str):
                w2 = (w2,)

            for ww in w2:
                if ww not in coll.dobj.keys():
                    msg = (
                        "Unknow which: {ww}\n"
                    )
                    warnings.warn(msg)

                else:
                    kwdargs[ww] = kwdargs.get(ww)
                    if kwdargs[ww] is not None:
                        if kwdargs[ww] not in coll.dobj[ww].keys():
                            msg = (
                                f"{which} '{key}' refers to unknwown {ww}: "
                                f"{kwdargs[k0]}\n"
                            )
                            raise Exception(msg)

    return kwdargs