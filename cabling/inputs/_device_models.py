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

    # Pirani gauges, INFICON
    dout['Pirani'] = {
        'description': 'Pirani passive gauge heads for VGC094, DN 40 CF-F',
        'PN_vendor': '350-423',
        'Prange': [8e-2, 1e5],
        'connections': {
            'all': {
                'type': "",
                'nb': 1,
            },
        },
        'url': (
            'https://www.inficon.com/en/products/vacuum-gauge-and-controller/psg01x',
        ),
    }

    # Cold cathod gauges, INFICON
    dout['ColdCathode'] = {
        'description': 'Cold cathode gauge heads MAG084 for VGC094, DN 40 CF-F',
        'PN_vendor': '399-850',
        'Bmax': 0.150,
        'Prange': [1e-6, 5e-1],
        'connections': {
            'all': {
                'type': "",
                'nb': 1,
            },
        },
        'url': (
            'https://www.inficon.com/en/products/vacuum-gauge-and-controller/mag084',
        ),
    }

    # vacuum control, INFICON
    dout['ColdCathode'] = {
        'description': 'Cold cathode gauge heads MAG084 for VGC094, DN 40 CF-F',
        'options': ('CP 300 C9', 'IF 500 PN'),
        'PN_vendor': '398-401',
        'Bmax': 0.150,
        'Prange': [1e-6, 5e-1],
        'connections': {
            'board1_gauge1': {
                'type': "",
                'nb': 1,
            },
            'board1_gauge2': {
                'type': "",
                'nb': 1,
            },
            'board2_gauge1': {
                'type': "",
                'nb': 1,
            },
            'board2_gauge2': {
                'type': "",
                'nb': 1,
            },
            'Interface': {
                'type': "RJ45",
                'nb': 2,
            },
            'power': {

            },

        },
        'url': (
            'https://www.inficon.com/en/products/vacuum-gauge-and-controller/vgc094',
        ),
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