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
    wcm = 'connector_model'

    # ------------------
    # in vessel SXR
    # ------------------

    _invessel_SXR(dout, wcm)

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

    systems = {'L1': 'DIAG', 'L2': 'XRAY', 'L3': 'SXR-VA'}

    # -----------
    # update
    # -----------

    npix = 15
    lcam = ['OMPu', 'OMPl', 'MPPu', 'MPPl']

    for pp in lcam:

        key_plate = f'sxr_{pp}_plate'
        key_cam = f'sxr_{pp}_cam'
        key_feed = f'sxr_{pp}_feed'

        # individual sensors to plate
        for ii in range(npix):

            dout[f"sxr_{pp}_microwire_{ii}"] = {
                wcm: 'microwire_pair',
                'systems': systems,
                'ptA':(f"sxr_{pp}_CVD_{ii}", 'all'),
                'ptB': (key_plate, f'in_{ii}'),
            }

            # plate to camera
            dout[f'sxr_{pp}_wire_{ii}'] = {
                wcm: 'wire_pair',
                'systems': systems,
                'ptA': (key_plate, f'out_{ii}'),
                'ptB': (key_cam, f'CVD_in_{ii}'),
            }

            # camera to feedthrough
            dout[f'sxr_{pp}_MI_{ii}'] = {
                wcm: 'MI_twist_pair',
                'systems': systems,
                'ptA': (key_cam, f'CVD_out_{ii}'),
                'ptB': (key_feed, f'CVD_in_{ii}'),
            }

        # ---------------------------------
        # individual thermocouple to camera

        dout[f'sxr_{pp}_therm_MI'] = {
            wcm: 'MI_single',
            'systems': systems,
            'ptA': (f'sxr_{pp}_therm', 'all'),
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