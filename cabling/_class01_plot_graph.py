# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 18:24:45 2024

@author: dvezinet
"""


import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import datastock as ds


# ############################################################
# ############################################################
#              Main
# ############################################################


def main(
    coll=None,
    # which devices to plot
    graph=None,
    # labels
    name_device=None,
    name_connector=None,
    # plotting options
    layout=None,
    layers=None,
    name_by=None,
    # -----------
    # parameters
    # edges
    arrows=None,
    # arrowsize=None,
    # nodes
    node_size=None,
    node_color=None,
    linewidths=None,
    width=None,
    edge_color=None,
    # labels
    with_labels=True,
    font_size=None,
    font_weight=None,
    # others
    hide_ticks=None,
    # figure
    ax=None,
):

    # ---------------
    # check input
    # ---------------

    kwdargs = _check(**locals())

    # -----------------
    # labels
    # -----------------

    dname_device, dname_connector = _labels(
        coll=coll,
        graph=graph,
        name_device=name_device,
        name_connector=name_connector,
    )

    # ---------------
    # layout
    # ---------------

    pos = _layout(
        coll=coll,
        graph=graph,
        layout=layout,
        layers=layers,
    )

    # ---------------
    # plot
    # ---------------

    ax = _plot_mpl(
        graph=graph,
        # labels
        dname_device=dname_device,
        dname_connector=dname_connector,
        # layout
        pos=pos,
        ax=ax,
        # options
        **kwdargs,
    )

    return ax


# ############################################################
# ############################################################
#              check
# ############################################################


def _check(
    # resources
    coll=None,
    graph=None,
    # automatic sizing / coloring
    size_by=None,
    color_by=None,
    # edges
    arrows=None,
    # arrowsize=None,
    # nodes
    node_size=None,
    node_color=None,
    linewidths=None,
    width=None,
    edge_color=None,
    # labels
    with_labels=True,
    font_size=None,
    font_weight=None,
    # others
    hide_ticks=None,
    # unused
    **kwds,
):

    # -------------
    # graph
    # -------------

    if not isinstance(graph, nx.Graph):
        msg = (
            "Arg graph must be a nx.Graph instance!\n"
            f"Provided:\n{graph}"
        )
        raise Exception(msg)

    # -------------
    # kwdargs for plot
    # -------------

    lout = ['coll', 'kwds', 'lout', 'size_by', 'color_by', 'layers', 'graph']
    kwdargs = {
        k0: v0 for k0, v0 in locals().items()
        if k0 not in lout
        and k0 not in kwds.keys()
    }

    kwdargs['arrows'] = True

    # -------------
    # size_by
    # -------------

    return kwdargs


# ############################################################
# ############################################################
#              labels
# ############################################################


def _labels(
    coll=None,
    # selection
    graph=None,
    # naming
    name_device=None,
    name_connector=None,
):

    # ---------------
    # extract
    # ---------------

    ldev = list(graph.nodes)
    wcon = coll._which_connector

    # ---------------
    # name_device
    # ---------------

    which = coll._which_device
    dname_device = coll.get_display_key_from_systems(
        which,
        keys=ldev,
        include=name_device,
    )

    # ---------------
    # name_connector
    # ---------------

    which = coll._which_connector
    dname_connector = None

    return dname_device, dname_connector


# ############################################################
# ############################################################
#              layout
# ############################################################


def _layout(
    coll=None,
    graph=None,
    layout=None,
    layers=None,
):

    # -------------
    # layout
    # -------------

    if layout is None and layers is not None:
        layout = 'multipartite'

    if isinstance(layout, dict):
        pos = layout

    elif layout == 'multipartite':

        if layers is None:
            wdev = coll._which_device
            dnsys = {k0: len(coll.dobj[wdev][k0]['systems']) for k0 in graph.nodes}
            nsys = np.unique([v0 for v0 in dnsys.values()])
            layers = {
                nn: [k1 for k1 in graph.nodes if dnsys[k1] == nn]
                for nn in nsys
            }

        pos = nx.multipartite_layout(
            graph,
            subset_key=layers,
            align='vertical',
            scale=1,
            center=None,
        )

    else:
        lout = ['bfs', 'bipartite', 'multipartite', 'rescale', 'spectral']
        lok = [
            ss[:-7] for ss in dir(nx)
            if ss.endswith('_layout')
            and not ss[:-7] in lout
        ]
        layout = ds._generic_check._check_var(
            layout, 'layout',
            types=str,
            default='fruchterman_reingold',
            allowed=lok,
        )

        # -------------
        # layout
        # -------------

        pos = getattr(nx, f'{layout}_layout')(graph)

    return pos


# ############################################################
# ############################################################
#              plot - matplotlib
# ############################################################


def _plot_mpl(
    graph=None,
    # labels
    dname_device=None,
    dname_connector=None,
    # layout
    pos=None,
    # figure
    ax=None,
    # options
    **kwdargs,
):

    # --------------
    # figure
    # --------------

    if ax is None:
        fig = plt.figure()
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    # --------------
    # plot
    # --------------

    nx.draw_networkx(
        graph,
        # labels
        labels=dname_device,
        with_labels=True,
        # ax
        ax=ax,
        # layout
        pos=pos,
        # edges
        # **kwdargs
    )

    return ax