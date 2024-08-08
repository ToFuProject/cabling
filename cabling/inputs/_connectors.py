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
#    utility
#############################################


def keysys(systems):
    lk = sorted(systems.keys())
    return '_'.join([systems[kk] for kk in lk])


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
            }

            # plate to camera
            dout[f'{keyS}_wire_{ii}'] = {
                wcm: 'wire_pair',
                'label': f'wire_{ii:02.0f}',
                'systems': systems,
                'ptA': (key_plate, f'out_{ii}'),
                'ptB': (key_cam, f'CVD_in_{ii}'),
            }

            # camera to feedthrough
            dout[f'sxr_{pp}_MI_{ii}'] = {
                wcm: 'MI_twist_pair',
                'label': f'MI_{ii:02.0f}',
                'systems': systems,
                'ptA': (key_cam, f'CVD_out_{ii}'),
                'ptB': (key_feed, f'CVD_in_{ii}'),
            }

        # ---------------------------------
        # individual thermocouple to camera

        dout[f'{keyS}_therm_MI'] = {
            wcm: 'MI_single',
            'label': f'therm_MI_{ii:02.0f}',
            'systems': systems,
            'ptA': (f'{keyS}_therm', 'all'),
            'ptB': (key_cam, 'Therm_in'),
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