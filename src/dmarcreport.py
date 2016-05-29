# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''Dmarc Report'''

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder


from src import config as cnf
from src.footer import Footer


class DmarcReport(App):

    '''Dmarc Report'''

    def __init__(self, **kwargs):
        super(DmarcReport, self).__init__(**kwargs)
        Builder.load_file('{0}/generic.kv'.format(cnf.KV_DIRECTORY))
        Builder.load_file('{0}/dmarcreport.kv'.format(cnf.KV_DIRECTORY))

        self.footer = Footer()
