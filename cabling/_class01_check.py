# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:31:37 2024

@author: dvezinet
"""


import copy
import datastock as ds


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

    connections = _class00_check._check_connections_types(
        coll=coll,
        which=which,
        key=key,
        connections=connections,
        lcon=None,
    )

    # ---------------------
    # connection nb
    # ---------------------

    connections = _connections_nb(
        coll=coll,
        which=which,
        key=key,
        connections=connections,
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


#######################
#######################
#    connections nb
#######################


def _connections_nb(
    coll=None,
    which=None,
    key=None,
    connections=None,
):

    # -------------
    # prepare
    # -------------

    lcon = list(connections.keys())

    # -------------
    # derive
    # -------------

    dout = {}
    for k0 in lcon:

        dcon = connections[k0]
        nb = dcon.get('nb')
        if nb is None or nb == 1:
            dout[k0] = {k1: v1 for k1, v1 in dcon.items() if k1 != 'nb'}

        else:

            if not (isinstance(nb, int) and nb > 1):
                msg = "Arg nb must be a strictly positive integer"
                raise Exception(msg)

            for i1 in range(nb):
                keyi = f"{k0}_{i1}"
                dout[keyi] = {k1: v1 for k1, v1 in dcon.items() if k1 != 'nb'}

    return dout


#############################################
#############################################
#       device
#############################################


def device(
    coll=None,
    key=None,
    systems=None,
    label=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    which = coll._which_device
    systems, keysys, label = _class00_check._systems(systems, which, label)

    # key
    lout = list(coll.dobj.get(which, {}).keys())
    if key is None:
        if key in lout:
            msg = (
                f"For {which} '{label}', the generated key already exists!\n"
                f"\t- systems: {systems}\n"
                f"\t- label: {label}\n"
                f"\t- generated key: {key}\n"
                "=> change label?\n"
            )
            raise Exception(msg)
        key = keysys

    else:
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
        harmonize=True,
        **kwdargs,
    )

    return