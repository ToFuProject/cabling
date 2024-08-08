# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:27:03 2024

@author: dvezinet
"""

import copy


import numpy as np
import datastock as ds


from . import _class00_check as _check
from. import _class00_show as _show
# from. import _class00_show_details as _show_details


__all__ = ['Connectors']


#############################################
#############################################
#       DEFAULT VALUES
#############################################





#############################################
#############################################
#       Spectral Lines
#############################################


class Connectors(ds.DataStock):

    _ddef = copy.deepcopy(ds.DataStock._ddef)
    _dshow = dict(ds.DataStock._dshow)
    _dshow['connector'] = None # to avoid nbug at add_obj()

    _ddef['params']['dobj'] = {
        # 'lines': {
        #     'lambda0': {'cls': float, 'def': 0.},
        #     'source': {'cls': str, 'def': 'unknown'},
        #     'transition': {'cls': str, 'def': 'unknown'},
        #     'element':  {'cls': str, 'def': 'unknown'},
        #     'charge':  {'cls': int, 'def': 0},
        #     'ion':  {'cls': str, 'def': 'unknown'},
        #     'symbol':   {'cls': str, 'def': 'unknown'},
        # },
    }

    _which_plug_type = 'plug_type'
    _which_connector_type = 'connector_type'
    _which_connector_model = 'connector_model'
    _which_connector = 'connector'
    _which_device_type = 'device_type'
    _which_device_model = 'device_model'
    _which_device = 'device'

    # -------------------
    # add connection type
    # -------------------

    def add_plug_type(self, key, **kwdargs):
        # add obj
        _check.plug_type(self, key, **kwdargs)

    # -------------------
    # add connector type
    # -------------------

    def add_connector_type(self, key=None, **kwdargs):
        # add obj
        _check.connector_type(self, key, **kwdargs)

    # -------------------
    # add Connector model
    # -------------------

    def add_connector_model(self, key=None, connections=None, **kwdargs):
        # add obj
        _check.connector_model(
            self,
            key=key,
            connections=connections,
            **kwdargs,
        )

    # -------------------
    # add Connector
    # -------------------

    def add_connector(
        self,
        systems=None,
        label=None,
        ptA=None,
        ptB=None,
        consistency=None,
        **kwdargs,
    ):

        # add obj
        return _check.connector(
            self,
            systems=systems,
            label=label,
            ptA=ptA,
            ptB=ptB,
            consistency=consistency,
            **kwdargs,
        )

    # -------------------
    # show
    # -------------------

    def _get_show_obj(self, which=None):
        if which == self._which_plug_type:
            return _show._plug_type
        elif which == self._which_connector_model:
            return _show._connector_model
        elif which == self._which_connector:
            return _show._connector
        else:
            return super()._get_show_obj(which)

    # def _get_show_details(self, which=None):
    #     if which == self._which_connector:
    #         return _show_details._connector
    #     else:
    #         super()._get_show_details(which)