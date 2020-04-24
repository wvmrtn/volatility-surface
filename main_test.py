#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 12:06:37 2020

@authors: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
# import third-party libraries
# import local libraries
from yahoo_requests import Market
from bond_requests import downloadBonds
from implied_vol_functions import implied_vol

if __name__ == '__main__':
    
    # download options of index
    ticker  = '^XSP'
    div_yield = 0.0231
    sp500 =  Market(ticker, div_yield)
    options = sp500.downloadAllOptions()
    
    # download bonds
    bonds = downloadBonds(ticker)
    
    
    
