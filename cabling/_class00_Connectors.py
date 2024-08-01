# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:27:03 2024

@author: dvezinet
"""

import copy


import numpy as np
import datastock as ds


from . import _class00_check as _check


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

    _which_connection_type = 'connection_type'
    _which_connector_model = 'connector_model'
    _which_connector = 'connector'
    _which_device_model = 'device_model'
    _which_device = 'device'

    # -------------------
    # add connection type
    # -------------------

    def add_connection_type(self, key=None, **kwdargs):
        # add obj
        _check.connector_type(self, key, **kwdargs)

    # -------------------
    # add Connector model
    # -------------------

    def add_connector_model(self, key=None, **kwdargs):
        # add obj
        _check.connector_model(self, key, **kwdargs)

    # -------------------
    # add Connector
    # -------------------

    def add_connector(self, key=None, ptA=None, ptB=None, **kwdargs):

        # add obj
        _check.connector(self, key, ptA, ptB, **kwdargs)

        # double-check connections
        self.check_connections()