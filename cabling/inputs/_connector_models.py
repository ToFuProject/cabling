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

    wplug = 'plug_type'
    wfam = 'connector_family'
    dout = {}

    # -------------
    # coax BNC cables
    # -------------

    for imp in ['50Hz', '75Hz']:
        for mf in [('M', 'F'), ('M', 'M'), ('F', 'F')]:
            key = f"BNC_{imp}_{''.join(mf)}"
            dout[key] = {
                'description': f'coaxial cable with {mf} connections',
                'connections': {
                    'ptA': {wplug: f"BNC_{imp}_{mf[0]}"},
                    'ptB': {wplug: f"BNC_{imp}_{mf[1]}"},
                },
                wfam: 'cable_coax',
            }

    # -------------
    # coax SHV cables
    # -------------

    for mf in [('M', 'F'), ('M', 'M'), ('F', 'F')]:
        key = f"SHV_{imp}_{''.join(mf)}"
        dout[key] = {
            'description': f'coaxial cable with {mf} connections',
            'connections': {
                'ptA': {wplug: f"SHV_{mf[0]}"},
                'ptB': {wplug: f"SHV_{mf[1]}"},
            },
            wfam: 'cable_coax',
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
        wfam: 'cable_MI',
    }

    dout['MI_twist'] = {
        'description': 'Mineral insulated twisted pair',
        'connections': {
            'ptA': {wplug: "MI_Term"},
            'ptB': {wplug: "MI_Term"},
        },
        wfam: 'cable_MI',
    }

    dout['beaded_pair'] = {
        'description': 'pair of naked wired with ceramic beads',
        'connections': {
            'ptA': {wplug: "wire_bond"},
            'ptB': {wplug: "wire_bond"},
        },
        wfam: 'cable_wire',
    }

    # -------------
    # Lemo cables
    # -------------

    # DECTRIS external trigger
    dout['coax_Lemo'] = {
        'description': 'coaxial cable with Lemo® Type 00 (NIM/CAMAC)',
        'connections': {
            'ptA': {wplug: "Lemo® Type 00"},
            'ptB': {wplug: "Lemo® Type 00"},
        },
        wfam: 'cable_coax',
    }

    # -------------
    # power cables
    # -------------

    # standard power chord
    dout['power_F'] = {
        'description': 'power chord US F',
        'connections': {
            'ptA': {wplug: "power_AC_US_F"},
            'ptB': {wplug: "US_A_M"},
        },
        wfam: 'power_chord',
    }

    # standard DECTRIS power chord for EIGER 2 S 500 K
    dout['power_DECTRIS'] = {
        'description': 'power chord DECTRIS 2 S 500 K',
        'connections': {
            'ptA': {wplug: "DECTRIS_pow_AC"},
            'ptB': {wplug: "DECTRIS_pow_DC"},
        },
        wfam: 'power_chord',
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
        wfam: 'fiber_optic',
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
        wfam: 'cool',
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