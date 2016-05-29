# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''Dmarc Report module.'''

import kivy
kivy.require('1.9.1')

from kivy.app import App

from src import config as cnf
from src.footer import Footer


class DmarcReport(App):

    '''Dmarc Report.'''

    def __init__(self, **kwargs):
        super(DmarcReport, self).__init__(**kwargs)
        self.kv_directory = cnf.KV_DIRECTORY
        self.footer = Footer()

        # Self is the view.
        # Model.
        # TODO: Put the model in here when you get that far.
        # Controller.
        # TODO: Put the controller in here when you get that far.
