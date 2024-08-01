# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:41:53 2024

@author: dvezinet
"""


#############################################
#############################################
#       DEFAULT KWDARGS for Connectors
#############################################


def get_def():

    return {
        'tag': {
            'def': None,
            'types': (int, str),
            'astype': str,
            'unique': True,
            'can_be_None': False,
        },
        'PID': {
            'def': None,
            'types': (int, str),
            'astype': str,
            'unique': False,
            'can_be_None': True,
        },
        'PN': {
            'def': None,
            'types': (int, str),
            'astype': str,
            'unique': True,
            'can_be_None': False,
        },
        'PN_vendor': {
            'def': None,
            'types': (int, str),
            'astype': str,
            'unique': False,
            'can_be_None': True,
        },
        'prov_with': {
            'def': '',
            'types': str,
            'unique': False,
            'can_be_None': True,
        },
        'comments': {
            'def': '',
            'types': str,
            'unique': False,
            'can_be_None': True,
        },
        'cost': {
            'def': None,
            'types': (int, float),
            'unique': False,
            'can_be_None': True,
        },
        'due_date': {
            'def': None,
            'types': str,
            'astype': str,
            'unique': False,
            'can_be_None': True,
        },
        'contact': {
            'def': None,
            'types': str,
            'astype': str,
            'unique': False,
            'can_be_None': True,
        },
    }