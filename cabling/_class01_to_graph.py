# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 18:24:45 2024

@author: dvezinet
"""


import networkx as nx
import datastock as ds


# ############################################################
# ############################################################
#              Main
# ############################################################


def main(
    coll=None,
    # which devices to plot
    devices=None,
    # naming
    name_device=None,
    name_connector=None,
    # plotting options
    layout=None,
    name_by=None,
):

    # ---------------
    # check
    # ---------------

    name_device, name_connector = _check(
        coll=coll,
        name_device=name_device,
        name_connector=name_connector,
    )

    # ---------------
    # select devices and connectors
    # ---------------

    ldev, lcon = _select(
        coll=coll,
        devices=devices,
     )

    # ---------------
    # create graph
    # ---------------

    graph = _create_graph(
        coll=coll,
        ldev=ldev,
        lcon=lcon,
        name_device=name_device,
        name_connector=name_connector,
    )

    return graph



# ############################################################
# ############################################################
#              check inputs
# ############################################################


def _check(
    coll=None,
    # naming
    name_device=None,
    name_connector=None,
):

    # ---------------
    # name_device
    # ---------------

    wdt = coll._which_device_type
    wdm = coll._which_device_model
    lok = ['key', 'tag', 'label', wdm, wdt, 'systems']

    name_device = ds._generic_check._check_var(
        name_device, 'name_device',
        types=str,
        allowed=lok,
        default='key',
    )

    # ---------------
    # name_connector
    # ---------------

    wct = coll._which_connector_type
    wcm = coll._which_connector_model
    lok = ['key', 'tag', 'label', wcm, wct, 'systems']

    name_connector = ds._generic_check._check_var(
        name_connector, 'name_connector',
        types=str,
        allowed=lok,
        default='key',
    )

    return name_device, name_connector

# ############################################################
# ############################################################
#              Select
# ############################################################


def _select(
    coll=None,
    devices=None,
    connectors='graph',
):

    # ---------------
    # devices
    # ---------------

    if isinstance(devices, str):
        devices = [devices]

    wdev = coll._which_device
    lok = list(coll.dobj[wdev].keys())
    ldev = list(ds._generic_check._check_var_iter(
        devices, 'devices',
        types=(list, tuple),
        types_iter=str,
        default=lok,
        allowed=lok,
    ))

    # ---------------
    # connectors
    # ---------------

    wcon = coll._which_connector
    if connectors == 'graph':
        lcon = []
        for kcon, vcon in coll.dobj.get(wcon, {}).items():
            dcon = coll.dobj[wcon][kcon]['connections']
            c0 = all([vv[wdev][0] in ldev for vv in dcon.values()])
            if c0 is True:
                lcon.append(kcon)

    else:
        if isinstance(connectors, str):
            connectors = [connectors]
        lok = list(coll.dobj[wcon].keys())
        lcon = ds._generic_check._check_var_iter(
            connectors, 'connectors',
            types=list,
            types_iter=str,
            allowed=lok,
            default=lok,
        )

    # ------------------------------------------------
    # restrict to connectors that have ok connections

    lcon  = [
        k0 for k0 in lcon
        if all([
            v0['flag'] == 'ok'
            for v0 in coll.dobj[wcon][k0]['connections'].values()
        ])
    ]

    return ldev, lcon


# ############################################################
# ############################################################
#              Create graph
# ############################################################


def _create_graph(
    coll=None,
    ldev=None,
    lcon=None,
    # naming
    name_device=None,
    name_connector=None,
):

    # -----------------
    # initialize
    # -----------------

    graph = nx.Graph()

    # -----------------
    # nodes = devices
    # -----------------

    wdev = coll._which_device
    for k0 in ldev:
        v0 = coll.dobj[wdev][k0]
        graph.add_node(k0)

    # -----------------
    # links = connectors
    # -----------------

    wcon = coll._which_connector
    for k0 in lcon:

        v0 = coll.dobj[wcon][k0]

        ptA_key = v0['connections']['ptA'][wdev][0]
        ptB_key = v0['connections']['ptB'][wdev][0]

        graph.add_edge(ptA_key, ptB_key)

    return graph