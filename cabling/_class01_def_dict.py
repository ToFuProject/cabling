# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:41:53 2024

@author: dvezinet
"""


#############################################
#############################################
#         Device_type kwdargs
#############################################


def get_device_type_kwdargs():

    return {
        'description': {
            'types': str,
        },
        'url': {
            'types': (str, tuple, list),
            'astype': tuple,
        },
    }


#############################################
#############################################
#       DEFAULT KWDARGS for Connectors models
#############################################


def get_device_model_kwdargs():

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
            'types': (str, tuple, list),
            'astype': tuple,
        },
        'device_type': {
            'types': str,
            'can_be_None': False,
            'which': 'device_type',
        },
    }


#############################################
#############################################
#       DEFAULT KWDARGS for Connectors
#############################################


def get_device_kwdargs():

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
        'Systems': {
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
        'device_model': {
            'types': str,
            'can_be_None': False,
            'which': 'device_model',
        },
    }