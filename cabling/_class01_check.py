# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:31:37 2024

@author: dvezinet
"""


import copy


import numpy as np
import datastock as ds


from . import _class00_connections
from . import _class00_check
from . import _class01_def_dict as _def_dict


#############################################
#############################################
#       device_type
#############################################


def device_type(
    coll=None,
    key=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    which = coll._which_device_type
    lout = list(coll.dobj.get(which, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _class00_check._kwdargs(
        coll=coll,
        which=which,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_device_type_kwdargs(),
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
#       device_model
#############################################


def device_model(
    coll=None,
    key=None,
    connections=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    which = coll._which_device_model
    lout = list(coll.dobj.get(which, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ---------------------
    # connection plug types
    # ---------------------

    connections = _class00_connections._check_connections_types(
        coll=coll,
        which=which,
        key=key,
        connections=connections,
        lcon=None,
    )

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _class00_check._kwdargs(
        coll=coll,
        which=which,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_device_type_kwdargs(),
    )

    # ---------------------
    # store
    # ---------------------

    coll.add_obj(
        which=which,
        key=key,
        connections=connections,
        harmonize=True,
        **kwdargs,
    )

    return


#############################################
#############################################
#       device
#############################################


def device(
    coll=None,
    key=None,
    systems=None,
    label=None,
    dcoords=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    which = coll._which_device
    systems, key, label = _class00_check._systems(
        coll, systems, which, label, key,
    )

    # ---------------------
    # dcoords
    # ---------------------

    dcoords = _dcoords(coll, which, key, dcoords)

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _class00_check._kwdargs(
        coll=coll,
        which=which,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_device_kwdargs(),
    )

    # ---------------------
    # connections, copy from model
    # ---------------------

    wdm = coll._which_device_model
    key_model = kwdargs[wdm]
    connections = copy.deepcopy(coll.dobj[wdm][key_model]['connections'])

    # ---------------------
    # store
    # ---------------------

    coll.add_obj(
        which=which,
        key=key,
        label=label,
        systems=systems,
        connections=connections,
        dcoords=dcoords,
        harmonize=True,
        **kwdargs,
    )

    return


#############################################
#############################################
#       coordinates
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

            if sorted(dcoords[k0].keys()) != lok:
                _dcoords_err(which, key, dcoords, k0, lok)

    return dcoords


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