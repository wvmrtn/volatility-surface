#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:49:05 2020

@authors: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
import requests
# import third-party libraries
import pandas as pd
# import local libraries
from config import _MAPPING, _TICKERS

def _downloadBonds(ticker):
    """Download bonds depending on ticker symbol.

    Parameters
    ----------
    ticker : string
        Ticker symbol of index.

    Returns
    -------
    bonds : pandas.Series
        pandas.Series with list of yields (name: yield).
        Keys are in days. 

    """
    assert ticker in _TICKERS, 'Ticker not valid.'
    
    area = _TICKERS[ticker] 
    bonds = pd.Series(float)
    
    if area == 'United States':
        # transform US bonds
        url = _MAPPING[area]
        html =requests.get(url).content 
        bonds = pd.read_html(html)[1]
        bonds = bonds.drop(columns = 'Date')
        # rename columns
        columns = bonds.columns
        columns = [s.split(' ') for s in columns]
        columns_days = []
        for c in columns:
            if c[1] == 'mo':
                days = 30
            elif c[1] == 'yr':
                days = 365
            else:
                days = 0
            columns_days.append(float(c[0])*days)
        bonds.columns = columns_days
        bonds = bonds.iloc[-1]
        bonds = bonds.rename('yield')
        bonds /= 100 # from percentage to float
        
    elif area == '':
        pass
    
    else:
        pass
    
    return bonds

if __name__ == '__main__':
    
    bonds = downloadBonds('^XSP')
