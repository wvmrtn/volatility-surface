# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:42:06 2020

@author: corentin
"""

from plotly.offline import plot
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.graph_objects as go


def affichage3D(sigma,maturity,strike):

    fig = go.Figure(data=[go.Surface(x=maturity,y=strike,z=sigma,colorscale='Viridis')])
    fig.update_layout(title_text='Volatility surface', autosize=True,
                  width=500, height=500,

                  scene = dict(
                    xaxis_title='Maturity',
                    yaxis_title='Strike',
                    zaxis_title='Volatility'),

                  margin=dict(r=20, b=10, l=10, t=90))
    
    plot(fig)
    # fig.show()
    
    return

def remplacenull(liste_sig,strike_fin,list_null):
    exit=0
    ind0=0
    
    while exit==0:
        dep=ind0 +0
        listi=[list_null[ind0]]

        while ind0+1<len(list_null) and list_null[ind0+1] == list_null[ind0]+1 :
            
            listi.append(list_null[ind0+1])
            ind0=ind0+1
        
        if len(listi) > 0:
            for i in range(len(listi)):
                h= (liste_sig[list_null[ind0]+1]- liste_sig[list_null[dep]-1])/(strike_fin[list_null[ind0]+1] -strike_fin[list_null[dep]-1] )
                liste_sig[i+list_null[dep]]= liste_sig[list_null[dep]-1] + (strike_fin[i+list_null[dep]]- strike_fin[list_null[dep]-1])*h
        
        ind0=ind0+1
        if ind0 >= len(list_null):
            exit=1
    return liste_sig
    
    

def step_std_from_strike(std,strike,N):
    liste_strike= np.linspace(min(strike),max(strike)+0.1,N+1)
    liste_sig = np.zeros(N)
    strike_fin=np.zeros(N)
    list_null=[]
    for i in range(N):
        mask1= (strike < liste_strike[i+1]) & (strike >= liste_strike[i])
        if len(std[mask1])== 0:
            list_null.append(i)
        else :
            liste_sig[i]=np.mean(std[mask1])
        strike_fin[i]= (liste_strike[i] + liste_strike[i+1])/2
        
    if len(list_null) > 0:
        liste_sig = remplacenull(liste_sig,strike_fin,list_null)
        
        
        
    return liste_sig,strike_fin
    

def aff_surface(sigma_calcul,strike,maturity):
    
    maturity_surf = np.zeros(len(maturity))
    sig_surf=np.zeros(len(maturity))
    strike_surf=np.zeros(len(maturity))
    mat= np.unique(maturity)
    
    for m in mat:
        mask = maturity==m
        N= len(maturity[mask])
        
        sigm, strikem = step_std_from_strike(sigma_calcul[mask],strike[mask],N)
        maturity_surf[mask]= m
        sig_surf[mask]=sigm
        strike_surf[mask]=strikem

    affichage3D(sig_surf,maturity_surf,strike_surf)

    
    return

#test 
std=np.array([0,1,2,5,2,6,8,9])
strike=np.array([10,12,20,22,80,60,25,50])
mat=np.array([1,1,3,3,1,2,2,3])

aff_surface(std,strike,mat)

