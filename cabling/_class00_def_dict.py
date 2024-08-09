# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:41:53 2024

@author: dvezinet
"""

#############################################
#############################################
#       DEFAULT KWDARGS for Connectors types
#############################################


def get_plug_type_kwdargs():

    return {
        'description': {
            'types': str,
        },
        'specs': {
            'types': str,
        },
        'ref': {
            'types': str,
        },
        'url': {
            'types': (str, tuple, list),
            'astype': tuple,
        },
    }


#############################################
#############################################
#       DEFAULT KWDARGS for Connectors types
#############################################


def get_connector_type_kwdargs():

    return {
        'description': {
            'types': str,
        },
    }


#############################################
#############################################
#       DEFAULT KWDARGS for Connectors models
#############################################


def get_connector_model_kwdargs():

    return {
        'PN': {
            'types': (int, str),
            'astype': str,
            'unique_all': True,
            # 'can_be_None': False,
        },
        'PN_vendor': {
            'types': (int, str),
            'astype': str,
            'unique_all': True,
        },
        'description': {
            'types': str,
        },
        'cost': {
            'types': (int, float),
            'astype': float,
        },
        'url': {
            'types': (str, tuple, list),
            'astype': tuple,
        },
        'connector_type': {
            'types': str,
            # 'can_be_None': False,
            'which': 'connector_type',
        },
    }


#############################################
#############################################
#       DEFAULT KWDARGS for Connectors
#############################################


def get_connector_kwdargs():

    return {
        'typ. signal': {
            'types': str,
            'astype': str,
        },
        'tag': {
            'types': (int, str),
            'astype': str,
            'unique_all': True,
        },
        'PID': {
            'types': (int, str),
            'astype': str,
        },
        'comments': {
            'types': str,
            'unique': False,
        },
        'length': {
            'types': (int, float),
            'astype': float,
        },
        'due_date': {
            'types': str,
            'astype': str,
        },
        'contact': {
            'types': str,
            'astype': str,
        },
        'connector_model': {
            'types': str,
            # 'can_be_None': False,
            'which': 'connector_model',
        },
    }