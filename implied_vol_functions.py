#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:49:05 2020

@authors: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

from scipy.stats import norm
import numpy as np
import pandas as pd

def black_scholes(S,sigma,k,tau,r,delta,types):
    
    #S: spot price
    #K: strike price
    #tau: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    #delta: continuous dividend rate
    #interest rate annualized

    d_d= (1/(sigma*np.sqrt(tau))) * (np.log(np.exp((r-delta)*tau) *S/k)-0.5*tau*(sigma**2))
    d_u= (1/(sigma*np.sqrt(tau))) * (np.log(np.exp((r-delta)*tau)*S/k)+0.5*tau*(sigma**2))
   
    if types=="put":
        price=  np.exp(-r*tau)*k*norm.cdf(-d_d) - np.exp(-delta*tau)*S*norm.cdf(-d_u)
    if types=="call":
        price=  np.exp(-delta*tau)*S*norm.cdf(d_u)-np.exp(-r*tau)*k*norm.cdf(d_d)
  
    return price
  
###############################################################

def vega(S,sigma,k,tau,r,delta):
    
    d_u= (1/(sigma*np.sqrt(tau))) * (np.log(np.exp((r-delta)*tau)*S/k)+0.5*tau*(sigma**2))
    v= np.exp(-delta*tau)*S*np.sqrt(tau)*norm.pdf(d_u)
    
    return v


###############################################################

def vol_extraction(H,S,sigma_0,k,tau,r,delta,types,error):
    # extract the implied volatility using Newton's optimisation scheme
    #S: spot price
    #K: strike price
    #tau: time to maturity
    #r: interest rate annualized
    #sigma: volatility of underlying asset
    #delta: continuous dividend rate
    #H: option price
    
    vol= sigma_0
    
    bs= black_scholes(S,vol,k,tau,r,delta,types)
    
    while abs(bs-H)>error:
        vol = vol - (bs-H)/vega(S,vol,k,tau,r,delta)
        bs= black_scholes(S,vol,k,tau,r,delta,types)
        
  
    return  vol
 
###############################################################    
     
def compact(df):
    
    tab=pd.DataFrame(np.zeros(3).reshape(-1,3))
    tab.columns=["maturity","strike","implied_vol"]
    maturity= df["maturity"].unique()
    
    for m in maturity:
        
        sub = df[df["maturity"]==m].groupby("strike").mean()
        sub["strike"]= sub.index.values
        sub.index=range(len(sub))
        
        tab=pd.concat([tab,sub])
        
    return tab.drop(0)
        
 ###############################################################
 
def implied_vol(df,sigma_0,error):#,div_yield,S): 
    #df: dataframe, cols={price","strike","maturity","rate","div_yield","type"}
    #div_yield: dividend yield  of the market
    #S: stock price
    
    result = pd.DataFrame()
    df2= df.copy()
    df2["implied_vol"]=np.nan
     
    #n= df2.shape[0]

    for i, row in df2.iterrows():  #for i in range(n):
        
        # S=df2["price"][i]
        # tau=df2["maturity"][i]
        # k=df2["strike"][i]
        # r=df2["rate"][i]
        # delta=div_yield
        # types=df2["type"][i]
        
        S =  row['lastPrice']
        tau = row['maturity']
        k = row['strike']
        r = row['rate']
        delta = row['delta']
        types = row['type']
        
        df2.at[i, 'implied_vol']= vol_extraction(S,sigma_0,k,tau,r,delta,types,error)

    
    result=compact(df2[["strike","maturity","implied_vol"]])
   
    return result

        
        
    
    
    
    
    
 
 
 
