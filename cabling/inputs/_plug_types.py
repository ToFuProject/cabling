# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:24:57 2024

@author: dvezinet
"""


import os


from . import _save2json


#############################################
#############################################
#    Plug types
#############################################


def get(path=None):

    dout = {}

    # -------------
    # generic
    # -------------

    dout['generic'] = {
        'description': 'generic, accomodates everything',
    }

    # -------------
    # BNC
    # -------------

    dout['BNC'] = {
        'description': 'BNC plug',
        'url': 'https://en.wikipedia.org/wiki/BNC_connector',
    }

    # -------------
    # SHV
    # -------------

    dout['SHV'] = {
        'description': 'Safe High Voltage',
    }

    # -------------
    # in-vessel
    # -------------

    dout.update({
        # MI termination
        'MI_Term': {
            'description': 'Termination for MI cables',
        },

        'MI_Term_pair': {
            'description': 'Termination for a pair of MI cables',
        },

        # wire-bonding
        'wire_bond_pair': {
            'description': 'micro-wires bonded with ultrasounds',
        },

        # wire-bonding
        'twist_pair': {
            'description': 'standard twisted pair',
        },
    })

    # ------------------
    # cables HXR
    # -------------------

    dout.update({
        'MCX': {
            'description': 'micro coaxial connector, CECC 22220',
            'url': (
                'https://en.wikipedia.org/wiki/MCX_connector',
            ),
        },
        'SMA': {
            'description': 'SubMiniature version A coaxial connector',
            'url': (
                'https://en.wikipedia.org/wiki/SMA_connector',
            ),
        },
    })

    # -------------
    # Lemo
    # -------------

    dout['Lemo00'] = {
        'description': ' Lemo® Type 00 (NIM/CAMAC), male ',
        'url': 'https://www.lemo.com/int_en/solutions/specialties/00-nim-camac.html',
    }

    # -------------
    # cables - DECTRIS
    # -------------

    dout.update({
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

        # bare optic fiber, for light
        'optical': {
            'description': 'light coming out of a fiber',
            'specs': '',
            'url': (
            ),
        },
    })

    # -------------
    # RJ45
    # -------------

    dout.update({
        # RJ45 ethernet
        'RJ45': {
            'description': 'standard ethernet RJ45',
            'specs': '',
            'url': (
            ),
        },
    })

    # ----------------------
    # compact cable bundles
    # ----------------------

    dout.update({
        'VHCDI': {
            'description': '68-pin connectors, Shielded, twisted pair wiring',
            'specs': '',
            'url': (
                'https://www.winford.com/products/cbvh68.php',
            ),
        },
    })

    # -------------
    # serial
    # -------------

    dout.update({

        # RS-232
        'RS232': {
            'description': 'Differential, common ground, 5V, up to 20 kb/s',
            'specs': '',
            'url': (
                'https://en.wikipedia.org/wiki/RS-232#:~:text=In%20telecommunications%2C%20RS%2D232%20or,serial%20communication%20transmission%20of%20data.',
            ),
        },

        # RS-422
        'RS422': {
            'description': 'Differential, return per cable, 0.4 V, up to 10 Mb/s at 1200 m',
            'specs': '',
            'url': (
                'https://en.wikipedia.org/wiki/RS-422',
            ),
        },

        # RS-485
        'RS485': {
            'description': 'Differential, return per cable, 0.4 V, up to 10 Mb/s at 1200 m',
            'specs': '',
            'url': (
                'https://en.wikipedia.org/wiki/RS-485',
            ),
        },
    })


    # -------------
    # USB
    # -------------

    dout.update({
        # RJ45 ethernet
        'usb_c': {
            'description': 'USB-C',
            'specs': '',
            'url': (
            ),
        },
    })

    # -------------
    # plugables
    # -------------

    dout.update({
        'MemCard': {
            'description': 'Memory card',
        },
    })

    # -------------
    # tubes
    # -------------

    dout.update({
        'DECTRIS_cool': {
            'description': 'cooling pipes connections for DECTRIS cameras',
            'specs': '1/8 inch ISO parallel thread',
        },
    })

    # ----------------------
    #  standard power chord
    # -----------------------

    dout.update({
        '1phase_AC_US': {
            'description': 'standard US cable with (phase, neutrral, ground)',
            'specs': '120/230 V, 50/60 Hz',
            'url': (
                'https://internationalconfig.com/power-cords-for-united-states-ac-power-cords.asp',
            ),
        },
        'power_AC_US': {
            'description': 'standard US AC detachable power chord',
            'specs': 'NEMA 5-15P, IEC 60320 C-13',
            'url': (
                'https://internationalconfig.com/power-cords-for-united-states-ac-power-cords.asp',
            ),
        },
        'US_A': {
            'description': 'standard US socket, ungrounded',
            'specs': '2 pins, not grounded',
            'url': (
                'https://www.worldstandards.eu/electricity/plugs-and-sockets/',
            ),
        },
        'US_B': {
            'description': 'standard US socket, grounded',
            'specs': '3 pins, grounded',
            'url': (
                'https://www.worldstandards.eu/electricity/plugs-and-sockets/',
            ),
        },
        'wire_pair_LV': {
            'description': 'standard Low-voltage pair of wires',
            'specs': '',
            'url': (
                '',
            ),
        },
        'power_bus_24V': {
            'description': 'standard 24 V power supply bus used by PLCs',
        },
    })

    # --------------
    # vendor-specific
    # --------------

    dout.update({
        'InficonPirani': {
            'description': "Single cable bundle for Inficon's Pirani gauges",
        },
        'InficonColdCath': {
            'description': "Single cable bundle for Inficon's Cold Cahtode gauges",
        },
        '8070-2530-02Z16-6PA': {
            'description': 'Glenair circular hermetic connector, used on VAT valves'
        },
        '8070-3039-01Z16-6KA': {
            'description': 'Glenair circular hermetic connector, used on VAT valves'
        },
        'VAT_position': {
            'description': '7 pins round cable connection used on VAT valves',
        },
    })

    # --------------
    # piping - vacuum
    # --------------

    dout.update({
        'DN100CF': {
            'description': 'DN100CF',
        },
        'DN63CF': {
            'description': 'DN63CF',
        },
        'DN40CF': {
            'description': 'DN40CF',
        },
    })

    # --------------
    # piping - fittings
    # --------------

    dout.update({
        'ISO_1/8': {
            'description': 'Connector for VAT valves air feeds',
            'specs': '1/8" ISO NPT',
        },
        'VCR_1/4': {
            'description': 'VCR fitting for 1/4" piping',
            'specs': '',
        },
    })


    # -------------
    # mechanical
    # -------------

    dout.update({
        # Mounting rail
        'rail': {
            'description': 'mounting rail in a rack',
            'specs': '',
        },
    })

    # ---------------
    # Common options
    # ---------------

    _common_options(dout)

    # ---------------
    # save to json
    # ---------------

    which = os.path.split(__file__)[-1][1:-3]
    return _save2json.main(path=path, dout=dout, which=which)


#############################################
#############################################
#      Common options
#############################################


def _common_options(dout):

    wpo = 'plug_option'

    # -------------
    # plug types
    # -------------

    lptype = [
        'RS232', 'RS422', 'RS485',
        'BNC', 'SHV',
        'Lemo00',
        'VHCDI',
        'usb_c',
        'RJ45',
        'MemCard',
        'power_AC_US', 'US_A', 'US_B',
        'VCR_1/4', 'ISO_1/8',
    ]

    # ------------
    # Common
    # -------------

    dcommon = {
        'M/F': lptype,
    }

    # ------------
    # Implement
    # -------------

    # for kopt, lk in dcommon.items():

    #     for ktype in lk:
    #         if dout[ktype].get('doptions') is None:
    #             dout[ktype]['doptions'] = {}
    #         dout[ktype]['doptions'][kopt]

    return


#############################################
#############################################
#    __main__
#############################################


if __name__ == '__main__':
    get()