# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 22:16:42 2024

@author: dvezinet
"""


import numpy as np


#############################################
#############################################
#       device_type
#############################################


def _device_type(coll=None, which=None, lcol=None, lar=None, show=None):

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

    wdt = coll._which_device_type
    lcol.append([which] + ['description'])

    # ---------------------------
    # data array
    # ---------------------------

    lar0 = []
    for k0 in lkey:

        # initialize with key
        arr = [k0, coll.dobj[wdt][k0].get('description', '')]
        lar0.append(arr)

    lar.append(lar0)

    return lcol, lar


#############################################
#############################################
#       device_model
#############################################


def _device_model(coll=None, which=None, lcol=None, lar=None, show=None):

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

    wdt = coll._which_device_type
    wdm = coll._which_device_model
    lcol.append([which] + [wdt, 'description', 'nb. connections', 'PN'])

    # ---------------------------
    # data array
    # ---------------------------

    lar0 = []
    for k0 in lkey:

        # initialize with key
        arr = [k0]

        # type
        dtype = coll.dobj[wdm][k0].get(wdt)
        arr.append('' if dtype is None else dtype)

        # description
        des = coll.dobj[wdm][k0].get('description')
        arr.append('' if des is None else des)

        # add nb of connections
        dcon = coll.dobj[wdm][k0]['connections']
        arr.append(str(len(dcon)))

        # add systems
        if coll.dobj[wdm][k0].get('PN') is None:
            nn = ''
        else:
            nn = coll.dobj[wdm][k0].get('PN')
        arr.append(nn)

        lar0.append(arr)

    lar.append(lar0)

    return lcol, lar


#############################################
#############################################
#       Device
#############################################


def _device(coll=None, which=None, lcol=None, lar=None, show=None):

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

    wdm = coll._which_device_model
    lcol.append([which] + [wdm, 'connections ok'])

    # ---------------------------
    # data array
    # ---------------------------

    lar0 = []
    wdev = coll._which_device
    for k0 in lkey:

        # initialize with key
        arr = [k0, coll.dobj[wdev][k0][wdm]]

        # add systems
        # dsys = coll.dobj[wdev][k0].get('systems')
        # if dsys is None:
        #     nn = ''
        # else:
        #     ln = sorted(dsys.keys())
        #     nn = ':'.join([dsys[k0] for k0 in ln])
        # arr.append(nn)


        # add ptA and ptB
        dcon = coll.dobj[wdev][k0]['connections']
        nok = np.sum([v0['flag'] == 'ok' for v0 in dcon.values()])
        nn = f"{nok} / {len(dcon)}"
        arr.append(nn)

        lar0.append(arr)

    lar.append(lar0)

    return lcol, lar