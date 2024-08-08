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
from . import _class01_utils as _utils
from . import _class01_to_graph as _to_graph
from . import _class01_to_DataFrame as _to_DataFrame
from . import _class01_to_spreadsheet as _to_spreadsheet
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
    _dshow['device'] = None # to avoid nbug at add_obj()

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

    def add_device(
        self,
        systems=None,
        label=None,
        **kwdargs,
    ):
        # add obj
        _check.device(
            self,
            systems=systems,
            label=label,
            **kwdargs,
        )

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
    # to Dataframes
    # -------------------

    def to_DataFrame(self, which=None, keys=None):
        lok = [
            self._which_plug_type,
            self._which_connector_type,
            self._which_connector_model,
            self._which_connector,
            self._which_device_type,
            self._which_device_model,
            self._which_device,
        ]
        if which in lok:
            return _to_DataFrame.main(self, which=which, keys=keys)
        else:
            super().to_DataFrame(which=which, keys=keys)

    # -------------------
    # export to spreadsheet
    # -------------------

    def save_to_spreadsheet(
        self,
        # selection
        devices=None,
        connectors=None,
        # options
        startrow=None,
        startcol=None,
        # pfe
        pfe=None,
        verb=None,
    ):
        return _to_spreadsheet.main(
            coll=self,
            # selection
            devices=devices,
            connectors=connectors,
            # options
            startrow=startrow,
            startcol=startcol,
            # pfe
            pfe=pfe,
            verb=verb,
        )

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
        return _to_graph.main(
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
        layers=None,
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
            layers=layers,
            name_by=name_by,
        )