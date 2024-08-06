# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:24:57 2024

@author: dvezinet
"""


import os


from . import _save2json


#############################################
#############################################
#    Connector models
#############################################


def get(path=None):

    wplug = 'plug_type'
    wtype = 'connector_type'
    dout = {}

    # -------------
    # coax BNC cables
    # -------------

    dout['BNC'] = {
        'description': f'coaxial cable with BNC plugs',
        'connections': {
            'ptA': {wplug: "BNC"},
            'ptB': {wplug: "BNC"},
        },
        wtype: 'cable_coax',
    }

    # -------------
    # coax SHV cables
    # -------------

    dout['SHV'] = {
        'description': f'coaxial cable with SHV plugs',
        'connections': {
            'ptA': {wplug: "SHV"},
            'ptB': {wplug: "SHV"},
        },
        wtype: 'cable_coax',
    }

    # -------------
    # MI cables
    # -------------

    dout['MI_single'] = {
        'description': 'Mineral insulated cable',
        'connections': {
            'ptA': {wplug: "MI_Term"},
            'ptB': {wplug: "MI_Term"},
        },
        wtype: 'cable_MI',
    }

    dout['MI_twist_pair'] = {
        'description': 'Mineral insulated twisted pair',
        'connections': {
            'ptA': {wplug: "MI_Term"},
            'ptB': {wplug: "MI_Term"},
        },
        wtype: 'cable_MI',
    }

    dout['microwire_pair'] = {
        'description': 'pair of naked microwires',
        'connections': {
            'ptA': {wplug: "wire_bond_pair"},
            'ptB': {wplug: "wire_bond_pair"},
        },
        wtype: 'cable_wire',
    }

    dout['wire_pair'] = {
        'description': 'pair of naked wires with ceramic beads',
        'connections': {
            'ptA': {wplug: "wire_bond_pair"},
            'ptB': {wplug: "wire_bond_pair"},
        },
        wtype: 'cable_wire',
    }

    # -------------
    # Lemo cables
    # -------------

    # Lemo
    dout['Lemo00'] = {
        'description': 'coaxial cable with Lemo® Type 00 (NIM/CAMAC)',
        'connections': {
            'ptA': {wplug: "Lemo00"},
            'ptB': {wplug: "Lemo00"},
        },
        'url': (
            '',
        ),
        wtype: 'cable_coax',
    }

    # -------------
    # power cables
    # -------------

    # standard power chord
    dout['power'] = {
        'description': 'power chord US',
        'connections': {
            'ptA': {wplug: "power_AC_US"},
            'ptB': {wplug: "US_A"},
        },
        wtype: 'power_chord',
    }

    # standard DECTRIS power chord for EIGER 2 S 500 K
    dout['power_DECTRIS'] = {
        'description': 'power chord DECTRIS 2 S 500 K',
        'connections': {
            'ptA': {wplug: "DECTRIS_pow_AC"},
            'ptB': {wplug: "DECTRIS_pow_DC"},
        },
        wtype: 'power_chord',
    }

    # -------------
    # poptics fiber
    # -------------

    # SFP+ optics fiber
    dout['10Gb_SM']= {
        'description': '10 GbE-LR single mode optic fiber for DECTRIS EIGER 2',
        'connections': {
            'ptA': {wplug: "SFP+"},
            'ptB': {wplug: "SFP+"},
        },
        wtype: 'fiber_optic',
    }

    # -------------
    # tubes
    # -------------

    # SFP+ optics fiber
    dout['DECTRIS_cool'] = {
        'description': 'cooling pipes connections for DECTRIS cameras',
        'connections': {
            'ptA': {wplug: "DECTRIS_cool"},
            'ptB': {wplug: "DECTRIS_cool"},
        },
        wtype: 'cool',
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