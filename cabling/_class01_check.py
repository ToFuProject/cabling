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