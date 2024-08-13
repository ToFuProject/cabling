# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:24:57 2024

@author: dvezinet
"""


import os


from . import _config
from . import _save2json


#############################################
#############################################
#    utility
#############################################


def keysys(systems, systems_key=_config._SYSTEMS_KEY):
    lk = sorted(systems.keys())
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
    wcm = 'connector_model'

    systems0 = {'L1': 'DIAG', 'L2': 'XRAY'}

    # ------------------
    # in vessel SXR
    # ------------------

    _invessel_SXR(dout, wcm, systems0)

    # ------------------
    # HXR scintillators
    # ------------------

    _exvessel_HXR_scintillators(dout, wcm, systems0)

    # ---------------
    # add labels if needed
    # ---------------

    for k0, v0 in dout.items():
        dout[k0]['label'] = v0.get('label', k0)

    # ---------------
    # save to json
    # ---------------

    which = os.path.split(__file__)[-1][1:-3]
    return _save2json.main(path=path, dout=dout, which=which)


#############################################
#############################################
#         in-vessel SXR
#############################################


def _invessel_SXR(dout, wcm, systems0):

    # -------------
    # system
    # -------------

    systems0 = dict(systems0, L3='SXRVA')

    # -----------
    # update
    # -----------

    npix = 15
    lcam = ['OMPu', 'OMPl', 'MPPu', 'MPPl']

    sysAcq = dict(systems0, L4='ACQ')
    keySacq = keysys(sysAcq)

    preamp_nb, breakout_nb = 0, 0
    ind_preamp, ind_breakout = 0, 0
    ind_twist2 = 0

    for pp in lcam:

        systems = dict(systems0, L4=pp)
        keyS = keysys(systems)

        key_plate = f'{keyS}_plate'
        key_cam = f'{keyS}_cam'
        key_feed = f'{keyS}_feed'

        # individual sensors to plate
        for ii in range(npix):

            dout[f"{keyS}_microwire_{ii:02.0f}"] = {
                wcm: 'microwire_pair',
                'label': f'microwire_{ii:02.0f}',
                'systems': systems,
                'ptA':(f"{keyS}_CVD_{ii:02.0f}", 'all'),
                'ptB': (key_plate, f'in_{ii}'),
                'typ. signal': '< mA, < 5 V',
            }

            # plate to camera
            dout[f'{keyS}_wire_{ii}'] = {
                wcm: 'wire_pair',
                'label': f'wire_{ii:02.0f}',
                'systems': systems,
                'ptA': (key_plate, f'out_{ii}'),
                'ptB': (key_cam, f'CVD_in_{ii}'),
                'typ. signal': '< mA, < 5 V',
            }

            # camera to feedthrough
            dout[f'{keyS}_MI_{ii}'] = {
                wcm: 'MI_twist_pair',
                'label': f'MI_{ii:02.0f}',
                'systems': systems,
                'ptA': (key_cam, f'CVD_out_{ii}'),
                'ptB': (key_feed, f'CVD_in_{ii}'),
                'typ. signal': '< mA, < 5 V',
            }

            # feedthrough to preamplifier
            key_preamp = f"{keySacq}_preamp_{preamp_nb:02.0f}"
            dout[f'{keyS}_twist_{ii}'] = {
                wcm: 'twist_pair',
                'label': f'twist_{ii:02.0f}',
                'systems': systems,
                'ptA': (key_feed, f'CVD_out_{ii}'),
                'ptB': (key_preamp, f'in_{ind_preamp}'),
                'typ. signal': '< mA, < 5 V',
            }

            # preamplifier to breakout board
            key_break = f"{keySacq}_breakout_{breakout_nb:02.0f}"
            dout[f'{keyS}_twist2_{preamp_nb}_{ind_preamp}'] = {
                wcm: 'twist_pair',
                'label': f'twist2_{preamp_nb}_{ind_preamp}',
                'systems': sysAcq,
                'ptA': (key_preamp, f'out_{ind_preamp}'),
                'ptB': (key_break, f'in_{ind_breakout}'),
                'typ. signal': '< mA, < 5 V',
            }

            # increment
            if ind_preamp == 3:
                ind_preamp = 0
                preamp_nb += 1
            else:
                ind_preamp += 1
            if ind_breakout == 31:
                ind_breakout = 0
                breakout_nb += 1
            else:
                ind_breakout += 1

        # ---------------------------------
        # individual thermocouple to camera

        dout[f'{keyS}_therm_MI'] = {
            wcm: 'MI_single',
            'label': f'therm_MI_{ii:02.0f}',
            'systems': systems,
            'ptA': (f'{keyS}_therm', 'all'),
            'ptB': (key_cam, 'Therm_in'),
            'typ. signal': '?',
        }

    # ---------------------
    # digitizer cables
    # ---------------------

    # breakout to digitizer
    for ii in range(breakout_nb+1):
        key_break = f"{keySacq}_breakout_{ii:02.0f}"
        key = f"{keySacq}_digit_{ii:02.0f}"
        dout[key] = {
            wcm: 'VHCDI',
            'label': f'digit_{ii:02.0f}',
            'systems': sysAcq,
            'ptA': (key_break, 'out'),
            'ptB': (f'{keySacq}_digit_{0:02.0f}', f'in_{ii}'),
        }

    return


#############################################
#############################################
#         ex-vessel SXR scintillators
#############################################


def _exvessel_HXR_scintillators(dout, wcm, systems0):

    # -------------
    # system
    # -------------

    systems0 = dict(systems0, L3='HXRTS')

    # -----------
    # update
    # -----------

    # -----------
    # update
    # -----------

    for ii, ss in enumerate(['North', 'South']):

        systems = dict(systems0, L4=ss)
        keyS = keysys(systems)

        dout[f"{keyS}_HV"] = {
            wcm: 'SHV',
            'label': f'HV',
            'systems': systems,
            'ptA':(f"{keyS}_scintillator", 'power'),
            'ptB': (f"{keyS}_power", f'out_{ii}'),
            'typ. signal': '0.1-1 kV',
        }

    return


#############################################
#############################################
#    __main__
#############################################


if __name__ == '__main__':
    get()