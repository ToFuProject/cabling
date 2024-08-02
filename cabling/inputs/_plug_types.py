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
    # BNC
    # -------------

    for imp in ['50Hz', '75Hz']:
        for mf in ['M', 'F']:
            key = f"BNC_{imp}_{mf}"
            dout[key] = {
                'description': f'{mf} BNC'
            }

    # -------------
    # SHV
    # -------------

    for mf in ['M', 'F']:
        key = f"SHV_{''.join(mf)}"
        dout[key] = {
            'description': f'{mf} Safe High Voltage'
        }

    # -------------
    # in-vessel
    # -------------

    dout.update({
        # MI termination
        'MI_Term': {
            'description': 'Termination for MI cables',
        },

        # wire-bonding
        'wire_bond': {
            'description': 'micro-wires bonded with ultrasounds',
        },
    })

    # -------------
    # cables - DECTRIS
    # -------------

    dout.update({
        # DECTRIS external trigger
        'Lemo® Type 00': {
            'description': ' Lemo® Type 00 (NIM/CAMAC) ',
            'url': 'https://media.dectris.com/220921-Technical-specifications-DECTRIS_EIGER2_S_500K-RW.pdf',
        },

        # DECTRIS power
        'DECTRIS_pow_AC': {
            'description': 'IEC-320-C14 input inlet',
            'specs': '',
        },

        # DECTRIS power
        'DECTRIS_pow_DC': {
            'description': 'round plug',
            'specs': '12 VDC, max. 11.5 A, 138 W (60 W needed)',
        },
    })

    # -------------
    # optics fiber
    # -------------

    dout.update({
        # SFP+ optics fiber
        'SFP+': {
            'description': '10 GbE-LR single mode SFP+',
            'specs': 'LC/UPC duplex',
            'url': (
                'https://media.dectris.com/220921-Technical-specifications-DECTRIS_EIGER2_S_500K-RW.pdf',
                'https://en.wikipedia.org/wiki/Small_Form-factor_Pluggable',
            ),
        },
    })

    # -------------
    # RJ45
    # -------------

    dout.update({
        # RJ45 ethernet
        'RJ45_F': {
            'description': 'standard ethernet RJ45, female',
            'specs': '',
            'url': (

            ),
        },
        'RJ45_M': {
            'description': 'standard ethernet RJ45, male',
            'specs': '',
            'url': (

            ),
        },
    })

    # -------------
    # tubes
    # -------------

    dout.update({
    # SFP+ optics fiber
        'DECTRIS_cool': {
            'description': 'cooling pipes connections for DECTRIS cameras',
            'specs': '1/8 inch ISO parallel thread',
        },
    })

    # ----------------------
    #  standard power chord
    # -----------------------

    dout.update({
        'power_AC_US_F': {
            'description': 'standard US AC detachable power chord, female',
            'specs': 'NEMA 5-15P, IEC 60320 C-13',
            'url': (
                'https://internationalconfig.com/power-cords-for-united-states-ac-power-cords.asp',
            ),
        },
        'power_AC_US_M': {
            'description': 'standard US AC detachable power chord, male',
            'specs': 'NEMA 5-15P, IEC 60320 C-13',
            'url': (
                'https://internationalconfig.com/power-cords-for-united-states-ac-power-cords.asp',
            ),
        },
        'US_A_F': {
            'description': 'standard US socket, ungrounded, female',
            'specs': '2 pins, not grounded, female',
            'url': (
                'https://www.worldstandards.eu/electricity/plugs-and-sockets/',
            ),
        },
        'US_A_M': {
            'description': 'standard US socket, male',
            'specs': '2 pins, not grounded, ungrounded, male',
            'url': (
                'https://www.worldstandards.eu/electricity/plugs-and-sockets/',
            ),
        },
        'US_B_F': {
            'description': 'standard US socket, grounded, female',
            'specs': '3 pins, grounded, female',
            'url': (
                'https://www.worldstandards.eu/electricity/plugs-and-sockets/',
            ),
        },
        'US_B_M': {
            'description': 'standard US socket, grounded, male',
            'specs': '3 pins, grounded, male',
            'url': (
                'https://www.worldstandards.eu/electricity/plugs-and-sockets/',
            ),
        },
    })


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