#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:49:05 2020

@authors: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
# import third-party libraries
# import local libraries

# base url to get options
_BASE_URL = 'https://query1.finance.yahoo.com'

# url links to bonds of each zone
_BOND_US = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/textview.aspx?data=yield'
_BOND_EU = 'https://ycharts.com/indicators/reports/euro_yield_curves'
_TICKERS = {'^GSPC': 'United States',
            'FEZ': 'Europe',
            }
_MAPPING = {'United States': _BOND_US,
            'Europe': _BOND_EU}

# constants for html objects
_DROPDOWN = [{'label': k, 'value': k} for k in _TICKERS.keys()]

# other constants
_YEAR = 252 # number of business days in a year 
_DEBUG = False

# PORT 
PORT = 8050


