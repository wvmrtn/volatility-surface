#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:49:05 2020

@authors: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
import copy
import os
import requests
import sys
# import third-party libraries
import pandas as pd
# import local libraries
from volatility_surface.config import _MAPPING, _TICKERS

# constants
_BONDS_PATH = os.path.dirname(__file__)
_BONDS_FOLDER = 'bonds'

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
        
        try:
            # transform US bonds
            url = _MAPPING[area]
            html = requests.get(url).content 
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
            
            # write in case 
            bonds.to_csv(os.path.join(_BONDS_PATH, _BONDS_FOLDER, area + '.csv'))
            
        except:
            # download in case
            print('Error while getting bonds for {}: {}'\
                  .format(area, sys.exc_info()[0]))
            bonds = pd.read_csv(os.path.join(_BONDS_PATH, _BONDS_FOLDER, area + '.csv'),
                                index_col = 0, squeeze = True)
            
    elif area == 'Europe':
        
        try:
            url = _MAPPING[area]
            html = requests.get(url).content
            bonds = pd.read_html(html)[1]
            bonds = bonds.drop(columns = ['Period', '% Chg Prev'])
            bonds['Value'] = bonds['Value'].str.rstrip('%')
            # drop rows starting with AAA
            bonds = bonds[~bonds['Indicator'].str.contains('AAA')]
            # get only year value in strings
            bonds['Indicator'] = bonds['Indicator'].str.extract('(\d+)', expand = False)
            # turn everything to float
            bonds = bonds.astype(float)
            # sort wrt to indicator
            bonds = bonds.sort_values(by = 'Indicator')
            bonds = bonds.reset_index(drop = True)
            # turn to series
            temp = pd.Series(data = bonds['Value'])
            temp.index = bonds['Indicator']
            # other things to do
            bonds = copy.deepcopy(temp)
            bonds.index.name = None
            # rename column
            bonds = bonds.rename('rate')
            # convert from percentage to float
            bonds /= 100
            
            # write in case 
            bonds.to_csv(os.path.join(_BONDS_PATH, _BONDS_FOLDER, area + '.csv'))
            
        except:
            # download in case
            print('Error while getting bonds for {}: {}'\
                  .format(area, sys.exc_info()[0]))
            bonds = pd.read_csv(os.path.join(_BONDS_PATH, _BONDS_FOLDER, area + '.csv'),
                                index_col = 0, squeeze = True)
    
    else:
        pass
    
    return bonds

if __name__ == '__main__':
    
    bonds = _downloadBonds('FEZ')
