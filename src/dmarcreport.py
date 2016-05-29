# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''Dmarc Report module.'''

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from src import config as cnf

Builder.load_file('{0}/dmarcreport.kv'.format(cnf.KV_DIRECTORY))


class DmarcReport(App):

    '''Dmarc Report.'''

    title = cnf.TITLE

    def build(self):
        '''Builds the NUI.'''
        return DmarcReportNui()


class DmarcReportNui(FloatLayout):

    '''Dmarc Report NUI.'''

    def load(self, path, sel):
        '''Loads the selected file stored in path.'''
        print path
        print sel

    def cancel(self):
        '''Goes back to the Dmarc Record item in the accordion.'''
        print "Go back!"
