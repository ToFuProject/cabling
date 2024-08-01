# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 12:11:27 2024

@author: dvezinet
"""


import datastock as ds


from . import _consistency_connections as _connections


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
    # consistency of connections
    # --------------------------

    dout = {}

    dout['connections'] = _connections.main(
        coll=coll,
        verb=verb,
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