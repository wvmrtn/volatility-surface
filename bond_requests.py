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
        pandas.Series with list of yields (name: rate).
        Keys are in years. 

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
        columns_years = []
        for c in columns:
            if c[1] == 'mo':
                years = 1/12
            elif c[1] == 'yr':
                years = 1
            else: # hope this doest not happend
                years = 0
            columns_years.append(float(c[0])*years)
        bonds.columns = columns_years
        bonds = bonds.iloc[-1]
        bonds = bonds.rename('rate')
        bonds /= 100 # from percentage to float
        
    elif area == '':
        pass
    
    else:
        pass
    
    return bonds

if __name__ == '__main__':
    
    bonds = _downloadBonds('^XSP')
