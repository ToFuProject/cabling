# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:31:37 2024

@author: dvezinet
"""


import datastock as ds


from . import _class00_check
from . import _class01_def_dict as _def_dict


#############################################
#############################################
#       main
#############################################


def main(
    coll=None,
    key=None,
    connections=None,
    **kwdargs,
):

    # ---------------------
    # check key
    # ---------------------

    wdev = coll._which_device
    lout = list(coll.dobj.get(wdev, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ---------------------
    # ptA, ptB
    # ---------------------

    connections = _connections(coll, key, connections)

    # ---------------------
    # kwdargs
    # ---------------------

    kwdargs = _class00_check._kwdargs(
        coll,
        key,
        kwdargs,
        defdict=_def_dict.get_kwdargs(),
    )

    # ---------------------
    # store
    # ---------------------

    coll.add_obj(
        which=wdev,
        key=key,
        connections=connections,
        harmonize=True,
        **kwdargs,
    )

    return


#############################################
#############################################
#       connections
#############################################


def _connections(coll, key, connections):

    # --------------------
    # available connectors
    # --------------------

    wcon = coll._which_connector
    lok = list(coll.dobj.get(wcon, {}))

    # --------------------
    # available connectors
    # --------------------

    if connections is None:
        connections = {}

    c0 = (
        isinstance(connections, dict)
        and all([
            isinstance(k0, str)
            and (
                isinstance(v0, str)
                or (
                    isinstance(v0, dict)
                    and isinstance(v0.get(wcon), str)
                )
            )
            for k0, v0 in connections.items()
        ])
    )

    # ------------------------------
    # population with default values
    # ------------------------------

    for k0, v0 in connections.items():
        for k1, v1 in _def_dict.get_connections().items():

            # type checking + default
            connections[k0][k1] = ds._generic_check._check_var(
                connections[k0].get(k1), k1,
                types=v1.get('types'),
                default=v1.get('def'),
            )

            # as type
            if v1.get('astype') is not None:
                connections[k0][k1] = eval(f"{v1['astype']}({connections[k0][k1]})")

            # can be None
            wdev = coll._which_device
            if v1.get('can_be_None') is False and connections[k0][k1] is None:
                msg = (
                    f"For {wdev} '{key}', connection '{k0}', "
                    f"arg '{k1}' must be provided!"
                )
                raise Exception(msg)

    return connections