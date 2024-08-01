# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:24:57 2024

@author: dvezinet
"""

from . import _known_connections

#############################################
#############################################
#    Connection types
#############################################


def get():

    dout = {}

    # -------------
    # coax BNC cables
    # -------------

    for imp in ['50Hz', '75Hz']:
        for mf in [('M', 'F'), ('M', 'M'), ('F', 'F')]:
            key = f"coax_BNC_{imp}_{''.join(mf)}"
            dout[key] = {
                'description': f'coaxial cable with {mf} connections',
                'connections': {
                    'ptA': {'type': f"BNC_{imp}_{mf[0]}"},
                    'ptB': {'type': f"BNC_{imp}_{mf[1]}"},
                },
            }

    # -------------
    # coax SHV cables
    # -------------

    for mf in [('M', 'F'), ('M', 'M'), ('F', 'F')]:
        key = f"coax_SHV_{imp}_{''.join(mf)}"
        dout[key] = {
            'description': f'coaxial cable with {mf} connections',
            'connections': {
                'ptA': {'type': f"SHV_{mf[0]}"},
                'ptB': {'type': f"SHV_{mf[1]}"},
            },
        }

    # -------------
    # MI cables
    # -------------

    dout['MI'] = {
        'description': 'Mineral insulated cable',
        'connections': {
            'ptA': {'type': "MI_Term"},
            'ptB': {'type': "MI_Term"},
        },
    }

    dout['MI_twist'] = {
        'description': 'Mineral insulated twisted pair',
        'connections': {
            'ptA': {'type': "MI_Term"},
            'ptB': {'type': "MI_Term"},
        },
    }

    dout['beaded_pair'] = {
        'description': 'pair of naked wired with ceramic beads',
        'connections': {
            'ptA': {'type': "wire_bond"},
            'ptB': {'type': "wire_bond"},
        },
    }

    # -------------
    # Lemo cables
    # -------------


    # DECTRIS external trigger
    dout['coax_Lemo'] = {
        'description': 'coaxial cable with Lemo® Type 00 (NIM/CAMAC)',
        'connections': {
            'ptA': {'type': "Lemo® Type 00"},
            'ptB': {'type': "Lemo® Type 00"},
        },
    }

    # -------------
    # power cables
    # -------------

    # DECTRIS power
    dout['DECTRIS_pow'] = {
        'description': 'power cable for DECTRIS EIGER 2 S 500K',
        'connections': {
            'ptA': {'type': "DECTRIS_pow"},
            'ptB': {'type': "DECTRIS_pow"},
        },
    }

    # -------------
    # poptics fiber
    # -------------

    # SFP+ optics fiber
    dout['10Gb_SM']= {
        'description': '10 GbE-LR single mode optic fiber for DECTRIS EIGER 2',
        'connections': {
            'ptA': {'type': "SFP+"},
            'ptB': {'type': "SFP+"},
        },
    }

    # -------------
    # tubes
    # -------------

    # SFP+ optics fiber
    dout['DECTRIS_cool'] = {
        'description': 'cooling pipes connections for DECTRIS cameras',
        'connections': {
            'ptA': {'type': "DECTRIS_cool"},
            'ptB': {'type': "DECTRIS_cool"},
        },
    }

    return dout