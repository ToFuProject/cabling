# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 11:13:37 2024

@author: dvezinet
"""


#############################################
#############################################
#       main
#############################################


#############################################
#############################################
#       main
#############################################


def main(
    coll=None,
):

    # --------------
    # prepare
    # --------------

    wcon = coll._which_connector
    wdev = coll._which_device
    wplug = coll._which_plug_type

    # --------------
    # check devices
    # --------------

    ddev = _connections(
        coll=coll,
        which0=wdev,
        which1=wcon,
        wplug=wplug,
    )

    # --------------
    # check connectors
    # --------------

    dcon = _connections(
        coll=coll,
        which0=wcon,
        which1=wdev,
        wplug=wplug,
    )

    # --------------
    # return
    # --------------

    return {
        wdev: ddev,
        wcon: dcon,
    }


#############################################
#############################################
#       check connections
#############################################


def _connections(
    coll=None,
    which0=None,
    which1=None,
    wplug=None,
):

    # -------------
    # initialize
    # -------------

    dout = {
        'lunique': [],
        'ok': {},
        'err': {},
        'loose': {},
        'multi': {},
        'unknown': {},
        'type_wrong': {},
        'specs_wrong': {},
        'specs_missing': {},
    }

    # --------------
    # loop
    # --------------

    lk0 = list(coll.dobj.get(which0, {}).keys())
    lk1 = list(coll.dobj.get(which1, {}).keys())
    for key in lk0:

        dcon = coll.dobj[which0][key]['connections']

        for k0, v0 in dcon.items():

            # ----------
            # loose end

            if v0.get(which1) is None:
                kflag = 'loose'
                _set_flag(dout, key, kflag, k0, True)

            # -----------------
            # error (not a tuple of 2 str)

            elif not (
                    isinstance(v0[which1], tuple)
                    and len(v0[which1]) == 2
                    and all([isinstance(ss, str) for ss in v0[which1]])
                ):
                kflag = 'err'
                _set_flag(dout, key, kflag, k0, v0[which1])

            else:

                k1, v1 = v0[which1]

                # ------------
                # unknown end - level 1: which

                if k1 not in lk1:
                    kflag = 'unknown'
                    _set_flag(dout, key, kflag, k0, f"{which1}: '{k1}'")

                # ------------
                # unknown end - level 2: plug

                elif v1 not in coll.dobj[which1][k1]['connections'].keys():
                    kflag = "unknown"
                    _set_flag(dout, key, kflag, k0, f"plug of {which1} '{k1}': {v1}")

                # -------------
                # redundant end

                elif v0[which1] in dout['lunique']:
                    kflag = 'multi'
                    _set_flag(dout, key, kflag, k0, v0[which1])

                # ------------------
                # ok => mark as done

                else:

                    dout['lunique'].append(v0[which1])

                    # -------------------------------------
                    # check matching plug types and options

                    k1, v1 = v0[which1]

                    con_flag, con_val = _plug_types(
                        coll=coll,
                        which0=which0,
                        which1=which1,
                        key0=key,
                        key1=k1,
                        con0=k0,
                        con1=v1,
                        v0=v0,
                        v1=coll.dobj[which1][k1]['connections'][v1],
                        wplug=wplug,
                    )

                    if con_flag is not None:
                        _set_flag(dout, key, con_flag, k0, con_val)

                    else:
                        _set_flag(dout, key, 'ok', k0, True)

    # -----------
    # update
    # -----------

    for kflag, vflag in dout.items():

        if kflag == 'lunique':
            continue

        for k0, v0 in vflag.items():
            for k1, v1 in v0.items():
                coll.dobj[which0][k0]['connections'][k1]['flag'] = kflag

    return dout


#############################################
#############################################
#       utility
#############################################


def _set_flag(dout, key, kflag, k0, val):
    if key not in dout[kflag].keys():
        dout[kflag][key] = {}
    dout[kflag][key][k0] = val


#############################################
#############################################
#       check plug types
#############################################


def _plug_types(
    coll,
    which0=None,
    which1=None,
    key0=None,
    key1=None,
    con0=None,
    con1=None,
    v0=None,
    v1=None,
    wplug=None,
):

    # ---------------
    # plug types
    # ---------------

    if v0[wplug] != v1[wplug]:
        msg = f"{v0[wplug]} vs {v1[wplug]} for {which1} '{key1}', connection '{con1}'"
        return 'type_wrong', msg

    # ---------------
    # options
    # ---------------

    dopt0 = v0.get('doptions')
    dopt1 = v1.get('doptions')

    if dopt0 is None:
        dopt0 = {}
    if dopt1 is None:
        dopt1 = {}

    # ------------------
    # options from dopt0
    # ------------------

    for kk, vv in dopt0.items():

        if dopt1.get(kk) is None:
            pass

        elif vv != dopt1[kk]:
            msg = (
                f"{kk} {vv} vs {dopt1[kk]} for {which1} '{key1}', connection '{con1}'"
            )
            return 'specs_wrong', msg

    # ------------------
    # options from dopt1 missing from dopt0
    # ------------------

    for kk, vv in dopt1.items():

        if dopt0.get(kk) is None:
            msg = kk
            return 'specs_wrong', msg

    return None, None