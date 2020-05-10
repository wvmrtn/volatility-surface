#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:31:55 2020

@author: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

# import standard libraries
from threading import Timer
import webbrowser
# import third-party libraries
import dash
# import local libraries
from volatility_surface import _DEBUG, PORT
from volatility_surface import MainPage

def open_browser():
      webbrowser.open_new('http://127.0.0.1:{}'.format(PORT))

if __name__ == '__main__':

    app = dash.Dash(__name__,
                    external_stylesheets = ['https://codepen.io/wvmrtn/pen/GRpvLOM.css'])
    # serve css from codepen
    app.config['suppress_callback_exceptions'] = True
    app.title = 'surface-volatility'    
        
    main_page = MainPage(app)
    app.layout = main_page.layout
    
    # handle different versions of dash across different operating systems
    try:
        Timer(1, open_browser).start()
        app.run_server(debug = _DEBUG, port = PORT)
    except:
        Timer(1, open_browser).start()
        app.run_server(debug = not _DEBUG, port = PORT)