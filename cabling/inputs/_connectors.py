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

    # ------------------
    # in vessel SXR
    # ------------------

    _invessel_SXR(dout, wcm)

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


def _invessel_SXR(dout, wcm):

    # -------------
    # system
    # -------------

    systems0 = {'L1': 'DIAG', 'L2': 'XRAY', 'L3': 'SXRVA'}

    # -----------
    # update
    # -----------

    npix = 15
    lcam = ['OMPu', 'OMPl', 'MPPu', 'MPPl']

    preamp_nb = 0
    ind_preamp = 0
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
            key_preamp = f"{keyS}_preamp_{preamp_nb:02.0f}"
            dout[f'{keyS}_twist_{ii}'] = {
                wcm: 'MI_twist_pair',
                'label': f'MI_{ii:02.0f}',
                'systems': systems,
                'ptA': (key_feed, f'CVD_in_{ii}'),
                'ptB': (key_preamp, f'input_{ind_preamp}'),
                'typ. signal': '< mA, < 5 V',
            }
            if ind_preamp == 3:
                ind_preamp = 0
                preamp_nb += 1
            else:
                ind_preamp += 1

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
        # preamplifiers cables
        # ---------------------

        # namp = int(np.ceil(npix / 4))

        # for ii in range(namp):

        #     for jj in range(4):

        #         # camera to preamplifier
        #         dout[f''] = {
        #             wcm: 'CVD_Therm',
        #             'systems': systems,
        #             'ptA': (key_feed, 'CVD_out_{ii*4+jj}'),
        #             'ptB': (f'sxr_{pp}_preamp_{ii}', 'in_{jj}'),
        #         }

    # ---------------------
    # digitizer cables
    # ---------------------

    # preamplifier to digitizer
    # key = f'sxr_{pp}_therm'
    # dout[key] = {
    #     wcm: 'CVD_preamp_digit',
    #     'systems': systems,
    #     'ptA': (key_pream, 'out'),
    #     'ptB': (key_digitizer, 'in'),
    # }

    return


#############################################
#############################################
#    __main__
#############################################


if __name__ == '__main__':
    get()