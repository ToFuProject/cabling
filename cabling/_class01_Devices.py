# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:27:03 2024

@author: dvezinet
"""

import copy


from ._class00_Connectors import Connectors as Previous
from . import _class01_check as _check
from . import _consistency


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

    # -------------------
    # add Device type
    # -------------------

    def add_device_type(self, key=None, **kwdargs):
        _check.type(coll=self, jey=key, **kwdargs)

    # -------------------
    # add Device model
    # -------------------

    def add_device_model(self, key=None, **kwdargs):
        _check.model(coll=self, jey=key, **kwdargs)

    # -------------------
    # add Device
    # -------------------

    def add_device(self, key=None, connections=None, **kwdargs):

        # add obj
        _check.device(self, key, connections, **kwdargs)

        # double-check connections
        self.check_connections()

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