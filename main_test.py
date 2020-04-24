#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 12:06:37 2020

@authors: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
# import third-party libraries
# import local libraries
from yahoo_requests import Index
from implied_vol_functions import implied_vol

if __name__ == '__main__':
    
    # download options of index
    ticker  = '^XSP'
    delta = 0.0231
    sp500 = Index(ticker, delta)
    sp500.downloadAllOptions()
    sp500.downloadBonds()
    options = sp500.options
    
    # compute implied volatility
    result = implied_vol(options, sigma_0 = 0.01, error = 0.01)
    
    
    
