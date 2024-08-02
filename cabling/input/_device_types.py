# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:24:57 2024

@author: dvezinet
"""


import os


from . import _save2json


#############################################
#############################################
#        DEFAULTS
#############################################

print(__file__)


#############################################
#############################################
#    Connection types
#############################################


def get(path=None):

    dout = {}

    # -------------
    # CVD diamonds cameras
    # -------------

    dout['CVD'] = {
        'description': 'CVD diamond sensor',
        'connections': {
            'all': {
                'type': "beaded_pair",
                'nb': 1,
            },
        },
    }

    dout['CVD_MI'] = {
        'description': 'CVD cameras MI adapter plate',
        'connections': {
            'all': {
                'type': "MI_Term",
                'nb': 30,
            },
        },
    }


    # ---------------
    # save to json
    # ---------------

    which = os.path.split(__file__)[-1][1:-3]
    print(which)
    return _save2json.main(pat=path, dout=dout, which=which)


#############################################
#############################################
#    __main__
#############################################


if __name__ == '__main__':
    get()