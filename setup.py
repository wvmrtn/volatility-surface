#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:36:58 2020

@authors: Kassi Franck Atte Aka, Corentin Bourdeix, William Martin
"""

from setuptools import setup

setup(
      name = 'volatility_surface',
      version = '0.0.0',
      author = 'Kassi Franck Atte Aka, Corentin Bourdeix, William Martin',
      description = 'An application to visualize volatility surfaces.',
      packages = ['volatility_surface'],
      install_requires=[
          'dash>=1.0.0',
          'pandas>=1.0.0',
          'scipy>=1.0.0',
          'jupyter-dash',
          'requests>=2.0.0'
          ],
      )