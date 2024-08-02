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

    # --------------
    # check devices
    # --------------

    ddev = _connections(
        coll=coll,
        which0=wdev,
        which1=wcon,
    )

    # --------------
    # check connectors
    # --------------

    dcon = _connections(
        coll=coll,
        which0=wcon,
        which1=wdev,
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
        'miss': {},
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

            if v0[which1] is None:
                kflag = 'loose'
                if key not in dout[kflag].keys():
                    dout[kflag][key] = {}
                dout[kflag][key][k0] = True

            # -----------------
            # error (not a tuple of 2 str)

            elif not (
                    isinstance(v0[which1], tuple)
                    and len(v0[which1]) == 2
                    and all([isinstance(ss, str) for ss in v0[which1]])
                ):
                kflag = 'err'
                if key not in dout[kflag][key].keys():
                    dout[kflag][key] = {}
                dout[kflag][key][k0] = v0[which1]

            # ------------
            # unknown end - level 1: which

            elif v0[which1][0] not in lk1:
                kflag = 'unknown'
                if key not in dout[kflag][key].keys():
                    dout[kflag][key] = {}
                dout[kflag][key][k0] = "which1}: '{v0[which1][0]}'"

            # ------------
            # unknown end - level 2: plug

            elif v0[which1][1] not in coll.dobj[which1][v0[which1][0]]['connections'].keys():
                kflag = "unknown"
                if key not in dout[kflag][key].keys():
                    dout[kflag][key] = {}
                dout[kflag][key][k0] = (
                    f"plug of {which1} '{v0[which1][0]}': {v0[which1][1]}"
                )

            # -------------
            # redundant end

            elif v0[which1] in dout['lunique']:
                kflag = 'multi'
                if key not in dout[kflag][key].keys():
                    dout[kflag][key] = {}
                dout[kflag][key][k0] = v0[which1]

            # ------------------
            # ok => mark as done

            else:
                kflag = 'ok'
                if key not in dout[kflag][key].keys():
                    dout[kflag][key] = {}
                dout[kflag][key][k0] = True
                dout['lunique'].append(v0[which1])

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