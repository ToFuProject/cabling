# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 11:04:35 2024

@author: dvezinet
"""


import os


from . import _save2json


#############################################
#############################################
#    Plug options
#############################################


def get(path=None):

    # ---------------------
    # CVD diamonds cameras
    # ---------------------

    dout = {
        'M/F': {
            'description': 'male or female',
            'values': ['M', 'F'],
        },
        'impedance': {
            'description': 'impedance [Ohms]',
            'values': 'float',
        },
    }

    # ---------------
    # save to json
    # ---------------

    which = os.path.split(__file__)[-1][1:-3]
    print()
    print(which)
    print(dout)
    return _save2json.main(path=path, dout=dout, which=which)