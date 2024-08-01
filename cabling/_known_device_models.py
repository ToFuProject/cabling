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
    # CVD diamonds cameras
    # -------------

    dout['CVD'] = {
        'description': 'CVD diamond sensor',
        'connections': {
            'all': {
                'type': "beaded_pair",
                'nb': 1,
            },
        },
    }

    dout['CVD_MI'] = {
        'description': 'CVD cameras MI adapter plate',
        'connections': {
            'all': {
                'type': "MI_Term",
                'nb': 30,
            },
        },
    }

    dout['CVD_Therm'] = {
        'description': 'Thermocouple inside CVD cameras',
        'connections': {
            'all': {'type': "MI_Term"},
        },
    }

    dout['CVD_cam_SXR'] = {
        'description': 'SXR CVD camera',
        'connections': {
            'CVD_in': {
                'type': "MI_Term",
                'nb': 30,
            },
            'Therm_in': {
                'type': "MI_Term",
                'nb': 1,
            },
            'CVD_out': {
                'type': "MI_Term",
                'nb': 30,
            },
            'Therm_out': {
                'type': "MI_Term",
                'nb': 1,
            },
        },
    }

    dout['CVD_cam_HXR'] = {
        'description': 'HXR CVD camera',
        'connections': {
            'CVD_in': {
                'type': "MI_Term",
                'nb': 6,
            },
            'Therm_in': {
                'type': "MI_Term",
                'nb': 1,
            },
            'CVD_out': {
                'type': "MI_Term",
                'nb': 6,
            },
            'Therm_out': {
                'type': "MI_Term",
                'nb': 1,
            },
        },
    }

    # -------------------
    # C-MOD preamplifiers
    # -------------------

    dout['pream_CMOD'] = {
        'description': 'CMOD transimpledance preamplifier boards (x4 channels)',
        'connections': {
            'input': {
                'type': "MI_Term",
                'nb': 6,
            },
            'power': {
                'type': "MI_Term",
                'nb': 1,
            },
            'output': {
                'type': "MI_Term",
                'nb': 6,
            },
        },
    }

    # -------------------
    # CFS DIAG FC
    # -------------------

    dout['DIAG_FC'] = {
        'description': 'Fast controller DIAG edition',
        'connections': {
            'input': {
                'type': "MI_Term",
                'nb': 6,
            },
            'power': {
                'type': "MI_Term",
                'nb': 1,
            },
            'output': {
                'type': "MI_Term",
                'nb': 6,
            },
        },
    }

    # -------------
    # DECTRIS
    # -------------

    # DECTRIS external trigger
    dout['EIGER_2S_500K'] = {
        'description': 'DECTRIS EIGER 2 S 500K',
        'connections': {
            'power': {
                'type': "DECTRIS_pow",
                'nb': 1,
            },
            'data': {
                'type': "SFP+",
                'nb': 1,
            },
            'ext_in': {
                'type': "Lemo® Type 00",
                'nb': 1,
            },
            'ext_out': {
                'type': "Lemo® Type 00",
                'nb': 1,
            },
            'cooling': {
                'type': "DECTRIS_cool",
                'nb': 2,
            },
        },
    }

    # DECTRIS external trigger
    dout['EIGER_2S_1M'] = {
        'description': 'DECTRIS EIGER 2 S 1M',
        'connections': {
            'power': {
                'type': "DECTRIS_pow",
                'nb': 1,
            },
            'data': {
                'type': "SFP+",
                'nb': 2,
            },
            'ext_in': {
                'type': "Lemo® Type 00",
                'nb': 1,
            },
            'ext_out': {
                'type': "Lemo® Type 00",
                'nb': 1,
            },
            'cooling': {
                'type': "DECTRIS_cool",
                'nb': 2,
            },
        },
    }

    # Servers
    dout['EIGER_2S_1M_serv'] = {
        'description': 'DECTRIS EIGER 2 S 1M server, DCU/Dell R7615',
        'sizeU': 2,
        'connections': {
            'power': {
                'type': "DECTRIS_pow",
                'nb': 1,
            },
            'data': {
                'type': "SFP+",
                'nb': 2,
            },
        },
    }


    # -------------
    # HXR scintillators
    # -------------

    # DECTRIS external trigger
    dout['HXR_scinctillator'] = {
        'description': 'DECTRIS EIGER 2 S 1M',
        'connections': {
            'data': {
                'type': "BNC_50H_M",
                'nb': 1,
            },
            'power': {
                'type': "SHV_M",
                'nb': 1,
            },
            'LED': {
                'type': 'fiber optic',
                'nb': 1,
            },
        },
    }

    # -------------
    # HXR scintillators
    # -------------

    # Hamamatsu PMT
    dout['HXR_scint'] = {
        'description': 'HXR scintillators, using Hamamatsu PMT',
        'connections': {
            'data': {
                'type': "BNC_50H_M",
                'nb': 1,
            },
            'power': {
                'type': "SHV_M",
                'nb': 1,
            },
        },
        'url': (
            'https://www.hamamatsu.com/us/en/product/optical-sensors/pmt/pmt_tube-alone/head-on-type/R9420.html',
        ),
    }

    # -------------
    # Pressure transducers
    # -------------

    # Hamamatsu PMT
    dout['Pirani'] = {
        'description': 'Pirani passive gauge heads for VGC094, 	DN 40 CF-F',
        'PN_vendor': '350-423',
        'Prange': [8e-2, 1e5],
        'connections': {
            'data': {
                'type': "BNC_50H_M",
                'nb': 1,
            },
            'power': {
                'type': "SHV_M",
                'nb': 1,
            },
        },
        'url': (
            'https://www.inficon.com/en/products/vacuum-gauge-and-controller/psg01x',
        ),
    }



    return dout