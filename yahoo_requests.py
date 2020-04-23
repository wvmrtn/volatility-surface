#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:54:28 2020

@authors: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
import datetime
import json
import requests as re
import urllib.parse
# import third-party libraries
import pandas as pd
# import local libraries

BASE_URL = 'https://query1.finance.yahoo.com'

class Market:
    """ Market object to get options.
    
    Attributes
    ----------
    ticker : string
        Ticker symbol of the market
    
    """
    def __init__(self, ticker):
        # some basic information
        self.ticker = ticker
        self.ticker_encoded = urllib.parse.quote(ticker)
            
        # get all maturity dates (epoch times)
        content = self.customGet()
        epochs = content['optionChain']['result'][0]['expirationDates']
        dates = [self.epochToDate(m) for m in epochs]
        self.maturity_dates = dict(zip(dates, epochs))
        self.maturity_epochs = dict(zip(epochs, dates))

    @staticmethod
    def epochToDate(epoch):
        return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d') 

    def customGet(self, date = None):
        if not date:
            url = '{}/v7/finance/options/{}'.format(BASE_URL, self.ticker_encoded)
        else:
            url = '{}/v7/finance/options/{}?date={}'.format(BASE_URL,
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
        # get epoch time
        if isinstance(date, str):
            date = self.maturity_dates[date]
            
        options = self.customGet(date = date)
        
        if parse_to_df:
            return self.parseOptions(options) 
        else:
            return options  
        
    def parseOptions(self, raw_options):
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
    
    def downloadAllOptions(self, parse_to_df = True):
        options_df = pd.DataFrame()
        for _, epoch in self.maturity_dates.items():
            temp = self.downloadOptions(date = epoch)
            options_df = pd.concat([options_df, temp], axis = 0)
        
        return options_df
    

# for testing
if __name__ == '__main__':
    
    sp500 = Market('^XSP')
    # options = sp500.downloadOptions(1591920000, parse_to_df = True)
    options = sp500.downloadAllOptions()
    
    
    
    
    
    
    
