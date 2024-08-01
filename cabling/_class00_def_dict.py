# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:41:53 2024

@author: dvezinet
"""

#############################################
#############################################
#       DEFAULT KWDARGS for Connectors types
#############################################


def get_connection_type_kwdargs():

    return {
        'description': {
            'def': '',
            'types': str,
        },
        'specs': {
            'def': '',
            'types': str,
        },
        'ref': {
            'def': '',
            'types': str,
        },
        'url': {
            'def': '',
            'types': (str, tuple),
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
            'def': '',
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
            'def': '',
            'types': str,
        },
        'cost': {
            'types': (int, float),
            'astype': float,
        },
        'url': {
            'types': str,
            'astype': str,
        },
        'type': {
            'types': str,
            'can_be_None': False,
            'which': 'connector_type',
        },
    }


#############################################
#############################################
#       DEFAULT KWDARGS for Connectors
#############################################


def get_connector_kwdargs():

    return {
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
            'def': '',
            'types': str,
            'unique': False,
        },
        'length': {
            'types': (int, float),
            'astype': float,
        },
        'System': {
            'types': (str, list, tuple),
            'astype': tuple,
        },
        'due_date': {
            'types': str,
            'astype': str,
        },
        'contact': {
            'types': str,
            'astype': str,
        },
        'model': {
            'types': str,
            'can_be_None': False,
            'which': ('connector_model', 'connector_type'),
        },
    }