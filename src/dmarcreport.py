# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''Dmarc Report'''

import kivy
kivy.require('1.9.1')

from kivy.app import App

from src import config as cnf


class DmarcReport(App):

    '''Dmarc Report'''

    kv_directory = cnf.KV_DIRECTORY
