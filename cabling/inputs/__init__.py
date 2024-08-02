# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:27:03 2024

@author: dvezinet
"""


from . import _plug_types
from . import _connector_types
from . import _connector_models
from . import _connectors
from . import _device_types
from . import _device_models
from . import _devices


# ####################################################
# ####################################################
#               main
# ####################################################


def create_all(path=None):

    lmod = [
        _plug_types,
        _connector_types,
        _connector_models,
        _connectors,
        _device_types,
        _device_models,
        _devices,
    ]

    for mm in lmod:
        mm.get(path=path)

    return