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
    wtype = 'device_type'
    dout = {}

    # -------------
    # CVD diamonds cameras
    # -------------

    dout['CVD'] = {
        'description': 'CVD diamond sensor',
        'connections': {
            'all': {
                wplug: "wire_bond",
                'nb': 2,
            },
        },
        wtype: 'sensor',
    }

    dout['CVD_MI'] = {
        'description': 'CVD cameras MI adapter plate',
        'connections': {
            'all': {
                wplug: "MI_Term",
                'nb': 30,
            },
        },
        wtype: 'sensor',
    }

    dout['CVD_Therm'] = {
        'description': 'Thermocouple inside CVD cameras',
        'connections': {
            'all': {wplug: "MI_Term"},
        },
        wtype: 'sensor',
    }

    dout['CVD_cam_SXR'] = {
        'description': 'SXR CVD camera',
        'connections': {
            'CVD_in': {
                wplug: "MI_Term",
                'nb': 30,
            },
            'Therm_in': {
                wplug: "MI_Term",
                'nb': 1,
            },
            'CVD_out': {
                wplug: "MI_Term",
                'nb': 30,
            },
            'Therm_out': {
                wplug: "MI_Term",
                'nb': 1,
            },
        },
        wtype: 'sensor',
    }

    dout['CVD_cam_HXR'] = {
        'description': 'HXR CVD camera',
        'connections': {
            'CVD_in': {
                wplug: "MI_Term",
                'nb': 6,
            },
            'Therm_in': {
                wplug: "MI_Term",
                'nb': 1,
            },
            'CVD_out': {
                wplug: "MI_Term",
                'nb': 6,
            },
            'Therm_out': {
                wplug: "MI_Term",
                'nb': 1,
            },
        },
        wtype: 'sensor',
    }

    # -------------------
    # C-MOD preamplifiers
    # -------------------

    dout['pream_CMOD'] = {
        'description': 'CMOD transimpledance preamplifier boards (x4 channels)',
        'connections': {
            'input': {
                wplug: "MI_Term",
                'nb': 6,
            },
            'power': {
                wplug: "MI_Term",
                'nb': 1,
            },
            'output': {
                wplug: "MI_Term",
                'nb': 6,
            },
        },
        wtype: 'amplifier',
    }

    # -------------------
    # CFS DIAG FC
    # -------------------

    dout['DIAG_FC'] = {
        'description': 'Fast controller DIAG edition',
        'connections': {
            'input': {
                wplug: "MI_Term",
                'nb': 6,
            },
            'power': {
                wplug: "MI_Term",
                'nb': 1,
            },
            'output': {
                wplug: "MI_Term",
                'nb': 6,
            },
        },
        wtype: 'digitizer',
    }

    # -------------
    # DECTRIS
    # -------------

    # DECTRIS external trigger
    dout['EIGER_2S_500K'] = {
        'description': 'DECTRIS EIGER 2 S 500K',
        'connections': {
            'power': {
                wplug: "power_AC_US_F",
                'nb': 1,
            },
            'data': {
                'type': "SFP+",
                'nb': 1,
            },
            'ext_in': {
                wplug: "Lemo® Type 00",
                'nb': 1,
            },
            'ext_out': {
                wplug: "Lemo® Type 00",
                'nb': 1,
            },
            'cooling': {
                wplug: "DECTRIS_cool",
                'nb': 2,
            },
        },
        'url': (
            'https://media.dectris.com/filer_public/8e/00/8e00d9d4-0de2-4435-b35e-8c07cec5ba38/technicalspecifications_eiger2_s_500k_v182.pdf',
        ),
        wtype: 'sensor',
    }

    # DECTRIS external trigger
    dout['EIGER_2S_1M'] = {
        'description': 'DECTRIS EIGER 2 S 1M',
        'connections': {
            'power': {
                wplug: "power_AC_US_F",
                'nb': 1,
            },
            'data': {
                wplug: "SFP+",
                'nb': 2,
            },
            'ext_in': {
                wplug: "Lemo® Type 00",
                'nb': 1,
            },
            'ext_out': {
                wplug: "Lemo® Type 00",
                'nb': 1,
            },
            'cooling': {
                wplug: "DECTRIS_cool",
                'nb': 2,
            },
        },
        'url': (
            '',
        ),
        wtype: 'sensor',
    }

    # Servers
    dout['EIGER_2S_1M_serv'] = {
        'description': 'DECTRIS EIGER 2 S 1M server, DCU/Dell R7615',
        'sizeU': 2,
        'connections': {
            'power': {
                wplug: "power_AC_US_M",
                'nb': 2,
            },
            'data': {
                wplug: "SFP+",
                'nb': 2,
            },
        },
        'url': (
            'https://www.dell.com/en-us/shop/dell-poweredge-servers/poweredge-r7615-rack-server/spd/poweredge-r7615/pe_r7615_tm_vi_vp_sb',
        ),
        wtype: 'server',
    }


    # -------------
    # HXR scintillators
    # -------------

    # Scintillators
    dout['HXR_scintillator'] = {
        'description': 'HXR scintillators, using Hamamatsu PMT',
        'connections': {
            'data': {
                wplug: "BNC_50H_M",
                'nb': 1,
            },
            'power': {
                wplug: "SHV_M",
                'nb': 1,
            },
            'LED': {
                wplug: 'fiber optic',
                'nb': 1,
            },
        },
        wtype: 'sensor',
    }

    # digitizer - fast
    dout['HXR_digitizer_fast'] = {
        'description': 'spectroscopy-relevant digitizer',
        'connections': {
            'data': {
                wplug: "",
                'nb': 1,
            },
            'power': {
                wplug: "",
                'nb': 1,
            },
        },
        'url': (
            '',
        ),
        wtype: 'sensor',
    }

    # digitizer - slow
    dout['HXR_digitizer_slow'] = {
        'description': 'current-mode-relevant digitizer',
        'connections': {
            'data': {
                wplug: "",
                'nb': 1,
            },
            'power': {
                wplug: "",
                'nb': 1,
            },
        },
        'url': (
            '',
        ),
        wtype: 'sensor',
    }

    # HV power supply
    dout['HXR_power_HV'] = {
        'description': 'high-voltage power supply for PMT',
        'connections': {
            'outlet': {
                wplug: "",
                'nb': 1,
            },
            'power': {
                wplug: "",
                'nb': 1,
            },
        },
        'url': (
            '',
        ),
        wtype: 'power',
    }

    # LED
    dout['HXR_LED'] = {
        'description': 'LED for gain monitoring',
        'connections': {
            'outlet': {
                wplug: "",
                'nb': 1,
            },
            'power': {
                wplug: "",
                'nb': 1,
            },
        },
        'url': (
            '',
        ),
        wtype: 'power',
    }

    # Pulse generator for LED
    dout['HXR_pulse'] = {
        'description': 'Pulse generator for LED for gain monitoring',
        'connections': {
            'outlet': {
                wplug: "",
                'nb': 1,
            },
            'power': {
                wplug: "",
                'nb': 1,
            },
        },
        'url': (
            '',
        ),
        wtype: 'power',
    }

    # -------------
    # Pressure transducers
    # -------------

    # Pirani gauges, INFICON
    dout['Inficon_Pirani'] = {
        'description': 'Pirani passive gauge heads for VGC094, DN 40 CF-F',
        'PN_vendor': '350-423',
        'Prange': [8e-2, 1e5],
        'connections': {
            'all': {
                wplug: "",
                'nb': 1,
            },
        },
        'url': (
            'https://www.inficon.com/en/products/vacuum-gauge-and-controller/psg01x',
        ),
    }

    # Cold cathod gauges, INFICON
    dout['Inficon_ColdCathode'] = {
        'description': 'Cold cathode gauge heads MAG084 for VGC094, DN 40 CF-F',
        'PN_vendor': '399-850',
        'Bmax': 0.150,
        'Prange': [1e-6, 5e-1],
        'connections': {
            'all': {
                wplug: "",
                'nb': 1,
            },
        },
        'url': (
            'https://www.inficon.com/en/products/vacuum-gauge-and-controller/mag084',
        ),
    }

    # vacuum control, INFICON
    dout['Inficon_Control'] = {
        'description': 'Cold cathode gauge heads MAG084 for VGC094, DN 40 CF-F',
        'options': ('CP 300 C9', 'IF 500 PN'),
        'PN_vendor': '398-401',
        'Bmax': 0.150,
        'Prange': [1e-6, 5e-1],
        'connections': {
            'board1_gauge1': {
                wplug: "",
                'nb': 1,
            },
            'board1_gauge2': {
                wplug: "",
                'nb': 1,
            },
            'board2_gauge1': {
                wplug: "",
                'nb': 1,
            },
            'board2_gauge2': {
                wplug: "",
                'nb': 1,
            },
            'Interface': {
                wplug: "RJ45",
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