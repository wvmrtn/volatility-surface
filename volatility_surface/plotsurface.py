# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:42:06 2020

@author: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

from plotly.offline import plot
#import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns
import plotly.graph_objects as go


def affichage3D(sigma,maturity,strike, _plot = True):
    
    fig = go.Figure(data=[go.Surface(x=maturity,
                                     y=strike,
                                     z=sigma,
                                     colorscale='RdBu',
                                
                                     colorbar = {'lenmode': 'fraction', 'len': 0.70},
                                     
                                     hovertemplate = 'Maturity: %{x}'+
                                     '<br>Strike: %{y:.0f}<br>'+
                                     'Volatility: %{z:.0f}<extra></extra>',
                                     
                                     )])
    
    camera = dict(
        up = dict(x = 0, y = 0, z = 1),
        center = dict(x = 0, y = 0, z = -0.1),
        eye = dict(x = 1.6, y = 1.6, z = 0.8)
        )
    
    fig.update_layout(
            #title_text='Volatility surface', 

            autosize=True,
            
            width=700, 
            height=700,
            
            scene = dict(
                xaxis_title='Maturity',
                yaxis_title='Strike ($)',
                zaxis_title='Volatility',
                xaxis = dict(showbackground = True,
                             backgroundcolor = '#302e2b',
                             tickfont = dict(color = '#f5f5f5'),
                             gridcolor = '#292724',
                             zerolinecolor = '#292724'),
                yaxis = dict(showbackground = True,
                             backgroundcolor = '#302e2b',
                             tickfont = dict(color = '#f5f5f5'),
                             gridcolor = '#292724',
                             zerolinecolor = '#292724'),
                zaxis = dict(showbackground = True,
                             backgroundcolor = '#302e2b',
                             tickfont = dict(color = '#f5f5f5'),
                             gridcolor = '#292724',
                             zerolinecolor = '#292724'),
                ),
            
            font = dict(color = '#f5f5f5'),

            margin=dict(r=0, b=0, l=0, t=0),
            
            scene_camera = camera,
            
            plot_bgcolor = '#292724',
            paper_bgcolor = '#292724',
            
            )
    
    fig.update_traces(showscale = False)
    
    if _plot:
        plot(fig)
        # fig.show()
    
    return fig

def remplacenull(liste_sig,list_null,strike_fin):
    
    n,m = np.shape(list_null)
    for j in range(m):
        list_nullj = list_null[:,j]
        list_nullm= []
        for k in range(len(list_nullj)):
            if list_nullj[k]==1:
                list_nullm.append(k)
        exit=0
        ind0=0
        
        while exit==0 and len(list_nullm)>0:
            dep=ind0 +0
            listi=[list_nullm[ind0]]
    
            while ind0+1<len(list_nullm) and list_nullm[ind0+1] == list_nullm[ind0]+1 :
                
                listi.append(list_nullm[ind0+1])
                ind0=ind0+1
            
            if len(listi) > 0:
                for i in range(len(listi)):
                    
                    h= (liste_sig[min(list_nullm[ind0]+1,n-1),j]- liste_sig[max(0,list_nullm[dep]-1),j])/(strike_fin[min(list_nullm[ind0]+1,n-1)] -strike_fin[max(0,list_nullm[dep]-1)] )
                    liste_sig[i+list_nullm[dep],j]= liste_sig[max(0,list_nullm[dep]-1),j] + (strike_fin[i+list_nullm[dep]]- strike_fin[max(0,list_nullm[dep]-1)])*h
            
            ind0=ind0+1
            if ind0 >= len(list_nullm):
                exit=1
    return liste_sig
    
    

def step_std_from_strike(std,liste_strike,strike,h):
    
    N = len(liste_strike)
    liste_sig= np.zeros(N)
    list_null=[]
    for i in range(N):
        mask1= (strike < liste_strike[i]+h) & (strike >= liste_strike[i]-h)
        if len(std[mask1])== 0:
            list_null.append(i)
        else :
            liste_sig[i]=np.mean(std[mask1])
        
        
        
    return liste_sig,list_null
    

def aff_surface(sigma_calcul,strike,maturity,_plot=True):
    
    maturity_surf= np.sort(np.unique(maturity))
    strike_u = np.sort(np.unique(strike))
    strike_surf= np.linspace(min(strike_u),max(strike_u)+0.1,int(len(strike_u)/2))
    h = (strike_surf[-1]-strike_surf[0])/len(strike_surf)
    sig_surf=np.zeros((len(strike_surf),len(maturity_surf)))
    list_null=np.zeros((len(strike_surf),len(maturity_surf)))
    for m in range(len(maturity_surf)):
        mask = maturity==maturity_surf[m]
        
        
        sigm,list_nulli = step_std_from_strike(sigma_calcul[mask],strike_surf,strike[mask],h)
        for j in list_nulli:
            list_null[j,m]=1
        sig_surf[:,m]=sigm
        
    sig_surf=remplacenull(sig_surf,list_null,strike_surf)
    maturity_surf2= np.empty(len(maturity_surf),dtype=object)
    
    for i in range(len(maturity_surf)):
        
        if maturity_surf[i]*12 <1:
            maturity_surf2[i] =str(int((maturity_surf[i]*12-int(maturity_surf[i]*12))*30) ) + 'D'
        elif maturity_surf[i]<1:
            maturity_surf2[i] = str(int((maturity_surf[i]*12)%12+1))+'M ' + str(int((maturity_surf[i]*12-int(maturity_surf[i]*12))*30) ) + 'D'
        elif int(maturity_surf[i]) ==maturity_surf[i]:
            maturity_surf2[i] = str(int(maturity_surf[i]))+'Y'
    
        else:
            maturity_surf2[i] = str(int(maturity_surf[i]))+'Y '  +str(int((maturity_surf[i]*12)%12+1))+'M ' + str(int((maturity_surf[i]*12-int(maturity_surf[i]*12))*30) ) + 'D'
        
    
    
    
    
    fig = affichage3D(sig_surf,maturity_surf2,strike_surf,_plot=_plot)
    
    return fig 

#test 
#std=np.array([0,1,2,5,2,6,8,9])
#strike=np.array([10,12,20,22,80,60,25,50])
#mat=np.array([1,1,3,3,1,2,2,3])

#aff_surface(std,strike,mat)

