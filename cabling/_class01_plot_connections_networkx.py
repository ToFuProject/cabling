# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 18:24:45 2024

@author: dvezinet
"""


import networkx as nx



# ############################################################
# ############################################################
#              Main
# ############################################################


def main(
    coll=None,
):

    # ---------------
    # select devices and connectors
    # ---------------

    ldev, lcon = _select(coll)

    # ---------------
    # create graph
    # ---------------

    graph = _create_graph(
        coll=coll,
        ldev=ldev,
        lcon=lcon,
    )

    # ---------------
    # plot
    # ---------------

    _plot(
        coll=coll,
        graph=graph,
    )

    return graph


# ############################################################
# ############################################################
#              Select
# ############################################################


def _select(coll=None):

    # ---------------
    # devices
    # ---------------

    wdev = coll._which_device
    ldev = list(coll.dobj.get(wdev, {}).keys())

    # ---------------
    # connectors
    # ---------------

    lcon = []
    wcon = coll._which_connector
    for kcon, vcon in coll.dobj.get(wcon, {}).items():

        dcon = coll.dobj[wcon][kcon]['connections']
        c0 = all([vv[wdev][0] in ldev for vv in dcon.values()])
        if c0 is True:
            lcon.append(kcon)

    return ldev, lcon


# ############################################################
# ############################################################
#              Create graph
# ############################################################


def _create_graph(
    coll=None,
    ldev=None,
    lcon=None,
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


# ############################################################
# ############################################################
#              plot
# ############################################################


def _plot(
    coll=None,
    graph=None,
):

    # --------------
    # plot
    # --------------

    nx.draw(graph, with_labels=True, font_weight='bold')

    return