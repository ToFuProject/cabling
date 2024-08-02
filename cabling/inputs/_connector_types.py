# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:24:57 2024

@author: dvezinet
"""


import os


from . import _save2json


#############################################
#############################################
#    Connection types
#############################################


def get(path=None):

    dout = {}

    # -------------
    # MI cables
    # -------------

    dout['cable_MI'] = {
        'description': 'Mineral insulated cables',
    }

    dout['cable_coax'] = {
        'description': 'Coaxial cables',
    }

    dout['cable_twist'] = {
        'description': 'Twisted pair cables',
    }

    dout['cable_wire'] = {
        'description': 'misc wire',
    }

    # -------------
    # power cables
    # -------------

    # DECTRIS power
    dout['power_chord'] = {
        'description': 'power chord',
    }

    # -------------
    # optics fiber
    # -------------

    # SFP+ optics fiber
    dout['fiber_optic']= {
        'description': 'optics fiber',
    }

    # -------------
    # tubes
    # -------------

    # SFP+ optics fiber
    dout['cool'] = {
        'description': 'cooling pipes',
    }

    # ---------------
    # save to json
    # ---------------

    which = os.path.split(__file__)[-1][1:-3]
    return _save2json.main(path=path, dout=dout, which=which)


#############################################
#############################################
#    __main__
#############################################


if __name__ == '__main__':
    get()