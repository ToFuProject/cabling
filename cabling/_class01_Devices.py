# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:27:03 2024

@author: dvezinet
"""

import copy


from ._class00_Connectors import Connectors as Previous
from . import _class01_check as _check
from . import _add_from_json
from . import _consistency
from . import _class01_plot_connections_networkx as _plot_connections_networkx


__all__ = ['Devices']


#############################################
#############################################
#       DEFAULT VALUES
#############################################





#############################################
#############################################
#       Spectral Lines
#############################################


class Devices(Previous):

    _ddef = copy.deepcopy(Previous._ddef)
    _dshow = dict(Previous._dshow)

    _dshow['device_model'] = ['device_type', 'description', 'PN_vendor', 'chassis', 'sizeU']

    # -------------------
    # add Device type
    # -------------------

    def add_device_type(self, key=None, **kwdargs):
        _check.device_type(coll=self, key=key, **kwdargs)

    # -------------------
    # add Device model
    # -------------------

    def add_device_model(self, key=None, connections=None, **kwdargs):
        _check.device_model(
            coll=self,
            key=key,
            connections=connections,
            **kwdargs,
        )

    # -------------------
    # add Device
    # -------------------

    def add_device(self, key=None, **kwdargs):
        # add obj
        _check.device(self, key=key, **kwdargs)

    # ----------------------
    # add from json
    # ----------------------

    def add_connectors_devices_from_json(self, pfe=None, verb=None):
        return _add_from_json.main(coll=self, pfe=pfe, verb=verb)

    # -------------------
    # check consistency
    # -------------------

    def check_consistency(
            self,
            verb=None,
            returnas=None,
        ):
        """ Check overall consistency and print a report


        Parameters
        ----------
        verb : bool, optional
            Flag whether or not to print the report

        Returns
        -------
        dout: dict
            report dict

        """

        return _consistency.main(
            self,
            verb=verb,
            returnas=returnas,
        )

    # -------------------
    # plot
    # -------------------

    def plot_connections(
        self
    ):
        return _plot_connections_networkx.main(
            coll=self,
        )