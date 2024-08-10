# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:31:37 2024

@author: dvezinet
"""


import copy


import datastock as ds


from . import _class00_def_dict as _def_dict
from . import _class00_check_utils as _check_utils
from . import _class00_connections as _connections
from . import _class00_check_coords as _check_coords



#############################################
#############################################
#       plug options
#############################################


def plug_options(
    coll=None,
    key=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    which = coll._which_plug_option
    lout = list(coll.dobj.get(which, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ---------------------
    # kwdargs
    # ---------------------

    # ----------------
    # check for type

    for k0, v0 in kwdargs.items():
        if v0 in ['float', 'int']:
            kwdargs[k0] = eval(v0)

    kwdargs = _check_utils._kwdargs(
        coll=coll,
        which=which,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_plug_options_kwdargs(),
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
#       plug type
#############################################


def plug_type(
    coll=None,
    key=None,
    doptions=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    which = coll._which_plug_type
    lout = list(coll.dobj.get(which, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ---------------------
    # options
    # ---------------------

    doptions = _options(
        coll=coll,
        which=which,
        key=key,
        doptions=doptions,
    )

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs =_check_utils._kwdargs(
        coll=coll,
        which=which,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_plug_type_kwdargs(),
    )

    # ---------------------
    # store
    # ---------------------

    coll.add_obj(
        which=which,
        key=key,
        doptions=doptions,
        harmonize=True,
        **kwdargs,
    )

    return


# ####################
# Plug type options
# ####################


def _options(
    coll=None,
    which=None,
    key=None,
    doptions=None,
):

    wpo = coll._which_plug_option
    lok = list(coll.dobj.get(wpo, {}).keys())

    # -----------------
    # trivial
    # -----------------

    if doptions is None:
        dout = None

    elif not isinstance(doptions, dict):
        _options_err(which, key, '')

    # --------------
    # conformity check
    # --------------

    else:

        dkout = {
            k0: v0
            for k0, v0 in doptions.items()
            if not (
                isinstance(k0, str)
                and k0 in lok
                and (
                    (
                        isinstance(coll.dobj[wpo][k0]['values'], (list, tuple))
                        and v0 in coll.dobj[wpo][k0]['values']
                    )
                    or (
                        isinstance(coll.dobj[wpo][k0]['values'], type)
                        and isinstance(v0, coll.dobj[wpo][k0]['values'])
                    )
                )
            )
        }


        if len(dkout) > 0:
            lstr = "\n".join([
                f"\t- '{k0}': {v0}" for k0, v0 in doptions.items()
            ])

            lstr = str(doptions)
            _options_err(which, key, lstr)

        # ---------------
        # standardization
        # ---------------

        dout = {}
        for k0, v0 in doptions.items():

            if isinstance(v0, (list, tuple)):
                dout[k0] = {
                    'values': tuple(v0),
                    'description': '',
                }

            else:
                dout[k0] = {
                    'values': tuple(v0['values']),
                    'description': v0.get('description'),
                    'units': v0.get('units'),
                }

    return dout


def _options_err(which, key, lstr):
    msg = (
        f"For {which} '{key}', arg doption must be a dict of:\n"
        f"\t- 'option0': list if possible values or dict\n"
        f"\t- ...      : list if possible values or dict\n"
        f"\t- 'optionN': list if possible values or dict\n\n"
        "If a dict is provided for each options, it should be:\n"
        + "{'values': list of possible values, 'description': str}\n\n"
        + f"Provided:\n{lstr}"
    )
    raise Exception(msg)


#############################################
#############################################
#       connector family
#############################################


def connector_type(
    coll=None,
    key=None,
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

    kwdargs = _check_utils._kwdargs(
        coll=coll,
        which=which,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_connector_type_kwdargs(),
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
#       connector type
#############################################


def connector_model(
    coll=None,
    key=None,
    connections=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    # key
    which = coll._which_connector_model
    lout = list(coll.dobj.get(which, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _check_utils._kwdargs(
        coll=coll,
        which=which,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_connector_model_kwdargs(),
    )

    # ---------------------
    # connection plug types
    # ---------------------

    connections = _connections._check_connections_types(
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
        connections=connections,
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
    systems=None,
    key=None,
    label=None,
    ptA=None,
    ptB=None,
    dcoords=None,
    consistency=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    which = coll._which_connector
    systems, key, label = _check_utils._systems(coll, systems, which, label, key)

    # -------------
    # consistency
    # -------------

    consistency = ds._generic_check._check_var(
        consistency, 'consistency',
        types=bool,
        default=True,
    )

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _check_utils._kwdargs(
        coll=coll,
        which=which,
        key=key,
        kwdargs=kwdargs,
        defdict=_def_dict.get_connector_kwdargs(),
    )

    # ---------------------
    # ptA, ptB
    # ---------------------

    ptA, ptB = _connections._ptAB(coll, which, key, ptA, ptB, systems)

    # update connections
    wcm = coll._which_connector_model
    wdev = coll._which_device
    kcm = kwdargs[wcm]
    connections = copy.deepcopy(coll.dobj[wcm][kcm]['connections'])
    connections['ptA'][wdev] = ptA
    connections['ptB'][wdev] = ptB

    # update device connections
    coll.dobj[wdev][ptA[0]]['connections'][ptA[1]][which] = (key, 'ptA')
    coll.dobj[wdev][ptB[0]]['connections'][ptB[1]][which] = (key, 'ptB')

    # ---------------------
    # dcoords
    # ---------------------

    dcoords = _check_coords._dcoords(coll, which, key, dcoords)

    # ---------------------
    # store
    # ---------------------

    coll.add_obj(
        which=which,
        key=key,
        systems=systems,
        label=label,
        connections=connections,
        dcoords=dcoords,
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