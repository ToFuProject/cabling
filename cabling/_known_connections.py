# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:24:57 2024

@author: dvezinet
"""

#############################################
#############################################
#    Connection types
#############################################


def get():

    return {

        # -------------
        # cables - HXR
        # -------------

        'BNC_50H_M': {
            'description': 'Male 50 Ohms BNC',
            'specs': '',
            'url': (
                'https://en.wikipedia.org/wiki/BNC_connector',
            ),
        },

        'BNC_50H_F': {
            'description': 'Female 50 Ohms BNC',
            'specs': '',
            'url': (
                'https://en.wikipedia.org/wiki/BNC_connector',
            ),
        },

        'BNC_75H_M': {
            'description': 'Male 75 Ohms BNC',
            'specs': '',
            'url': (
                'https://en.wikipedia.org/wiki/BNC_connector',
            ),
        },

        'BNC_75H_F': {
            'description': 'Female 75 Ohms BNC',
            'specs': '',
            'url': (
                'https://en.wikipedia.org/wiki/BNC_connector',
            ),
        },

        'SHV': {
            'description': '',
            'specs': '',
            'url': (
                'https://en.wikipedia.org/wiki/SHV_connector',
            ),
        },

        'BNC': {
            'description': '',
            'specs': '',
        },

        # -------------
        # cables - DECTRIS
        # -------------

        # MI termination
        'MI_Term': {
            'description': 'Termination for MI cables',
        },

        # DECTRIS external trigger
        'DECTRIS_ext': {
            'description': ' Lemo® Type 00 (NIM/CAMAC) ',
            'url': 'https://media.dectris.com/220921-Technical-specifications-DECTRIS_EIGER2_S_500K-RW.pdf',
        },

        # DECTRIS power
        'DECTRIS_pow': {
            'descrption': 'IEC-320-C14 input inlet',
            'specs': '12 VDC, max. 11.5 A, 138 W (60 W needed)',
        },

        # -------------
        # optics fiber
        # -------------

        # SFP+ optics fiber
        'SFP+': {
            'description': '10 GbE-LR single mode SFP+',
            'specs': 'LC/UPC duplex',
            'url': (
                'https://media.dectris.com/220921-Technical-specifications-DECTRIS_EIGER2_S_500K-RW.pdf',
                'https://en.wikipedia.org/wiki/Small_Form-factor_Pluggable',
            ),
        },

        # -------------
        # tubes
        # -------------

        # SFP+ optics fiber
        'DECTRIS_cool': {
            'description': 'cooling pipes connections for DECTRIS cameras',
            'specs': '1/8 inch ISO parallel thread',
        },
    }