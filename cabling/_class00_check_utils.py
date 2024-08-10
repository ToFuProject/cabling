# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 14:39:36 2024

@author: dvezinet
"""


import warnings


import datastock as ds


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