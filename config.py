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

_TICKERS = {'^XSP': 'United States',
            '^GSPC': 'United States'}
_MAPPING = {'United States': _BOND_US}

# other constants
_YEAR = 365 # number of days in a year 

