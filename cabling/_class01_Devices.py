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
from . import _class01_select as _select
from . import _class01_show as _show
from . import _class01_export_to_graph as _export_to_graph
from . import _class01_export_spreadsheet as _export_spreadsheet
from . import _class01_plot_graph as _plot_graph


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
    # select system
    # -------------------

    def select_systems(self, include=None, exclude=None):
        """ Return list of Devices / Connectors matching desired subsystems

        Parameters
        ----------

        Returns
        -------
        dout: dict
            dict with keys
                - 'device': list of device keys matching selection
                - 'connector': list of connector keys matching selection

        """
        return _select.main(coll=self, include=include, exclude=exclude)

    # -------------------
    # show
    # -------------------

    def _get_show_obj(self, which=None):
        if which == self._which_device_type:
            return _show._device_type
        elif which == self._which_device_model:
            return _show._device_model
        elif which == self._which_device:
            return _show._device
        else:
            return super()._get_show_obj(which)

    # -------------------
    # export to Dataframes and spreadsheet
    # -------------------

    def to_spreadsheet(self):
        return _export_spreadsheet.main(coll)

    # -------------------
    # export to graph
    # -------------------

    def to_graph(
        self,
        # select
        devices=None,
        # naming
        name_device=None,
        name_connector=None,
    ):
        """


        Parameters
        ----------
        devices: list, optional
            list of devices to include in the export
            systems-based selection can be done using self.select_systems()
        name_device : str, optional
            DESCRIPTION. The default is None.
        name_connector : str, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        graph
            a networkx graph with selected nodes (devices) and edges (connectors)

        """
        return _export_to_graph.main(
            coll=self,
            # select
            devices=devices,
            # naming
            name_device=name_device,
            name_connector=name_connector,
        )

    # -------------------
    # plot
    # -------------------

    def plot_graph(
        self,
        # which devices to plot
        devices=None,
        name_device=None,
        name_connector=None,
        # plotting options
        layout=None,
        name_by=None,
    ):

        return _plot_graph.main(
            coll=self,
            # which devices to plot
            devices=devices,
            name_device=name_device,
            name_connector=name_connector,
            # plotting options
            layout=layout,
            name_by=name_by,
        )