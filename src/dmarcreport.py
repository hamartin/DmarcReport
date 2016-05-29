# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''Dmarc Report module.'''

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

from src import config as cnf


class DmarcReportNui(GridLayout):

    '''Dmarc Report App.'''

    Builder.load_file('{0}/dmarcreportnui.kv'.format(cnf.KV_DIRECTORY))


class DmarcReport(App):

    '''Dmarc Report.'''

    def build(self):
        '''Creates the GNUI.'''
        return DmarcReportNui()
