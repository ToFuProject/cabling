# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 22:16:42 2024

@author: dvezinet
"""


#############################################
#############################################
#       Connector_type
#############################################


def _plug_type(coll=None, which=None, lcol=None, lar=None, show=None):

    # ---------------------------
    # list of functions
    # ---------------------------

    # list of connectors
    lkey = [
        k1 for k1 in coll._dobj.get(which, {}).keys()
        if show is None or k1 in show
    ]

    # ---------------------------
    # column names
    # ---------------------------

    wplug = coll._which_plug_type
    lcol.append([which] + ['description', 'options'])

    # ---------------------------
    # data array
    # ---------------------------

    lar0 = []
    for k0 in lkey:

        # initialize with key
        arr = [k0, coll.dobj[wplug][k0].get('description', '')]

        # options
        dopt = coll.dobj[wplug][k0].get('doptions')
        if dopt is None:
            nn = ''
        else:
            nn = str(sorted(dopt.keys()))
        arr.append(nn)

        lar0.append(arr)

    lar.append(lar0)

    return lcol, lar


#############################################
#############################################
#       Connector_model
#############################################


def _connector_model(coll=None, which=None, lcol=None, lar=None, show=None):

    # ---------------------------
    # list of functions
    # ---------------------------

    # list of connectors
    lkey = [
        k1 for k1 in coll._dobj.get(which, {}).keys()
        if show is None or k1 in show
    ]

    # ---------------------------
    # column names
    # ---------------------------

    wplug = coll._which_plug_type
    wct = coll._which_connector_type
    wcm = coll._which_connector_model
    lcol.append([which] + [wct, 'description', 'ptA', 'ptB', 'PN'])

    # ---------------------------
    # data array
    # ---------------------------

    lar0 = []
    for k0 in lkey:

        # initialize with key
        arr = [k0, coll.dobj[wcm][k0][wct]]

        # description
        arr.append(coll.dobj[wcm][k0].get('description', ''))

        # add ptA and ptB
        dcon = coll.dobj[wcm][k0]['connections']
        for pt in ['ptA', 'ptB']:
            nn = str(dcon[pt][wplug]['key'])
            arr.append(nn)

        # add systems
        arr.append(str(coll.dobj[wcm][k0].get('PN', '')))
        lar0.append(arr)

    lar.append(lar0)

    return lcol, lar


#############################################
#############################################
#       Connector
#############################################


def _connector(coll=None, which=None, lcol=None, lar=None, show=None):

    # ---------------------------
    # list of functions
    # ---------------------------

    # list of connectors
    lkey = [
        k1 for k1 in coll._dobj.get(which, {}).keys()
        if show is None or k1 in show
    ]

    # ---------------------------
    # column names
    # ---------------------------

    wcm = coll._which_connector_model
    lcol.append(['systems', which] + [wcm, 'ptA', 'ptB'])

    # ---------------------------
    # data array
    # ---------------------------

    lar0 = []
    wcon = coll._which_connector
    wdev = coll._which_device
    for k0 in lkey:

        arr = []

        # add systems
        dsys = coll.dobj[wcon][k0].get('systems')
        if dsys is None:
            nn = ''
        else:
            ln = sorted(dsys.keys())
            nn = ':'.join([dsys[k0] for k0 in ln])
        arr.append(nn)

        # initialize with key
        arr += [k0, coll.dobj[wcon][k0][wcm]]

        # add ptA and ptB
        dcon = coll.dobj[wcon][k0]['connections']
        for pt in ['ptA', 'ptB']:
            nn = str(dcon[pt][wdev])
            arr.append(nn)

        lar0.append(arr)

    lar.append(lar0)

    return lcol, lar