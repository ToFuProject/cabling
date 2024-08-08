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
    which=None,
    key=None,
    doptions=None,
):

    # -----------------
    # trivial
    # -----------------

    if doptions is None:
        dout = None

    else:

        # --------------
        # conformity check
        # --------------

        c0 = (
            isinstance(doptions, dict)
            and all([
                isinstance(k0, str)
                and isinstance(v0, (list, tuple))
                or (
                    isinstance(v0, dict)
                    and isinstance(v0.get('values'), (list, tuple))
                )
                for k0, v0 in doptions.items()
            ])
        )

        if not c0:
            if isinstance(doptions, dict):
                lstr = "\n".join([
                    f"\t- '{k0}': {v0}" for k0, v0 in doptions.items()
                ])

            else:
                lstr = str(doptions)

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

    connections = _check_connections_types(
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
        and (
                (
                    isinstance(connections[pt].get(wplug), str)
                    and connections[pt][wplug] in lok
                )
            or (
                isinstance(connections[pt].get(wplug), dict)
                and connections[pt][wplug]['key'] in lok
            )
        )
        for pt in lcon
    ])
    if not c0:
        _err_connections(which, key, connections, wplug, lok, lcon)

    # ------------
    # plug options
    # -------------

    dout = {}
    for pt in lcon:

        dout[pt] = {
            wplug: {},
            **{k1: v1 for k1, v1 in connections[pt].items() if k1 != wplug}
        }

        if isinstance(connections[pt].get(wplug), str):
            dout[pt][wplug] = {'key': connections[pt][wplug]}

        else:
            for k1, v1 in connections[pt][wplug].items():

                if k1 == 'key':
                    dout[pt][wplug]['key'] = v1

                # ---------------
                # options

                else:

                    plug_type = connections[pt][wplug]['key']
                    dplug = coll.dobj[wplug][plug_type].get('doptions')

                    if k1 not in dplug.keys():
                        msg = (
                            f"For {which} '{key}', arg connections must have "
                            "options known to the associated {wplug}:\n"
                            f"\t- {plug_type} has options: {sorted(dplug.keys())}\n"
                            f"Provided:\n{k1}"
                        )
                        raise Exception(msg)

                    if v1 not in dplug[k1]:
                        msg = (
                            f"For {which} '{key}', arg connections must have "
                            "options known to the associated {wplug}:\n"
                            f"\t- plug_type: {plug_type}\n"
                            f"\t- option: {k1}\n"
                            f"\t- available values: {dplug[k1]}\n"
                            f"Provided:\n\t{v1}"
                        )
                        raise Exception(msg)

                    dout[pt][wplug][k1] = v1

    return dout


def _err_connections(which, key, connections, wplug, lok=[], lcon=None):

    # initialize msg
    msg = (
        f"{which} '{key}' must be provided with a 'connections' dict:\n"
    )

    # add connections
    if lcon is not None:
        lstr = [
            f"\t- '{cc}': '{wplug}': {connections.get(cc)}\n"
            for cc in lcon
            if connections.get(cc, {}).get(wplug) not in lok
        ]
        msg += "\n".join(lstr)

        # available
        msg += f"\nAvailable '{wplug}':\n\t{lok}\n\n"

    # Provided
    msg += f"Provided:\n\t{connections}"
    raise Exception(msg)


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
    which = coll._which_connector
    lout = list(coll.dobj.get(which, {}).keys())
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

    ptA, ptB = _ptAB(coll, which, key, ptA, ptB)

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
#       ptA and ptB
#############################################


def _ptAB(coll, which, key, ptA, ptB):

    # -----------------
    # available devices
    # -----------------

    wdev = coll._which_device
    lok = list(coll.dobj.get(wdev, {}))

    din = {'ptA': ptA, 'ptB': ptB}
    for pt in ['ptA', 'ptB']:

        if din[pt] is not None:

            # -----------------------
            # check format

            c0 = (
                isinstance(din[pt], (list, tuple))
                and len(din[pt]) == 2
                and all([isinstance(ss, str) for ss in din[pt]])
            )

            # raise error if needed
            if not c0:
                msg = (
                    f"For {which} '{key}', "
                    "arg '{pt}' must be a tuple of the form:\n"
                    "(<device name>, <plug name>)\n"
                    f"Provided '{pt}': {din[pt]}"
                )
                raise Exception(msg)

            # -----------------------
            # check existence of pts

            if din[pt][0] not in lok:
                msg = (
                    f"For {which} '{key}', wrong first term in arg '{pt}':\n"
                    f"\t- Unknwon {wdev}: '{din[pt][0]}'\n"
                )
                raise Exception(msg)

            if din[pt][1] not in coll.dobj[wdev][din[pt][0]]['connections'].keys():
                msg = (
                    f"For {which} '{key}', wrong second term in arg '{pt}':\n"
                    f"\t- Unknwon {wdev} connection: '{din[pt][1]}'\n"
                )
                raise Exception(msg)

    return tuple(ptA), tuple(ptB)


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

        # --------------
        # special cases

        if k0 == 'systems':
            kwdargs[k0] = _systems(kwdargs.get(k0), which, key)
            continue

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
            kwdargs[k0] = v0['astype'](kwdargs[k0])

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


def _systems(systems, which, key):

    if systems is not None:

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
                f"{which} '{key}' arg 'systems' must be a dict of:\n"
                f"\t- str (system level): str (value)\n"
                "e.g.: {'L1': 'DIAG', 'L2': 'XRAY', ...}n"
                f"Provided:\n{systems}\n"
            )
            raise Exception(msg)

    return systems