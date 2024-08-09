# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 18:24:45 2024

@author: dvezinet
"""


import itertools as itt


import numpy as np
import pandas as pd
import datastock as ds


# ############################################################
# ############################################################
#              Main
# ############################################################


def main(
    coll=None,
    # which devices to plot
    which=None,
    keys=None,
):

    # ---------------
    # check
    # ---------------

    which, keys, dwhich = _check(
        coll=coll,
        which=which,
        keys=keys,
    )

    # ---------------
    # select devices and connectors
    # ---------------

    dout = _DataFrame(
        coll=coll,
        which=which,
        keys=keys,
        dwhich=dwhich,
    )

    return dout


# ############################################################
# ############################################################
#              check inputs
# ############################################################


def _check(
    coll=None,
    # naming
    which=None,
    keys=None,
):

    # ---------------
    # which
    # ---------------

    lok = list(coll.dobj.keys())
    which = ds._generic_check._check_var(
        which, 'which',
        types=str,
        allowed=lok,
    )

    # ---------------
    # keys
    # ---------------

    if isinstance(keys, str):
        keys = [keys]

    lok = list(coll.dobj.get(which, {}).keys())
    keys = list(ds._generic_check._check_var_iter(
        keys, 'keys',
        types=(list, tuple),
        types_iter=str,
        allowed=lok,
    ))

    # ---------------
    # dwhich
    # ---------------

    dwhich = {
        'plug_type': coll._which_plug_type,
        'connector_type': coll._which_connector_type,
        'connector_model': coll._which_connector_model,
        'connector': coll._which_connector,
        'device_type': coll._which_device_type,
        'device_model': coll._which_device_model,
        'device': coll._which_device,
    }

    return which, keys, dwhich


# ############################################################
# ############################################################
#              Select
# ############################################################


def _DataFrame(
    coll=None,
    which=None,
    keys=None,
    dwhich=None,
):

    # ---------------
    # plug types
    # ---------------

    if which == dwhich['plug_type']:
        dout = _get_plug_type(coll, which, keys)

    elif which == dwhich['connector_type']:
        dout = _get_connector_type(coll, which, keys)

    elif which == dwhich['connector_model']:
        dout = _get_connector_model(coll, which, keys)

    elif which == dwhich['connector']:
        dout = _get_connector(coll, which, keys)

    elif which == dwhich['device_type']:
        dout = _get_device_type(coll, which, keys)

    elif which == dwhich['device_model']:
        dout = _get_device_model(coll, which, keys)

    elif which == dwhich['device']:
        dout = _get_device(coll, which, keys)

    # ---------------
    # to DataFrame
    # ---------------

    for k0, v0 in dout.items():
        dout[k0] = pd.DataFrame.from_dict(v0, orient='index')

    return dout


# ############################################################
# ############################################################
#              plug_type
# ############################################################


def _get_plug_type(coll, which, keys):

    # -----------------
    #  prepare
    # -----------------

    dobj = coll.dobj[which]
    dout = {which: {}}

    # -----------------
    #  generic
    # -----------------

    _generic_fields(
        dout, dobj, which, keys,
        lparam=coll.get_lparam(which),
        lout=['doptions'],
    )

    # -------------
    # options
    # -------------

    for key in keys:

        options = dobj[key].get('doptions')
        options = '' if options is None else sorted(options.keys())
        dout[which][key]['options'] = options

    # ---------------
    # unique options
    # ---------------

    options_unique = list(set(itt.chain.from_iterable([
        list(dobj[k0]['doptions'].keys())
        for k0 in keys
        if dobj[k0].get('doptions') is not None
    ])))

    nopt = len(options_unique)

    return dout


# ############################################################
# ############################################################
#              connector_type
# ############################################################


def _get_connector_type(coll, which, keys):

    # -----------------
    #  prepare
    # -----------------

    dobj = coll.dobj[which]
    dout = {which: {}}

    # -----------------
    #  generic
    # -----------------

    _generic_fields(
        dout, dobj, which, keys,
        lparam=coll.get_lparam(which),
        lout=['nb connector_model'],
    )

    return dout


# ############################################################
# ############################################################
#              connector_model
# ############################################################


def _get_connector_model(coll, which, keys):

    # -----------------
    #  prepare
    # -----------------

    dobj = coll.dobj[which]
    wplug = coll._which_plug_type
    dout = {which: {}}

    # -----------------
    #  generic
    # -----------------

    _generic_fields(
        dout, dobj, which, keys,
        lparam=coll.get_lparam(which),
        lout=['nb connector', 'connections'],
    )

    # --------------
    # connections
    # --------------

    for key in keys:

        dout[which][key]['ptA'] = dobj[key]['connections']['ptA'][wplug]['key']
        dout[which][key]['ptB'] = dobj[key]['connections']['ptB'][wplug]['key']

    return dout


# ############################################################
# ############################################################
#              connector
# ############################################################


def _get_connector(coll, which, keys):

    # -----------------
    #  prepare
    # -----------------

    dobj = coll.dobj[which]
    wdev = coll._which_device
    dout = {which: {}}

    # -----------------
    #  generic
    # -----------------

    _generic_fields(
        dout, dobj, which, keys,
        lparam=coll.get_lparam(which),
        lout=['connections'],
    )

    # --------------
    # connections
    # --------------

    for key in keys:

        dout[which][key]['ptA'] = dobj[key]['connections']['ptA'][wdev]
        dout[which][key]['ptB'] = dobj[key]['connections']['ptB'][wdev]

    return dout


# ############################################################
# ############################################################
#              device_type
# ############################################################


def _get_device_type(coll, which, keys):

    # -----------------
    #  prepare
    # -----------------

    dobj = coll.dobj[which]
    wdm = coll._which_device_model
    dout = {which: {}}

    # -----------------
    #  generic
    # -----------------

    _generic_fields(
        dout, dobj, which, keys,
        lparam=coll.get_lparam(which),
        lout=[f'nb {wdm}'],
    )

    return dout


# ############################################################
# ############################################################
#              device_model
# ############################################################


def _get_device_model(coll, which, keys):

    # -----------------
    #  prepare
    # -----------------

    wplug = coll._which_plug_type
    dobj = coll.dobj[which]
    wdev = coll._which_device
    dout = {which: {}}

    # -----------------
    #  generic
    # -----------------

    _generic_fields(
        dout, dobj, which, keys,
        lparam=coll.get_lparam(which),
        lout=[f'nb {wdev}', 'connections'],
    )

    # --------------
    # connections
    # --------------

    dncon = {key: len(dobj[key]['connections']) for key in keys}
    nconmax = np.max([vv for vv in dncon.values()])

    for key in keys:

        dcon = dobj[key]['connections']
        for kcon in sorted(dcon.keys()):
            out = (dcon[kcon]['name'], dcon[kcon][wplug]['key'])
            if out is None:
                out = dcon[kcon]['flag']
            dout[which][key][kcon] = str(out)

        for ii in range(dncon[key], nconmax):
            dout[which][key][f'con{ii}'] = ''

    return dout


# ############################################################
# ############################################################
#              device
# ############################################################


def _get_device(coll, which, keys):

    # -----------------
    #  prepare
    # -----------------

    wcon = coll._which_connector
    dobj = coll.dobj[which]
    dout = {which: {}}

    # -----------------
    #  generic
    # -----------------

    _generic_fields(
        dout, dobj, which, keys,
        lparam=coll.get_lparam(which),
        lout=['connections'],
    )

    # --------------
    # connections
    # --------------

    dncon = {key: len(dobj[key]['connections']) for key in keys}
    nconmax = np.max([vv for vv in dncon.values()])

    for key in keys:

        dcon = dobj[key]['connections']
        for kcon in sorted(dcon.keys()):
            out = dcon[kcon].get(wcon)
            if out is None:
                out = dcon[kcon]['flag']
            dout[which][key][kcon] = str(out)

        for ii in range(dncon[key], nconmax):
            dout[which][key][f'con{ii}'] = ''

    return dout


# ############################################################
# ############################################################
#              get field
# ############################################################


def _generic_fields(dout, dobj, which, keys, lparam, lout):

    # -----------
    # generic
    # -----------

    for key in keys:

        # generic
        dout[which][key] = {
            pp: dobj[key][pp]
            for pp in lparam if pp not in lout + ['systems']
        }

    # -------------
    # systems
    # -------------

    if 'systems' in lparam:

        LNu = sorted(set(itt.chain.from_iterable([
            list(dobj[key]['systems'].keys()) for key in keys
        ])))

        for key in keys:
            for sys in LNu:
                dout[which][key][sys] = dobj[key]['systems'].get(sys, '')

    return


# ############################################################
# ############################################################
#             systems breakdown
# ############################################################


def _systems(dobj, keys):

    # ---------------
    # Unique systems
    # ---------------


    # ---------------
    # dict of systems
    # ---------------

    dsys = {}
    for k0 in keys:

        pass

    return dsys, keys