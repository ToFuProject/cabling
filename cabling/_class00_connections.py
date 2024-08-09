# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:53:23 2024

@author: dvezinet
"""




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