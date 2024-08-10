# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:24:57 2024

@author: dvezinet
"""


import os


import numpy as np


from . import _config
from . import _save2json


#############################################
#############################################
#    utility
#############################################


def keysys(systems, systems_key=_config._SYSTEMS_KEY):
    return '_'.join([
        systems[kk] for kk in systems_key
        if systems.get(kk) is not None
    ])


#############################################
#############################################
#    Connection types
#############################################


def get(path=None):

    dout = {}
    wdm = 'device_model'

    systems0 = {'L1': 'DIAG', 'L2': 'XRAY'}

    # --------------------
    # CVD diamonds cameras
    # --------------------

    # sxr
    _invessel_SXR(dout, wdm, systems0)

    # hxr
    # _invessel_HXR(dout, wdm)

    # # --------------------
    # # Collaborator camera
    # # --------------------

    # _collaborator(dout, wdm)

    # # -----------------
    # # HXR scintillators
    # # -----------------

    # _scintillators(dout, wdm)

    # # -------------
    # # Beamlines
    # # -------------

    # _beamlines(dout, wdm)

    # ---------------
    # add labels if needed
    # ---------------

    for k0, v0 in dout.items():
        dout[k0]['label'] = v0.get('label', k0)

    # ---------------
    # convert arrays to tuples
    # ---------------

    for k0, v0 in dout.items():
        for k1, v1 in v0.get('dcoords', {}).items():
            dout[k0]['dcoords'][k1] = tuple(np.array(v1).astype(float))

    # ---------------
    # save to json
    # ---------------

    which = os.path.split(__file__)[-1][1:-3]
    return _save2json.main(path=path, dout=dout, which=which)


#############################################
#############################################
#    Devices for in-vessel cameras
#############################################


# ##########
# SXR
# ##########


def _invessel_SXR(dout, wdm, systems0):

    # -------------
    # prepare
    # -------------

    systems0 = dict(systems0, L3='SXRVA')

    # coordinates
    dcoords = {
        'OMPu': np.r_[
            np.cos(340*np.pi/180) * 2,
            np.sin(340*np.pi/180) * 2,
            0.8,
        ],
        'OMPl': np.r_[
            np.cos(340*np.pi/180) * 2,
            np.sin(340*np.pi/180) * 2,
            -0.8,
        ],
        'MPPu': np.r_[
            np.cos(340*np.pi/180) * 2,
            np.sin(340*np.pi/180) * 2,
            0.2,
        ],
        'MPPl': np.r_[
            np.cos(340*np.pi/180) * 2,
            np.sin(340*np.pi/180) * 2,
            -0.2,
        ],
        'feed_OMPu': np.r_[
            np.cos(340*np.pi/180) * 4.5,
            np.sin(340*np.pi/180) * 4.5,
            1.2,
        ],
        'feed_OMPl': np.r_[
            np.cos(340*np.pi/180) * 4.5,
            np.sin(340*np.pi/180) * 4.5,
            -1.2,
        ],
        'feed_MPPu': np.r_[
            np.cos(340*np.pi/180) * 4.5,
            np.sin(340*np.pi/180) * 4.5,
            0,
        ],
        'feed_MPPl': np.r_[
            np.cos(340*np.pi/180) * 4.5,
            np.sin(340*np.pi/180) * 4.5,
            0,
        ],
        'preamp': np.r_[
            np.cos(340*np.pi/180) * 5,
            np.sin(340*np.pi/180) * 5,
            -5,
        ],
        'digit': np.r_[
            25,
            -1,
            0,
        ],
    }

    # -----------
    # update
    # -----------

    # ---------------
    # add CVD sensors

    for pp in ['OMPu', 'OMPl', 'MPPu', 'MPPl']:

        systems = dict(systems0, L4=pp)

        systems = dict(systems0, L4=pp)
        keyS = keysys(systems)

        key_plate = f'{keyS}_plate'
        key_cam = f'{keyS}_cam'
        key_feed = f"{keyS}_feed"

        # individual sensors
        for ii in range(15):
            key = f"{keyS}_CVD_{ii:02.0f}"
            dout[key] = {
                'label': f'CVD_{ii:02.0f}',
                wdm: 'CVD',
                'systems': systems,
                'dcoords': {
                    '3d': dcoords[pp],
                },
            }

        # individual thermocouple
        dout[f'{keyS}_therm'] = {
            wdm: 'CVD_Therm',
            'label': 'therm',
            'systems': systems,
            'dcoords': {
                '3d': dcoords[pp],
            },
        }

        # diff
        psi = np.arctan2(dcoords[pp][1], dcoords[pp][0])
        diff = 0.1 * np.r_[np.cos(psi), np.sin(psi), 0]

        # support plate
        dout[key_plate] = {
            wdm: 'CVD_plate_15',
            'label': 'plate',
            'systems': systems,
            'dcoords': {
                '3d': dcoords[pp] + diff,
            },
        }

        # --------------
        # camera

        dout[key_cam] = {
            wdm: 'CVD_cam_15',
            'label': 'cam',
            'systems': systems,
            'dcoords': {
                '3d': dcoords[pp] + 2 * diff,
            },
        }

        # ----------------
        # feedthrough

        dout[key_feed] = {
            wdm: 'feed_CVD',
            'label': 'feed',
            'systems': systems,
            'dcoords': {
                '3d': dcoords[f'feed_{pp}'],
            },
        }

    # -------------
    # preamplifiers

    systems = dict(systems0, L4='ACQ')
    keyS = keysys(systems)

    for ii in range(int(np.ceil((15*4)/4))):

        key = f'sxr_preamp_{ii:02.0f}'
        dout[key] = {
            wdm: 'preamp_CMOD',
            'label': f'preamp_{ii:02.0f}',
            'systems': systems,
            'dcoords': {
                '3d': dcoords['preamp'],
            },

        }

    # -------------
    # digitizers

    for ii in range(int(np.ceil((15*4)/32))):

        key = f'sxr_digit_{ii:02.0f}'
        dout[key] = {
            wdm: 'DIAG_FC',
            'label': f'digit_{ii:02.0f}',
            'systems': systems,
            'dcoords': {
                '3d': dcoords['digit'],
            },
        }

    return


# ##########
# HXR
# ##########


def _invessel_HXR(dout, wdm, systems0):

    systems0 = dict(systems0, L3='HXRVA')

    # -------------
    # system
    # -------------

    systems = {'L1': 'DIAG', 'L2': 'XRAY', 'L3': 'HXR-VA'}

    # -----------
    # update
    # -----------

    # ---------------
    # add CVD sensors

    for pp in ['cw', 'ccw']:

        # individual sensors
        for ii in range(3):
            key = f"hxr_{pp}_CVD_{ii}"
            dout[key] = {
                wdm: 'CVD',
                'systems': systems,
            }

        # individual thrmocouple
        dout[f'hxr_{pp}_therm'] = {
            wdm: 'CVD_Therm',
            'systems': systems,
        }

        # support plate
        dout[f'hxr_{pp}_plate'] = {
            wdm: 'CVD_plate_3',
            'systems': systems,
        }

    # ------------
    # others

    dout.update({

        # ---------------
        # cameras

        'hxr_cw': {
            wdm: 'CVD_cam_3',
            'systems': systems,
        },
        'hxr_ccw': {
            wdm: 'CVD_cam_3',
            'systems': systems,
        },

        # --------------------------
        # transimpedance amplifiers

        'hxr_amp': {
            wdm: 'preamp_CMOD',
            'systems': systems,
        },

        # ---------------------
        # digitizers

        'hxr_digitizer': {
            wdm: 'DIAG_FC',
            'systems': systems,
        },

    })

    return


#############################################
#############################################
#    Devices for collaborator cameras
#############################################


def _collaborator(dout, wdm):

    # -------------
    # system
    # -------------

    systems = {'L1': 'DIAG', 'L2': 'XRAY', 'L3': 'Collab'}

    # -----------
    # update
    # -----------

    dout.update({

        # --------------------
        # In the vacuum vessel

        # camera
        'collab_cam': {
            wdm: 'EIGER_2S_500K',
            'systems': systems,
        },

        # Basement
        'collab_server': {
            wdm: 'EIGER_2S_1M_serv',
            'systems': systems,
        },

        # power supply
        'collab_power': {
            wdm: 'multi_outlet',
            'systems': systems,
        },

        # --------------------
        # Pressure transducers

        # pirani
        'collab_press_pirani': {
            wdm: 'Inficon_Pirani',
            'systems': systems,
        },

        # cold cathode
        'collab_press_cathode': {
            wdm: 'Inficon_ColdCathode',
            'systems': systems,
        },

        # control
        'collab_press_control': {
            wdm: 'Inficon_ColdCathode',
            'systems': systems,
        },

        # Feedthrough
        # 'feedthrough': {
        #     'model': 'Feed_EIGER_2S_500K',
        #     'systems': systems,
        # },

        # ----------
        # Gate Valve

        # main
        'collab_gate': {
            wdm: 'AllMetal_DN63CF',
            'systems': systems,
        },

        # pressure
        'collab_gate': {
            wdm: 'AllMetal_DN40CF',
            'systems': systems,
        },

        # --------
        # Solenoid

        # --------
        # PLC

        # Power supply
        'collab_PLC_PS': {
            wdm: 'PLC_PS',
            'systems': systems,
        },

        # CPU
        'collab_PLC_CPU': {
            wdm: 'PLC_CPU',
            'systems': systems,
        },

    })

    return


#############################################
#############################################
#    Devices for HXR scintillators
#############################################


def _scintillators(dout, wdm):

    # -------------
    # system
    # -------------

    systems = {'L1': 'DIAG', 'L2': 'XRAY', 'L3': 'HXR-TS'}

    # -----------
    # update
    # -----------

    dout.update({

        # ----------------
        # scintillators

        'hxr_scintillator_north': {
            wdm: 'HXR_scintillator',
            'systems': systems,
        },

        'hxr_scintillator_south': {
            wdm: 'HXR_scintillator',
            'systems': systems,
        },

        # ------------------
        # HV power supply

        'hxr_power_HV': {
            wdm: 'HXR_power_HV',
            'systems': systems,
        },

        # -----------------
        # HXR digitizers

        'hxr_digitizer_fast': {
            wdm: 'HXR_digitizer_fast',
            'systems': systems,
        },

        'hxr_digitizer_current': {
            wdm: 'DIAG_FC',
            'systems': systems,
        },

        # -----------------
        # HXR LED

        'hxr_LED_north': {
            wdm: 'HXR_LED',
            'systems': systems,
        },

        'hxr_LED_south': {
            wdm: 'HXR_LED',
            'systems': systems,
        },

    })

    return


#############################################
#############################################
#    Devices for beamlines
#############################################


def _beamlines(dout, wdm):

    # -------------
    # system
    # -------------

    systems = {'L1': 'DIAG', 'L2': 'XRAY', 'L3': 'XRB'}

    lkeyb = [
        'neg_0490',
        'neg_0260',
        'neg_0040',
        'pos_0160',
        'pos_0380',
    ]

    # -----------
    # update
    # -----------

    for kb in lkeyb:

        # beamline key
        keyb = f"xrb_{kb.replace('_', '')}"

        # ------------
        # gate valves

        for jj, gv in enumerate(('AllMetal_DN100CF', 'AllMetal_DN63CF', 'UHV_DN100CF')):
            key = f"{keyb}_GV{jj}"
            dout[key] = {
                wdm: gv,
                'systems': systems,
            }

        # ------------
        # bellows

        for jj, gv in enumerate(('AllMetal_DN100CF', 'AllMetal_DN63CF', 'UHV_DN100CF')):
            key = f"{keyb}_Bellow{jj}"
            dout[key] = {
                wdm: gv,
                'systems': systems,
            }

        # ---------------
        # pressure gauges

        for jj in range(3):

            for gv in ('Inficon_Pirani', 'Inficon_ColdCathode'):
                key = f"{keyb}_Press_{gv}{jj}"
                dout[key] = {
                    wdm: gv,
                    'systems': systems,
                }

            # check valve
            key = f"{keyb}_GAS_check{jj}"
            dout[key] = {
                wdm: 'check_valve',
                'systems': systems,
            }

            # gate valve
            key = f"{keyb}_GAS_GV"
            dout[key] = {
                wdm: 'AllMetal_DN40CF',
                'systems': systems,
            }

    # ----------------------
    # pressure control unit

    for ii in range(8):

        key = f"{keyb}_Press_control{jj}"
        dout[key] = {
            wdm: 'Inficon_Control',
            'systems': systems,
        }

    # -----------------
    # Vertical manifold

    dout[f'xrb_manifold_GV'] = {
        wdm: 'UHV_DN100CF',
        'systems': systems,
    }

    return


#############################################
#############################################
#    Connection types
#############################################


#############################################
#############################################
#    __main__
#############################################


if __name__ == '__main__':
    get()