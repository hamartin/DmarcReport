# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''Dmarc Report module.'''

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.pagelayout import PageLayout

from src import config as cnf

Builder.load_file('{0}/dmarcreport.kv'.format(cnf.KV_DIRECTORY))


class DmarcReport(App):

    '''Dmarc Report.'''

    title = 'Dmarc Report'.title()

    def build(self):
        '''Builds the NUI.'''
        return DmarcReportNui()


class DmarcReportNui(PageLayout):

    '''Dmarc Report NUI.'''

    pass
