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

    dout = {
        'sensor': {
            'description': 'device mostly used for sensing',
        },
        'actuator': {
            'description': 'device mostly used for controlled actions',
        },
        'digitizer': {
            'description': 'digitizer',
        },
        'amplifier': {
            'description': 'transimpedance amplifier',
        },
        'PLC': {
            'description': 'part of a PLC controller',
        },
        'controller': {
            'description': 'vendor-specific controller for sensors',
        },
        'server': {
            'description': 'server or computer',
        },
        'solenoid': {
            'description': 'solenoid valve',
        },
        'power': {
            'description': 'power source for another device',
        },
        'mechanical': {
            'description': 'mechanical parts',
        },
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