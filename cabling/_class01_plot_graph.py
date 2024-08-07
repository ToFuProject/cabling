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
    name_device=None,
    name_connector=None,
    # plotting options
    layout=None,
    name_by=None,
    # -----------
    # parameters
    # edges
    arrows=None,
    arrowsize=None,
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
):

    # ---------------
    # check input
    # ---------------

    kwdargs = _check(**locals())

    # ---------------
    # select devices and connectors
    # ---------------

    graph = coll.to_graph(
        # select
        devices=devices,
        # naming
        name_device=name_device,
        name_connector=name_connector,
    )

    # ---------------
    # layout
    # ---------------

    pos = _layout(graph, layout)

    # ---------------
    # plot
    # ---------------

    _plot_mpl(
        graph=graph,
        # layout
        pos=pos,
        # options
        **kwdargs,
    )

    return graph


# ############################################################
# ############################################################
#              check
# ############################################################


def _check(
    # resources
    coll=None,
    # automatic sizing / coloring
    size_by=None,
    color_by=None,
    # edges
    arrows=None,
    arrowsize=None,
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

    lout = ['coll', 'kwds', 'lout', 'size_by', 'color_by']
    kwdargs = {k0: v0 for k0, v0 in locals().items() if k0 not in lout}


    # -------------
    # size_by
    # -------------


    return kwdargs


# ############################################################
# ############################################################
#              layout
# ############################################################


def _layout(
    graph=None,
    layout=None,
):

    # -------------
    # layout
    # -------------

    if isinstance(layout, dict):
        pos = layout

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
    # layout
    pos=None,
    # options
    **kwdargs,
):

    # --------------
    # figure
    # --------------

    # --------------
    # plot
    # --------------

    nx.draw_networkx(
        graph,
        # ax
        ax=None,
        # layout
        pos=pos,
        # edges
        **kwdargs
    )

    return