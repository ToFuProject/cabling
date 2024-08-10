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

    # ---------------------
    # CVD diamonds cameras
    # ---------------------

    _cvd(dout, wplug, wtype)

    # -------------
    # DECTRIS
    # -------------

    _dectris(dout, wplug, wtype)

    # -------------
    # HXR scintillators
    # -------------

    _scintillators(dout, wplug, wtype)

    # -------------
    # Valves
    # -------------

    _valves(dout, wplug, wtype)

    # -------------
    # Bellows and ceramic breaks
    # -------------

    _bellows_breaks(dout, wplug, wtype)

    # -------------
    # Pressure transducers
    # -------------

    _pressure(dout, wplug, wtype)

    # --------------
    # PLC components
    # --------------

    _plc(dout, wplug, wtype)

    # -------------
    # Power plug
    # -------------

    dout['multi_outlet'] = {
        'description': '6 outlets, US standard, grounded',
        'connections': {
            'plugs': {
                wplug: 'US_B',
                'nb': 6,
            },
        },
        wtype: 'power',
    }

    # ---------------
    # save to json
    # ---------------

    which = os.path.split(__file__)[-1][1:-3]
    return _save2json.main(path=path, dout=dout, which=which)


#############################################
#############################################
#         CVD
#############################################


def _cvd(dout, wplug, wtype):

    # -----------
    # CVD sensor
    # -----------

    dout['CVD'] = {
        'description': 'CVD diamond sensor',
        'connections': {
            'all': {
                wplug: "wire_bond_pair",
                'nb': 1,
            },
        },
        wtype: 'sensor',
    }

    # ---------------------
    # CVD MI adpater plates
    # ---------------------

    dout['CVD_plate_15'] = {
        'description': 'CVD cameras MI adapter plate',
        'connections': {
            'in': {
                wplug: "wire_bond_pair",
                'nb': 15,
            },
            'out': {
                wplug: "MI_Term_pair",
                'nb': 15,
            },
        },
        wtype: 'sensor',
    }

    dout['CVD_plate_3'] = {
        'description': 'CVD cameras MI adapter plate',
        'connections': {
            'in': {
                wplug: "wire_bond_pair",
                'nb': 3,
            },
            'out': {
                wplug: "MI_Term_pair",
                'nb': 3,
            },
        },
        wtype: 'sensor',
    }

    # ------------
    # Thermocouple
    # ------------

    dout['CVD_Therm'] = {
        'description': 'Thermocouple inside CVD cameras',
        'connections': {
            'all': {wplug: "MI_Term"},
        },
        wtype: 'sensor',
    }

    # -----------------
    # whole camera, sxr
    # -----------------

    dout['CVD_cam_15'] = {
        'description': 'SXR CVD camera',
        'connections': {
            'CVD_in': {
                wplug: "MI_Term_pair",
                'nb': 15,
            },
            'Therm_in': {
                wplug: "MI_Term",
                'nb': 1,
            },
            'CVD_out': {
                wplug: "MI_Term_pair",
                'nb': 15,
            },
            'Therm_out': {
                wplug: "MI_Term",
                'nb': 1,
            },
        },
        wtype: 'sensor',
    }

    # -----------------
    # whole camera, hxr
    # -----------------

    dout['CVD_cam_3'] = {
        'description': 'HXR CVD camera',
        'connections': {
            'CVD_in': {
                wplug: "MI_Term_pair",
                'nb': 3,
            },
            'Therm_in': {
                wplug: "MI_Term",
                'nb': 1,
            },
            'CVD_out': {
                wplug: "MI_Term_pair",
                'nb': 3,
            },
            'Therm_out': {
                wplug: "MI_Term",
                'nb': 1,
            },
        },
        wtype: 'sensor',
    }

    # -------------------
    # Feedthrough
    # -------------------

    dout['feed_CVD'] = {
        'description': 'feedthrough for CVDs',
        'connections': {
            'CVD_in': {
                wplug: "MI_Term_pair",
                'nb': 32,
            },
            'CVD_out': {
                wplug: "MI_Term_pair",
                'nb': 32,
            },
        },
    }

    # -------------------
    # C-MOD preamplifiers
    # -------------------

    dout['preamp_CMOD'] = {
        'description': 'CMOD transimpledance preamplifier boards (x4 channels)',
        'sizeU': 3,
        'chassis': 'Eurocard',
        'connections': {
            'input': {
                wplug: "MI_Term",
                'nb': 4,
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

    dout['VME'] = {
        'description': 'chassis for CMOD transimpledance preamplifiers',
        'sizeU': 3,
        'chassis': 'Eurocard',
        'connections': {
            'input': {
                wplug: "MI_Term",
                'nb': 6,
            },
            'power': {
                wplug: "power_AC_US",
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
                wplug: "VHCDI",
                'nb': 4,
            },
            'power': {
                wplug: "power_AC_US",
                'nb': 1,
            },
            'network_10Gb': {
                wplug: "SFP+",
                'nb': 1,
            },
            'network_2Gb': {
                wplug: "RJ45",
                'nb': 1,
            },
        },
        wtype: 'digitizer',
    }

    return


#############################################
#############################################
#         Dectris
#############################################


def _dectris(dout, wplug, wtype):

    # DECTRIS external trigger
    dout['EIGER_2S_500K'] = {
        'description': 'DECTRIS EIGER 2 S 500K',
        'connections': {
            'power': {
                wplug: "power_AC_US",
                'nb': 1,
            },
            'data': {
                wplug: "SFP+",
                'nb': 1,
            },
            'ext_in': {
                wplug: "Lemo00",
                'nb': 1,
            },
            'ext_out': {
                wplug: "Lemo00",
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
                wplug: "power_AC_US",
                'nb': 1,
            },
            'data': {
                wplug: "SFP+",
                'nb': 2,
            },
            'ext_in': {
                wplug: "Lemo00",
                'nb': 1,
            },
            'ext_out': {
                wplug: "Lemo00",
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
                wplug: "power_AC_US",
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

    return


#############################################
#############################################
#         Scintillators
#############################################


def _scintillators(dout, wplug, wtype):

    # -------------
    # Scintillators

    dout['HXR_scintillator'] = {
        'description': 'HXR scintillators, using Hamamatsu PMT',
        'connections': {
            'data': {
                wplug: "BNC",
                'nb': 1,
            },
            'power': {
                wplug: "SHV",
                'nb': 1,
            },
            'LED': {
                wplug: 'optical',
                'nb': 1,
            },
        },
        wtype: 'sensor',
    }

    # ----------------
    # digitizer - fast

    dout['HXR_digitizer_fast'] = {
        'description': 'spectroscopy-relevant digitizer',
        'sizeU': 6,
        'chassis': 'VMEX64',
        'PN_vendor': 'Caen:VX2730',
        'connections': {
            'data': {
                wplug: "MCX",
                'nb': 32,
            },
            'network': {
                wplug: 'SFP+',
                'nb': 1,
            },
            'usb': {
                wplug: 'usb_c',
                'nb': 1,
            },
            'TRG-IN': {
                wplug: 'Lemo00',
            },
            'TRG-OUT': {
                wplug: 'Lemo00',
            },
            'GPIO': {
                wplug: 'Lemo00',
            },
            'S-IN': {
                wplug: 'Lemo00',
            },
        },
        'url': (
            'https://www.caen.it/subfamilies/2730-digitizer-family/',
        ),
        wtype: 'sensor',
    }

    # ---------------
    # HV power supply

    dout['HXR_power_HV'] = {
        'description': 'high-voltage power supply for PMT',
        'PN_vendor': 'Caen:R8033',
        'sizeU': 3,
        'chassis': '19"',
        'connections': {
            'outlet': {
                wplug: "SHV",
                'nb': 8,
            },
            'network': {
                wplug: "RJ45",
                'nb': 1,
            },
            'power': {
                wplug: "power_AC_US",
            },
        },
        'url': (
            'https://www.caen.it/subfamilies/up-to-6-kv-family-r803x/',
        ),
        wtype: 'power',
    }

    # -----------
    # LED

    dout['HXR_LED'] = {
        'description': 'LED for gain monitoring',
        'connections': {
            'outlet': {
                wplug: "optical",
                'nb': 1,
            },
            # 'power': {
            #     wplug: "",
            #     'nb': 1,
            # },
        },
        'url': (
            '',
        ),
        wtype: 'actuator',
    }

    # # Pulse generator for LED
    # dout['HXR_pulse'] = {
    #     'description': 'Pulse generator for LED for gain monitoring',
    #     'connections': {
    #         'outlet': {
    #             wplug: "",
    #             'nb': 1,
    #         },
    #         'power': {
    #             wplug: "",
    #             'nb': 1,
    #         },
    #     },
    #     'url': (
    #         'https://www.keysight.com/us/en/product/33220A/function--arbitrary-waveform-generator-20-mhz.html',
    #     ),
    #     wtype: 'power',
    # }

    return


#############################################
#############################################
#         Valves
#############################################


def _valves(dout, wplug, wtype):

    # -----------------------
    # All-metal gate valves
    # ----------------------

    # ------------
    # DN100CF

    dout['AllMetal_DN100CF'] = {
        'description': 'VAT all-metal gate vale DN100CF',
        'PN': '0088528',
        'PN_vendor': 'VAT:48240-CE24-AWO1',
        'connections': {
            'CDA_close': {
                wplug: "ISO_1/8",
            },
            'CDA_open': {
                wplug: "ISO_1/8",
            },
            'position': {
                wplug: "VAT_position",
            },
            'interspace_pump': {
                wplug: 'VCR_1/4',
            },
            'vacuum': {
                wplug: "DN100CF",
            },
        },
        'url': (
            'https://tcprod.cfsenergy.com/#/teamcenter.search.search?searchCriteria=0088528&secondaryCriteria=*&filter=Categorization.category%3DParts',
        ),
        wtype: 'actuator',
    }

    # ------------
    # DN63CF

    dout['AllMetal_DN63CF'] = {
        'description': 'VAT all-metal gate vale DN63CF',
        'PN': '0089325',
        'PN_vendor': 'VAT:48236-CE24-AW01',
        'connections': {
            'CDA_close': {
                wplug: "ISO_1/8",
            },
            'CDA_open': {
                wplug: "ISO_1/8",
            },
            'position': {
                wplug: "VAT_position",
            },
            'interspace_pump': {
                wplug: 'VCR_1/4',
            },
            'vacuum': {
                wplug: "DN63CF",
            },
        },
        'url': (
            'https://tcprod.cfsenergy.com/#/teamcenter.search.search?searchCriteria=0089325&secondaryCriteria=*&filter=Categorization.category%3DParts',
        ),
        wtype: 'actuator',
    }

    # ------------
    # DN40CF

    dout['AllMetal_DN40CF'] = {
        'description': 'VAT all-metal gate vale DN40CF',
        'PN': '0088529',
        'PN_vendor': 'VAT:48132-CE24-AWO1',
        'connections': {
            'CDA_close': {
                wplug: "ISO_1/8",
            },
            'CDA_open': {
                wplug: "ISO_1/8",
            },
            'position': {
                wplug: "VAT_position",
            },
            'interspace_pump': {
                wplug: 'VCR_1/4',
            },
            'vacuum': {
                wplug: "DN40CF",
            },
        },
        'url': (
            'https://tcprod.cfsenergy.com/#/teamcenter.search.search?searchCriteria=DN%2040%20CF%20PNEUMATIC%20ALL%20METAL&secondaryCriteria=*&filter=Categorization.category%3DParts',
        ),
        wtype: 'actuator',
    }

    # ---------------
    # UHV gate valves
    # ---------------

    # ------------
    # DN100CF

    dout['UHV_DN100CF'] = {
        'description': 'VAT UHV gate vale DN100CF',
        'PN': '0088559',
        'PN_vendor': 'VAT:10836-CE24-BMU1',
        'connections': {
            'CDA_close': {
                wplug: "ISO_1/8",
            },
            'CDA_open': {
                wplug: "ISO_1/8",
            },
            'position': {
                wplug: "VAT_position",
            },
            'vacuum': {
                wplug: "DN100CF",
            },
        },
        'url': (
            'https://tcprod.cfsenergy.com/#/teamcenter.search.search?searchCriteria=DN%20100%20CF%20PNEUMATIC%20UHV%20GATE&secondaryCriteria=*&filter=Categorization.category%3DParts',
        ),
        wtype: 'actuator',
    }

    # ------------
    # DN40CF

    dout['UHV_DN40CF'] = {
        'description': 'VAT UHV gate vale DN40CF',
        'PN': '0088558',
        'PN_vendor': 'VAT:01032-CE24-BNL1',
        'connections': {
            'CDA_close': {
                wplug: "ISO_1/8",
            },
            'CDA_open': {
                wplug: "ISO_1/8",
            },
            'position': {
                wplug: "VAT_position",
            },
            'vacuum': {
                wplug: "DN40CF",
            },
        },
        'url': (
            'https://tcprod.cfsenergy.com/#/teamcenter.search.search?searchCriteria=DN%2040%20CF%20PNEUMATIC%20UHV%20GATE&secondaryCriteria=*&filter=Categorization.category%3DParts',
        ),
        wtype: 'actuator',
    }

    # ---------------
    # Gas valves
    # ---------------

    dout['gas_valve'] = {
        'description': 'regular pneumatic gas valve',
        'PN': '0092192',
        'PN_vendor': 'APTech:AZ3540S-2PW-MV4-MV4',
        'connections': {
            'inlet': {
                wplug: "VCR_1/4",
            },
            'outlet': {
                wplug: "VCR_1/4",
            },
            'actuation': {
                wplug: "ISO_1/8",
            },
        },
        'url': (
            'https://tcprod.cfsenergy.com/#/teamcenter.search.search?searchCriteria=0092192&secondaryCriteria=*&filter=Categorization.category%3DParts',
        ),
        wtype: 'actuator',
    }

    # ---------------
    # Check valves
    # ---------------

    dout['check_valve'] = {
        'description': 'regular check valve',
        'PN': '0092193',
        'PN_vendor': 'swagelok:6L-CW4FR4-VR4',
        'connections': {
            'inlet': {
                wplug: "VCR_1/4",
            },
            'outlet': {
                wplug: "VCR_1/4",
            },
        },
        'url': (
            'https://products.swagelok.com/en/c/fixed-pressure/p/6L-CW4FR4-VR4',
        ),
        wtype: 'actuator',
    }


    return


# ############################################
# ############################################
#         Bellows and ceramic breaks
# ############################################


def _bellows_breaks(dout, wplug, wtype):

    # -------------------------------
    # Double-ply hydroformed bellows
    # -------------------------------

    dout['Bellow_DP_DN100CF'] = {
        'description': 'Double-ply hydroformed bellow, DN 100 CF',
        'PN': '',
        'PN_vendor': '',
        'connections': {
            'in': {
                wplug: "InficonPirani",
            },
            'out': {
                wplug: "DN40CF",
            },
        },
        'url': (
            '',
        ),
        wtype: 'sensor',
    }

    return


#############################################
#############################################
#         Pressure transducers
#############################################


def _pressure(dout, wplug, wtype):

    # ----------------------
    # Pirani gauges, INFICON
    # ----------------------

    dout['Inficon_Pirani'] = {
        'description': 'Pirani passive gauge heads for VGC094, DN 40 CF-F',
        'PN_vendor': 'Inficon:350-423',
        'Prange': [8e-2, 1e5],
        'connections': {
            'all': {
                wplug: "InficonPirani",
            },
            'vacuum': {
                wplug: "DN40CF",
            },
        },
        'url': (
            'https://www.inficon.com/en/products/vacuum-gauge-and-controller/psg01x',
        ),
        wtype: 'sensor',
    }

    # ---------------------------
    # Cold cathod gauges, INFICON
    # ---------------------------

    dout['Inficon_ColdCathode'] = {
        'description': 'Cold cathode gauge heads MAG084 for VGC094, DN 40 CF-F',
        'PN_vendor': 'Inficon:399-850',
        'Bmax': 0.150,
        'Prange': [1e-6, 5e-1],
        'connections': {
            'all': {
                wplug: "InficonColdCath",
                'nb': 1,
            },
        },
        'url': (
            'https://www.inficon.com/en/products/vacuum-gauge-and-controller/mag084',
        ),
        wtype: 'sensor',
    }

    # -----------------------
    # vacuum control, INFICON
    # -----------------------

    dout['Inficon_Control'] = {
        'description': 'Cold cathode gauge heads MAG084 for VGC094, DN 40 CF-F',
        'options': ('CP 300 C9', 'IF 500 PN'),
        'PN_vendor': 'Inficon:398-401',
        'connections': {
            'board1_gauge1': {
                wplug: "InficonPirani",
                'nb': 1,
            },
            'board1_gauge2': {
                wplug: "InficonColdCath",
                'nb': 1,
            },
            'board2_gauge1': {
                wplug: "InficonPirani",
                'nb': 1,
            },
            'board2_gauge2': {
                wplug: "InficonColdCath",
                'nb': 1,
            },
            'network': {
                wplug: 'RJ45',
                'nb': 2,
            },
            'power': {
                wplug: 'power_AC_US',
            },
        },
        'url': (
            'https://www.inficon.com/en/products/vacuum-gauge-and-controller/vgc094',
        ),
        wtype: 'controller',
    }

    return


#############################################
#############################################
#             PLC
#############################################


def _plc(dout, wplug, wtype):

    # --------
    # CPU

    dout['PLC_CPU'] = {
        'description': '',
        'PN': '0092665',
        'PN_vendor': 'Siemens:6ES75163AP030AB0',
        'connections': {
            'PROFINET': {
                wplug: 'RJ45',
                'nb': 2,
            },
            'PROFINET_RT': {
                wplug: 'RJ45',
                'nb': 1,
            },
            'PROFIBUS': {
                wplug: 'RS485',
                'nb': 1,
                'url': (
                    'https://en.wikipedia.org/wiki/Profibus',
                ),
            },
        },
        'url': (
            'file:///C:/Users/dvezinet/Documents/Procurement/Beamlines_IC/PLC/PLC_CPU_6ES75163AN020AB0_datasheet_en.pdf',
            'https://mall.industry.siemens.com/mall/en/us/Catalog/Product/6ES7516-3AP03-0AB0',
        ),
        wtype: 'controller',
    }

    # ------------
    # Power Supply

    dout['PLC_PS'] = {
        'description': 'output: 24 V DC/3 A power supply for SIMATIC S7-1500',
        'PN': '0092666',
        'PN_vendor': 'Siemens:6EP13324BA00',
        'connections': {
            'power_in': {
                wplug: '1phase_AC_US',
                'nb': 1,
            },
            'power_out': {
                wplug: 'power_bus_24V',
                'nb': 1,
            },
            'output': {
                wplug: 'wire_pair_LV',
                'nb': 2,
            },
        },
        'url': (
            'https://mall.industry.siemens.com/mall/en/us/Catalog/Product/6EP13324BA00',
        ),
        wtype: 'controller',
    }

    # ------------
    # Memory

    dout['PLC_MemCard'] = {
        'description': 'Memory card',
        'specs': '256 Mb',
        'PN_vendor': 'Siemens:6ES7954-8LL04-0AA0',
        'connections': {
            'mem': {
                wplug: 'MemCard',
                'nb': 1,
            },
        },
        'url': (
            'https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/6ES7954-8LL04-0AA0',
        ),
        wtype: 'controller',
    }

    # --------------
    # Communication

    dout['PLC_Com'] = {
        'description': 'Communication module',
        'PN': '0092667',
        'PN_vendor': 'Siemens:6ES7541-1AB00-0AB0',
        'connections': {
            'power_in': {
                wplug: 'power_bus_24V',
                'nb': 1,
            },
            'power_out': {
                wplug: 'power_bus_24V',
                'nb': 1,
            },
            'RS422': {
                wplug: 'RS422',
                'nb': 1,
            },
            'RS485': {
                wplug: 'RS485',
                'nb': 1,
            },
        },
        'url': (
            'https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/6ES7541-1AB00-0AB0',
        ),
        wtype: 'controller',
    }

    # --------------
    # Digital output

    dout['PLC_DOut'] = {
        'description': 'Digital output module, 16 channels',
        'PN': '0092668',
        'PN_vendor': 'Siemens:6ES7522-1BH01-0AB0',
        'connections': {
            'power_in': {
                wplug: 'power_bus_24V',
                'nb': 1,
            },
            'power_out': {
                wplug: 'power_bus_24V',
                'nb': 1,
            },
            'digital_out': {
                wplug: 'wire_pair_LV',
                'nb': 16,
                'comments': 'each channel is a pair of cables with 0.5 A (True) or 0.5 mA (False)',
            },
        },
        'url': (
            'https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/6ES7522-1BH01-0AB0',
        ),
        wtype: 'controller',
    }

    # --------------
    # Digital input

    dout['PLC_DIn'] = {
        'description': 'Digital input module, 16 channels, 24 V DC',
        'spec': 'False: -30 to +5 V, True: +11 to +30V',
        'PN': '0092676',
        'PN_vendor': '6ES75211BH100AA0',
        'connections': {
            'power_in': {
                wplug: 'power_bus_24V',
                'nb': 1,
            },
            'power_out': {
                wplug: 'power_bus_24V',
                'nb': 1,
            },
            'digital_out': {
                wplug: 'wire_pair_LV',
                'nb': 16,
                'comments': 'each channel is a pair of cables with 0.5 A (True) or 0.5 mA (False)',
            },
        },
        'url': (
            'https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/6ES7521-1BH10-0AA0',
        ),
        wtype: 'controller',
    }

    # ------------
    # Analog input

    dout['PLC_AIn'] = {
        'description': 'Analog input module, digitizes on 16 bits on 2.5-100 ms',
        'PN': '0092684',
        'PN_vendor': 'Siemens:6ES75317KF000AB0',
        'connections': {
            'power_in': {
                wplug: 'power_bus_24V',
                'nb': 1,
            },
            'power_out': {
                wplug: 'power_bus_24V',
                'nb': 1,
            },
            'analog_in_V': {
                wplug: 'wire_pair_LV',
                'nb': 8,
                'comments': '8 for voltage (up to -10/+10 V)',
            },
            'analog_in_I': {
                wplug: 'wire_pair_LV',
                'nb': 8,
                'comments': '8 for current (up to -20/+20 mA)',
            },
        },
        'url': (
            'https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/6ES7531-7KF00-0AB0',
        ),
        wtype: 'controller',
    }

    # -------------
    # Mounting rail

    dout['PLC_Rail'] = {
        'description': 'Mounting rail in a rack',
        'PN_vendor': 'Siemens:6ES7590-1AB60-0AA0',
        'connections': {
            '': {
                wplug: 'rail',
                'nb': 32,
            },
        },
        'url': (
            'https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/6ES7590-1AB60-0AA0',
        ),
        wtype: 'mechanical',
    }

    return


#############################################
#############################################
#                 __main__
#############################################


if __name__ == '__main__':
    get()