# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''Dmarc Report'''

import kivy
kivy.require('1.9.1')

from kivy.app import App


class DmarcReport(App):

    '''Dmarc Report'''

    def build(self):
        '''Builds the Dmarc Report front end.'''
        from kivy.uix.label import Label
        return Label(text='Dmarc Report')
