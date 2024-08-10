# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:53:23 2024

@author: dvezinet
"""


import datastock as ds


#############################################
#############################################
#       connections type, nb and names
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

    # check is dict
    wplug = coll._which_plug_type
    if not isinstance(connections, dict):
        _err_connections(which, key, connections, wplug)

    # check keys if provided
    lk = sorted(connections.keys())
    lok = sorted(coll.dobj[wplug].keys())
    if lcon is not None:
        if lk != sorted(lcon):
            _err_connections(which, key, connections, wplug, lok, lcon)

    # ----------------
    # plug types
    # ----------------

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
        for pt in lk
    ])
    if not c0:
        _err_connections(which, key, connections, wplug, lok, lk)

    # ------------
    # plug options
    # -------------

    dout = {}
    inc = 0
    for ii, pt in enumerate(lk):

        # ------------
        # check for nb

        dcon = connections[pt]
        nb = dcon.get('nb')
        if nb is None or nb == 1:
            kcon = pt if lcon is not None else f'con{inc}'
            name = dcon.get('name', pt)
            _individual_connection(
                coll, dout, pt, kcon, name, wplug, dcon, which, key,
            )
            inc += 1

        else:

            if lcon is not None:
                msg = "lcon cannot be provided if nb is provided!"
                raise Exception(msg)

            if not (isinstance(nb, int) and nb > 1):
                msg = "Arg nb must be a strictly positive integer"
                raise Exception(msg)

            for i1 in range(nb):
                kcon = f'con{inc}'
                name = f"{dcon.get('name', pt)}_{i1}"
                _individual_connection(
                    coll, dout, pt, kcon, name, wplug, dcon, which, key,
                )
                inc += 1

    return dout


#############################################
#############################################
#       individual connection
#############################################


def _individual_connection(
    coll=None,
    dout=None,
    pt=None,
    kcon=None,
    name=None,
    wplug=None,
    dcon=None,
    which=None,
    key=None,
):

    dout[kcon] = {
        'name': name,
        wplug: {},
        **{k1: v1 for k1, v1 in dcon.items() if k1 != wplug and k1 != 'nb'}
    }

    if isinstance(dcon.get(wplug), str):
        dout[kcon][wplug] = {'key': dcon[wplug]}

    else:
        for k1, v1 in dcon[wplug].items():

            if k1 == 'key':
                dout[kcon][wplug]['key'] = v1

            # ---------------
            # options

            else:

                plug_type = dcon[wplug]['key']
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

                dout[kcon][wplug][k1] = v1

    return


#############################################
#############################################
#       error handling
#############################################


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
#       ptA and ptB for Connectors
#############################################


def _ptAB(coll, which, key, ptA, ptB, systems):

    # -----------------
    # available devices
    # -----------------

    wdev = coll._which_device
    lok = list(coll.dobj.get(wdev, {}))

    din = {'ptA': ptA, 'ptB': ptB}
    for pt in ['ptA', 'ptB']:

        if din[pt] is None:
            msg = (
                f"For {which} '{key}', arg '{pt}' must be provided!"
            )
            raise Exception(msg)

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
            # check existence of device

            if din[pt][0] not in lok:
                msg = (
                    f"For {which} '{key}', wrong first term in arg '{pt}':\n"
                    "Should be either:\n"
                    f"\t- a known unique key to a {wdev}\n"
                    f"\t- a known label to a {wdev} in the same systems\n"
                    "Available:\n"
                    f"\t- keys: {lok}\n"
                    f"Provided:\n\t'{din[pt][0]}'\n"
                )
                raise Exception(msg)

            # -----------------------
            # check existence of pts

            dcon = coll.dobj[wdev][din[pt][0]]['connections']
            lok_keys = list(dcon.keys())
            lok_names = [dcon[kk]['name'] for kk in lok_keys]

            if din[pt][1] in lok_names:
                din[pt] = (din[pt][0], lok_keys[lok_names.index(din[pt][1])])

            elif din[pt][1] not in lok_keys:
                msg = (
                    f"For {which} '{key}', wrong second term in arg '{pt}':\n"
                    f"For {wdev} '{din[pt][0]}' connections:\n"
                    f"\t- available connection keys: {lok_keys}\n"
                    f"\t- available connection names: {lok_names}\n"
                    f"Provided:\n\t'{din[pt][1]}'\n"
                )
                raise Exception(msg)

    return tuple(din['ptA']), tuple(din['ptB'])


###########################################################
###########################################################
#      Connection report
###########################################################


def get_report(
    coll=None,
    which=None,
    returnas=None,
    verb=None,
):

    # ------------
    # check inputs
    # ------------

    lwhich, verb, returnas = _check(
        coll=coll,
        which=which,
        returnas=returnas,
        verb=verb,
    )

    # ------------
    # connectors
    # ------------

    dout = {}
    lwhich0 = [coll._which_connector, coll._which_device]
    for ii, ww in enumerate(lwhich0):
        if ww in lwhich:
            dout[ww] = _get_report(coll, ww, lwhich0[1-ii])

    # ------------
    # return
    # ------------

    if returnas is dict:
        return dout

    dmsg = {}
    for ii, ww in enumerate(lwhich0):
        if ww in lwhich:
            dmsg[ww] = _to_msg(coll, dout, ww, lwhich0[1-ii])

    if verb is True:
        print("\n\n".join(list(dmsg.values())))

    return


#############################################
#############################################
#      check
#############################################


def _check(
    coll=None,
    which=None,
    verb=None,
    returnas=None,
):

    # -----------------
    # which
    # -----------------

    if isinstance(which, str):
        which = [which]
    lok = [coll._which_device, coll._which_connector]
    which = ds._generic_check._check_var_iter(
        which, 'which',
        types=(list, tuple),
        allowed=lok,
    )

    # -----------------
    # verb
    # -----------------

    verb = ds._generic_check._check_var(
        verb, 'verb',
        types=bool,
        default=True,
    )

    # -----------------
    # verb
    # -----------------

    returnas = ds._generic_check._check_var(
        returnas, 'returnas',
        types=bool,
        default=(not verb),
    )

    return which, verb, returnas


#############################################
#############################################
#      report for which
#############################################


def _get_report(coll=None, which0=None, which1=None):

    dout = {}
    wplug = coll._which_plug_type
    for k0, v0 in coll.dobj.get(which0, {}).items():
        dout[k0] = {}
        for kcon, vcon in v0['connections'].items():
            dout[k0][kcon] = {
                'name': vcon['name'],
                wplug: vcon[wplug]['key'],
                which1: vcon.get(which1),
                'flag': vcon['flag'],
            }

    return dout


#############################################
#############################################
#      to msg
#############################################


def _to_msg(coll, dout, which0, which1):

    # -------------
    # lcol
    # --------------

    wplug = coll._which_plug_type
    lcol = [[which0, '|', 'kcon', 'name', wplug, '|', f'({which1}, kcon)', 'flag']]

    # -------------
    # larr
    # --------------

    larr = []
    for k0, v0 in coll.dobj.get(which0, {}).items():
        for ii, (kcon, vcon) in enumerate(v0['connections'].items()):

            arr = [
                k0 if ii == 0 else  '',
                '|',
                kcon,
                str(dout[which0][k0][kcon]['name']),
                str(dout[which0][k0][kcon][wplug]),
                '|',
                str(dout[which0][k0][kcon][which1]),
                str(dout[which0][k0][kcon]['flag']),
            ]
            larr.append(arr)

    # ----------------
    # msg
    # ----------------

    return ds._generic_utils.pretty_print(
        headers=lcol,
        content=[larr],
        sep=None,
        line=None,
        justify=None,
        table_sep=None,
        verb=False,
        returnas=str,
    )