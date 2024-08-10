# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 12:11:27 2024

@author: dvezinet
"""


import datastock as ds


from . import _consistency_connections as _connections
from . import _class00_check_coords as _check_coords


#############################################
#############################################
#       main
#############################################



def main(
    coll=None,
    verb=None,
    returnas=None,
):

    # --------------
    # check inputs
    # --------------

    verb, returnas = _check(
        verb=verb,
        returnas=returnas,
    )

    # --------------------------
    # verb
    # --------------------------

    if verb is True:
        msg = (
            '\n\t--------------------------\n'
            "\tOverall consistency check\n"
        )
        print(msg)

    # --------------------------
    # consistency of connections
    # --------------------------

    dout = {}

    dout['connections'] = _connections.main(
        coll=coll,
    )

    # ---------------------
    # consistency of coords
    # ---------------------

    wcon = coll._which_connector
    for k0, v0 in coll.dobj.get(wcon, {}).items():
        coll.dobj[wcon][k0]['dcoords'] = _check_coords._dcoords_connector(
            coll, wcon, k0,
            dcon=coll.dobj[wcon][k0]['connections'],
            dcoords=coll.dobj[wcon][k0].get('dcoords'),
        )

    # --------------------------
    # verb
    # --------------------------

    if verb is True:
        _verb(coll, dout)

    # --------------------------
    # return
    # --------------------------

    if returnas is True:
        out = dout
    else:
        out = None

    return out


#############################################
#############################################
#       check inputs
#############################################


def _check(
    verb=None,
    returnas=None,
):

    # -----------------
    # verb
    # -----------------

    verb = ds._generic_check._check_var(
        verb, 'verb',
        types=bool,
        default=True,
    )

    # -----------------
    # returnas
    # -----------------

    returnas_def = not verb
    returnas = ds._generic_check._check_var(
        returnas, 'returnas',
        types=bool,
        default=returnas_def,
    )

    return verb, returnas


#############################################
#############################################
#       verb
#############################################


def _verb(coll=None, dout=None):

    return