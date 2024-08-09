# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:31:37 2024

@author: dvezinet
"""


import copy
import warnings


import datastock as ds


from . import _class00_def_dict as _def_dict
from . import _class00_connections as _connections



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

    kwdargs = _kwdargs(
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

    kwdargs = _kwdargs(
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

    kwdargs = _kwdargs(
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

    kwdargs = _kwdargs(
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
    consistency=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    which = coll._which_connector
    systems, key, label = _systems(coll, systems, which, label, key)

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

    kwdargs = _kwdargs(
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
    # store
    # ---------------------

    coll.add_obj(
        which=which,
        key=key,
        systems=systems,
        label=label,
        connections=connections,
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
                extra_msg=f"For {which} '{key}', arg '{k0}' must be provided!",
            )

        elif kwdargs.get(k0) is None:
            continue

        elif kwdargs.get(k0) is not None:
            kwdargs[k0] = ds._generic_check._check_var(
                kwdargs.get(k0), k0,
                types=v0.get('types'),
                default=v0.get('def'),
            )

        # -----------
        # as type

        if v0.get('astype') is not None:
            kwdargs[k0] = v0['astype'](kwdargs[k0])

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
                        "Error defining {which} '{key}':"
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


# ###########################################################
# ###########################################################
#                 Systems
# ###########################################################


def _systems(coll, systems, which, label, key):

    # ----------------
    # check systems
    # ----------------

    c0 = (
        isinstance(systems, dict)
        and all([
            isinstance(k0, str)
            and isinstance(v0, str)
            for k0, v0 in systems.items()
        ])
    )

    if not c0:
        msg = (
            f"{which} '{label}' arg 'systems' must be a dict of:\n"
            f"\t- str (system level): str (value)\n"
            "e.g.: {'L1': 'DIAG', 'L2': 'XRAY', ...}n"
            f"Provided:\n{systems}\n"
        )
        raise Exception(msg)

    # ----------------
    # make key_sys (from sys+label)
    # ----------------

    label = ds._generic_check._check_var(
        label, 'label',
        types=str,
    )

    # derive key
    lsys = [
        systems[ksys] for ksys in coll._systems_key
        if systems.get(ksys) is not None
    ]
    key_sys = "_".join(lsys + [label])

    # -----------------
    # key
    # ----------------

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
        key = key_sys

    else:
        key = ds._generic_check._check_var(
            key, 'key',
            types=str,
            excluded=lout,
        )

    return systems, key, label