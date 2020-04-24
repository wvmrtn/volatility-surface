#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:54:28 2020

@authors: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
import datetime
import requests as re
import urllib.parse
# import third-party libraries
import pandas as pd
# import local libraries
from config import _TICKERS
from bond_requests import _downloadBonds

_BASE_URL = 'https://query1.finance.yahoo.com'

class Market:
    """ Market object to get options.
    
    Attributes
    ----------
    ticker : string
        Ticker symbol of the market
    
    """
    
    def __init__(self, ticker,  div_yield):
        """Init function of class.

        Parameters
        ----------
        ticker : string
            Ticker symbol of index.
        div_yield : float
            Dividend yield of the index. Not percentage.

        Returns
        -------
        None.

        """
        # some basic information
        assert ticker in _TICKERS, 'Ticker not valid.'
        self.ticker = ticker
        self.ticker_encoded = urllib.parse.quote(ticker)
        self.div_yield = div_yield
            
        # get all maturity dates (epoch times)
        content = self.customGet()
        epochs = content['optionChain']['result'][0]['expirationDates']
        dates = [self.epochToDate(m) for m in epochs]
        self.maturity_dates = dict(zip(dates, epochs))
        self.maturity_epochs = dict(zip(epochs, dates))

    @staticmethod
    def epochToDate(epoch):
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

    def customGet(self, date = None):
        """Custom get requests.

        Parameters
        ----------
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
        if not date:
            url = '{}/v7/finance/options/{}'.format(_BASE_URL, self.ticker_encoded)
        else:
            url = '{}/v7/finance/options/{}?date={}'.format(_BASE_URL,
                                                            self.ticker_encoded,
                                                            date)
        # try requests
        try:
            response = re.get(url).json()
            return response
        # raise error, cannot continue
        except re.exceptions.RequestException as e:
            raise e

    def downloadOptions(self, date, parse_to_df = True):
        """Donwload options of market at date.

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
            
        options = self.customGet(date = date)
        
        if parse_to_df:
            return self.parseOptions(options) 
        else:
            return options  
        
    def parseOptions(self, raw_options):
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
        keep = ['strike', 'lastPrice', 'impliedVolatility', 'expiration']
        # put in dataframe and keep only columns 
        calls_df = pd.DataFrame(calls, columns = keep)
        puts_df = pd.DataFrame(puts, columns = keep)
        # add column type (call/option)
        calls_df['type'] = 'call'
        puts_df['type'] = 'put'
        # add column with date from epoch time
        options_df = pd.concat([calls_df, puts_df], axis = 0)
        # add column with string date
        options_df['maturity'] = options_df['expiration'].apply(self.epochToDate)

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
        
        return options_df
    
    def downloadBonds(self):
        
        return None
    

# for testing
if __name__ == '__main__':
    
    ticker = list(_TICKERS.keys())[0]
    sp500 = Market(ticker)
    # options = sp500.downloadOptions(1591920000, parse_to_df = True)
    options = sp500.downloadAllOptions()
    
    
    
    
    
    
    
