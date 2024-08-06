# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:24:57 2024

@author: dvezinet
"""


import os


import numpy as np


from . import _save2json


#############################################
#############################################
#    Connection types
#############################################


def get(path=None):

    dout = {}
    wdm = 'device_model'

    # --------------------
    # CVD diamonds cameras
    # --------------------

    # sxr
    _invessel_SXR(dout, wdm)

    # hxr
    _invessel_HXR(dout, wdm)

    # --------------------
    # Collaborator camera
    # --------------------

    _collaborator(dout, wdm)

    # -----------------
    # HXR scintillators
    # -----------------

    _scintillators(dout, wdm)

    # -------------
    # Beamlines
    # -------------

    _beamlines(dout, wdm)

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


def _invessel_SXR(dout, wdm):

    # -------------
    # system
    # -------------

    systems = ('DIAG', 'XRAY', 'SXR-VA')

    # -----------
    # update
    # -----------

    # ---------------
    # add CVD sensors

    for pp in ['OMPu', 'OMPl', 'MPPu', 'MPPl']:

        key_plate = f'sxr_{pp}_plate'
        key_cam = f'sxr_{pp}_cam'
        key_feed = f"sxr_{pp}_feed"

        # individual sensors
        for ii in range(15):
            key = f"sxr_{pp}_CVD_{ii}"
            dout[key] = {
                wdm: 'CVD',
                'Systems': systems,
            }

        # individual thermocouple
        dout[f'sxr_{pp}_therm'] = {
            wdm: 'CVD_Therm',
            'Systems': systems,
        }

        # support plate
        dout[key_plate] = {
            wdm: 'CVD_plate_15',
            'Systems': systems,
        }

        # --------------
        # camera

        dout[key_cam] = {
            wdm: 'CVD_cam_15',
            'Systems': systems,
        }

        # ----------------
        # feedthrough

        dout[key_feed] = {
            wdm: 'feed_CVD',
            'Systems': systems,
        }


    # -------------
    # preamplifiers

    for ii in range(int(np.ceil((15*4)/4))):

        key = f'sxr_preamp{ii}'
        dout[key] = {
            wdm: 'preamp_CMOD',
            'Systems': systems,
        }

    # -------------
    # digitizers

    for ii in range(int(np.ceil((15*4)/32))):

        key = f'sxr_digit{ii}'
        dout[key] = {
            wdm: 'DIAG_FC',
            'Systems': systems,
        }

    return


# ##########
# HXR
# ##########


def _invessel_HXR(dout, wdm):

    # -------------
    # system
    # -------------

    systems = ('DIAG', 'XRAY', 'HXR-VA')

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
                'Systems': systems,
            }

        # individual thrmocouple
        dout[f'hxr_{pp}_therm'] = {
            wdm: 'CVD_Therm',
            'Systems': systems,
        }

        # support plate
        dout[f'hxr_{pp}_plate'] = {
            wdm: 'CVD_plate_3',
            'Systems': systems,
        }

    # ------------
    # others

    dout.update({

        # ---------------
        # cameras

        'hxr_cw': {
            wdm: 'CVD_cam_3',
            'Systems': systems,
        },
        'hxr_ccw': {
            wdm: 'CVD_cam_3',
            'Systems': systems,
        },

        # --------------------------
        # transimpedance amplifiers

        'hxr_amp': {
            wdm: 'preamp_CMOD',
            'Systems': systems,
        },

        # ---------------------
        # digitizers

        'hxr_digitizer': {
            wdm: 'DIAG_FC',
            'Systems': systems,
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

    systems = ('DIAG', 'XRAY', 'Collab')

    # -----------
    # update
    # -----------

    dout.update({

        # --------------------
        # In the vacuum vessel

        # camera
        'collab_cam': {
            wdm: 'EIGER_2S_500K',
            'Systems': systems,
        },

        # Basement
        'collab_server': {
            wdm: 'EIGER_2S_1M_serv',
            'Systems': systems,
        },

        # power supply
        'collab_power': {
            wdm: 'multi_outlet',
            'Systems': systems,
        },

        # --------------------
        # Pressure transducers

        # pirani
        'collab_press_pirani': {
            wdm: 'Inficon_Pirani',
            'Systems': systems,
        },

        # cold cathode
        'collab_press_cathode': {
            wdm: 'Inficon_ColdCathode',
            'Systems': systems,
        },

        # control
        'collab_press_control': {
            wdm: 'Inficon_ColdCathode',
            'Systems': systems,
        },

        # Feedthrough
        # 'feedthrough': {
        #     'model': 'Feed_EIGER_2S_500K',
        #     'Systems': systems,
        # },

        # ----------
        # Gate Valve

        # main
        'collab_gate': {
            wdm: 'AllMetal_DN63CF',
            'Systems': systems,
        },

        # pressure
        'collab_gate': {
            wdm: 'AllMetal_DN40CF',
            'Systems': systems,
        },

        # --------
        # Solenoid

        # --------
        # PLC

        # Power supply
        'collab_PLC_PS': {
            wdm: 'PLC_PS',
            'Systems': systems,
        },

        # CPU
        'collab_PLC_CPU': {
            wdm: 'PLC_CPU',
            'Systems': systems,
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

    systems = ('DIAG', 'XRAY', 'HXR-TS')

    # -----------
    # update
    # -----------

    dout.update({

        # ----------------
        # scintillators

        'hxr_scintillator_north': {
            wdm: 'HXR_scintillator',
            'Systems': systems,
        },

        'hxr_scintillator_south': {
            wdm: 'HXR_scintillator',
            'Systems': systems,
        },

        # ------------------
        # HV power supply

        'hxr_power_HV': {
            wdm: 'HXR_power_HV',
            'Systems': systems,
        },

        # -----------------
        # HXR digitizers

        'hxr_digitizer_fast': {
            wdm: 'HXR_digitizer_fast',
            'Systems': systems,
        },

        'hxr_digitizer_current': {
            wdm: 'DIAG_FC',
            'Systems': systems,
        },

        # -----------------
        # HXR LED

        'hxr_LED_north': {
            wdm: 'HXR_LED',
            'Systems': systems,
        },

        'hxr_LED_south': {
            wdm: 'HXR_LED',
            'Systems': systems,
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

    systems = ('DIAG', 'XRAY', 'XRB')

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
                'Systems': systems,
            }

        # ------------
        # bellows

        for jj, gv in enumerate(('AllMetal_DN100CF', 'AllMetal_DN63CF', 'UHV_DN100CF')):
            key = f"{keyb}_Bellow{jj}"
            dout[key] = {
                wdm: gv,
                'Systems': systems,
            }

        # ---------------
        # pressure gauges

        for jj in range(3):

            for gv in ('Inficon_Pirani', 'Inficon_ColdCathode'):
                key = f"{keyb}_Press_{gv}{jj}"
                dout[key] = {
                    wdm: gv,
                    'Systems': systems,
                }

            # check valve
            key = f"{keyb}_GAS_check{jj}"
            dout[key] = {
                wdm: 'check_valve',
                'Systems': systems,
            }

            # gate valve
            key = f"{keyb}_GAS_GV"
            dout[key] = {
                wdm: 'AllMetal_DN40CF',
                'Systems': systems,
            }

    # ----------------------
    # pressure control unit

    for ii in range(8):

        key = f"{keyb}_Press_control{jj}"
        dout[key] = {
            wdm: 'Inficon_Control',
            'Systems': systems,
        }

    # -----------------
    # Vertical manifold

    dout[f'xrb_manifold_GV'] = {
        wdm: 'UHV_DN100CF',
        'Systems': systems,
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