#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:37:04 2020

@author: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
# import third-party libraries
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
# import local libraries
from volatility_surface.yahoo_requests import Index
from volatility_surface.implied_vol_functions import implied_vol
from volatility_surface.plotsurface import aff_surface
import volatility_surface.config as cfg

class MainPage:
    
    def __init__(self, app):
        
        self.app = app
        
        # call about content
        self.about_page = AboutPage(self.app)
        self.about_page.serveLayout()
        
        # call plot content
        self.plot_page = PlotPage(self.app)
        self.plot_page.serveLayout()
        
        # create layout
        self.layout = html.Div(
            
            [
                
                # div containing the banner
                html.Div(
                    
                    [
                    
                    html.H2('volatility-surface', className = 'BannerH2')
                    
                    ], className = 'MainBannerDiv', id = 'main-banner-div'),
                
                # div containing the tabs and graph
                html.Div(
                    
                    dcc.Loading(id = 'loading-figure',
                                className = 'LoadingFigure',
                                type = 'cube',
                                color = '#f5f5f5',
                                children = 
                    
                    [
                     
                    html.Div(
                        
                        [
                         
                        dcc.Tabs(value = 'tab-1',
                                 children = [
                                     dcc.Tab(label = 'About', value = 'tab-1', 
                                             className = 'Tab',
                                             selected_className = 'TabSelected',
                                             selected_style = {'backgroundColor': '#302e2b',
                                                               'color': '#f5f5f5'},
                                             style = {'backgroundColor': '#302e2b',
                                                               'color': '#f5f5f5'}), 
                                     dcc.Tab(label = 'Plot', value = 'tab-2',
                                             className = 'Tab',
                                             selected_className = 'TabSelected',
                                             selected_style = {'backgroundColor': '#302e2b',
                                                               'color': '#f5f5f5'},
                                             style = {'backgroundColor': '#302e2b',
                                                               'color': '#f5f5f5'}), #ebeef5
                                     ], className = 'Tabs', id = 'tabs')
                            
                        ], className = 'TabsDiv', id = 'tabs-div'),
                    
                    html.Div(className = 'TabContent', id = 'tab-content',
                             children = self.plot_page.layout), # dirty fix
                    
                    html.Div([], className = 'FigureDiv', 
                             id = 'figure-div'),
                    
                    ]), className = 'ContentDiv', id = 'content-div'),
                
            ], className = 'MainDiv', id = 'main-div')
        
    
        self.invokeCallbacks()
        
        
    def invokeCallbacks(self):
        
        # callback to serve tabs
        @self.app.callback(Output('tab-content', 'children'),
                           [Input('tabs', 'value')])
        def serveContent(tab):
            if tab == 'tab-1':
                return self.about_page.layout
            
            elif tab == 'tab-2':
                return self.plot_page.layout
            
            else:
                return []
            
        # callback to draw surface plot
        @self.app.callback(Output('figure-div', 'children'),
                           [Input('plot-button', 'n_clicks')],
                           [State('dropdown-ticker', 'value'),
                            State('input-yield', 'value')]
                           )
        def plotSurface(clicked, ticker, div_yield):
            if div_yield is not None and clicked > 0:
                
                # create index object
                index = Index(ticker, div_yield/100)
                index.downloadAllOptions()
                index.downloadBonds()
                options = index.options
                
                # price of index
                price = index.price
                # dividen yield
                dividend = index.div_yield
                
                # get results
                results = implied_vol(options, sigma_0 = 1, error = 10**-(6), 
                                      div_yield = dividend, S = price)
                
                # get plotly figure
                fig = aff_surface(sigma_calcul = results["implied_vol"],
                                  strike = results["strike"],
                                  maturity = results["maturity"],
                                  _plot = False)
                
                return [dcc.Graph(figure = fig,
                                  config = {'displayModeBar': False},
                                  id = 'surface-plot',
                                  className = 'SurfacePlot')
                        ]
                    
            else:
                return []
            
class AboutPage:
    
    def __init__(self, app):
        
        self.app = app
        self.layout = None
        
    # serve layout
    def serveLayout(self):
        self.layout = html.Div(
            
            [
                
            html.H4(children = 'volatility-surface', className = 'H4About'),
            html.P('Use this calculator to calculate and visualized the implied volatility surface of the S&P500 index and the Euro Stoxx 50 index.', 
                   className = 'PTag'),
            html.P('By using the market price of the option as a known variable in the BSM formula, underlying volatility can be back-calculated and the volatility calculated this way is known as implied volatility.',
                   className = 'PTag'),
            html.P('Implied volatility represents the market expectation of the volatility and it is often used to check if an option is under or overpriced.', 
                   className = 'PTag')
                
            ], className = 'AboutDiv', id = 'about-div')
            
        
class PlotPage:
    
    def __init__(self, app):
        
        self.app = app
        self.layout = None
        
    # serve layout
    def serveLayout(self):
        self.layout = html.Div(
            
            [
                
            html.P('Ticker symbol', className = 'PTag'),
            dcc.Dropdown(options = cfg._DROPDOWN,
                         searchable = False,
                         clearable = False,
                         value = cfg._DROPDOWN[0]['value'],
                         className = 'DropdownTicker',
                         id = 'dropdown-ticker'
                         ),
            html.P('Dividend yield [%]', className = 'PTag'),
            dcc.Input(inputMode = 'numeric',
                      max = 10.00,
                      min = -10.00,
                      type = 'number',
                      id = 'input-yield',
                      value = 0.00,
                      className = 'InputYield',
                      style = {'fontSize': '11pt', 'textAlign': 'center',
                               'verticalAlign': 'middle', 'color': '#525049',
                               'borderRadius': '4px', 'border': '1px solid #ccc',
                               'display': 'table'}),
            html.Button('Plot', n_clicks = 0, 
                        className = 'PlotButton', id = 'plot-button')
            
            ], className = 'PlotDiv', id = 'plot-div')
        
        
if __name__ == '__main__':
    
    pass
