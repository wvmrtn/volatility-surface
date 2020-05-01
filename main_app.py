#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:31:55 2020

@author: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
# import third-party libraries
import dash
# import local libraries
from config import _DEBUG
from webpage import MainPage

if __name__ == '__main__':
    
    app = dash.Dash(__name__)
    app.config['suppress_callback_exceptions'] = True
    app.title = 'surface-volatility'    
        
    main_page = MainPage(app)
    app.layout = main_page.layout
    
    app.run_server(debug = _DEBUG)
