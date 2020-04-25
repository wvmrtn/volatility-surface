#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:54:28 2020

@authors: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
import datetime
import numpy as np
import requests as re
import urllib.parse
# import third-party libraries
import pandas as pd
# import local libraries
from config import _TICKERS, _BASE_URL, _YEAR
from bond_requests import _downloadBonds

class Index:
    """ Index object to get options.
    
    Attributes
    ----------
    ticker : string
        Ticker symbol of the market
    
    """
    
    def __init__(self, ticker, div_yield):
        """Init function of class.

        Parameters
        ----------
        ticker : string
            Ticker symbol of index.
        div_yield : float
            Dividend yield of the index. Not in percentage.

        Returns
        -------
        None.

        """
        # some basic information
        assert ticker in _TICKERS, 'Ticker not valid.'
        self.ticker = ticker
        self.ticker_encoded = urllib.parse.quote(ticker)
        self.div_yield = div_yield
        self.options = pd.DataFrame()
        self.bonds = pd.DataFrame()
            
        # get all maturity dates (epoch times)
        content = self._customGet()
        epochs = content['optionChain']['result'][0]['expirationDates']
        dates = [self._epochToDate(m) for m in epochs]
        self.maturity_dates = dict(zip(dates, epochs))
        self.maturity_epochs = dict(zip(epochs, dates))
        
        # get price of index
        content = self._customGet(get = 'price')
        self.price = content['chart']['result'][0]['meta']['regularMarketPrice']

    @staticmethod
    def _epochToDate(epoch):
        """ Transform epoch integers to dates in strings

        Parameters
        ----------
        epoch : int
            Epoch number of maturity date.

        Returns
        -------
        string
            The equivalent epoch time in date string.

        """
        return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d') 

    def _customGet(self, get = 'options', date = None):
        """Custom get requests.

        Parameters
        ----------
        get : string, optional
            What to get.  The default is 'options'
        date : string or int, optional
            The maturity date of the option. The default is None.

        Raises
        ------
        error
            Requestion error.

        Returns
        -------
        response : dict
            JSON-type reponse from request.

        """
        if get == 'options':
            if not date:
                url = '{}/v7/finance/options/{}'.format(_BASE_URL, self.ticker_encoded)
            else:
                url = '{}/v7/finance/options/{}?date={}'.format(_BASE_URL,
                                                                self.ticker_encoded,
                                                                date)
        elif get == 'price': # get price otherwise
            url = '{}/v8/finance/chart/{}'.format(_BASE_URL, 
                                                  self.ticker_encoded)
        else:
            url = ''
            
        # try requests
        try:
            response = re.get(url).json()
            return response
        # raise error, cannot continue
        except re.exceptions.RequestException as e:
            raise e

    def downloadOptions(self, date, parse_to_df = True):
        """Donwload options of index at date.

        Parameters
        ----------
        date : string or int
            Maturity or expiration date of options.
        parse_to_df : bool, optional
            Parse options from request from pandas.DataFrame. 
            The default is True.

        Returns
        -------
        dict or pandas.DataFrame
            Options, either raw from request or cleaned in a pandas.DataFrame.

        """
        # get epoch time
        if isinstance(date, str):
            date = self.maturity_dates[date]
            
        options = self._customGet(date = date)
        
        if parse_to_df:
            return self._parseOptions(options) 
        else:
            return options  
        
    def _parseOptions(self, raw_options):
        """Parse raw options into one pandas.DataFrame.

        Parameters
        ----------
        raw_options : dict
            Raw optionss from request.

        Returns
        -------
        options_df : pandas.DataFrame
            All options cleaned into one pandas.DataFrame.

        """
        
        # transform options to dataframe
        options = raw_options['optionChain']['result'][0]['options'][0]
        calls = options['calls']
        puts = options['puts']
        # keep only these entries
        keep = ['strike', 'ask', 'bid', 'impliedVolatility', 'expiration']
        # put in dataframe and keep only columns 
        calls_df = pd.DataFrame(calls, columns = keep)
        puts_df = pd.DataFrame(puts, columns = keep)
        # add column type (call/option)
        calls_df['type'] = 'call'
        puts_df['type'] = 'put'
        # add column with date from epoch time
        options_df = pd.concat([calls_df, puts_df], axis = 0)
        # add column with string date
        options_df['maturityDate'] = options_df['expiration'].apply(self._epochToDate)
        # date to datetime object
        options_df['maturityDate'] =  pd.to_datetime(options_df['maturityDate'])
        # put number of days till maturityDate normalized by year
        now = datetime.datetime.now()
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        options_df['maturity'] = (options_df['maturityDate'] - now).dt.days/_YEAR 
        # drop expiration
        options_df = options_df.drop(columns = 'expiration')
        # add column average between ask and bid
        options_df['optionPrice'] = options_df[['ask', 'bid']].mean(axis = 1)

        return options_df
    
    def downloadAllOptions(self):
        """Download all options at all maturity dates.

        Returns
        -------
        options_df : pandas.DataFrame
            All options at all maturity dates.

        """
        options_df = pd.DataFrame()
        for _, epoch in self.maturity_dates.items():
            temp = self.downloadOptions(date = epoch, parse_to_df = True)
            options_df = pd.concat([options_df, temp], axis = 0)
        # reset index
        options_df = options_df.reset_index(drop = True)
        self.options = options_df
        
        # do a merge with bonds if not empty
        if not self.bonds.empty:
            self.options = self._merge()
        
        return self.options
    
    def downloadBonds(self):
        """Download treasury bonds.

        Returns
        -------
        pandas.Series
            Series containing yield curve.

        """
        self.bonds = _downloadBonds(self.ticker)
        
        # do a merge with options if not empty
        if not self.options.empty:
            self.options = self._merge()
        
        return self.bonds
    
    def _merge(self, options = None, bonds = None):
        """Merge bonds and options intelligently

        Parameters
        ----------
        options : pandas.DataFrame, optional
            DataFrame containing options. The default is None.
        bonds : pandas.Series, optional
            Series containing bonds. The default is None.

        Returns
        -------
        options : pandas.DataFrame
            Options with bonds merged into them.

        """
        # merge bonds rate into options
        if options is None:
            options = self.options.copy()
        if bonds is None:
            bonds = self.bonds.copy()
    
        options['rate'] = np.nan
        # iterate over bonds and place them correctly in options
        for maturity, rate in bonds[::-1].iteritems():
            options['rate'] = options['rate'].mask(options['maturity'] < maturity,
                                                   rate)
        
        return options       


# for testing
if __name__ == '__main__':
    
    div_yield = 0.0231
    ticker = list(_TICKERS.keys())[0]
    sp500 = Index(ticker, div_yield)
    #options = sp500.downloadOptions(1591920000, parse_to_df = False)
    options = sp500.downloadAllOptions()
    
    
    
