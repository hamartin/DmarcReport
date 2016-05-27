# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''Dmarc Report module.'''

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from src import config as cnf
from src.footer import Footer
from src.loadfile import LoadFile

Builder.load_file('{0}/dmarcreportnui.kv'.format(cnf.KV_DIRECTORY))


class DmarcReportNui(GridLayout):

    '''Dmarc Report App.'''

    footer = Footer()
    _popup = None

    def show_load_list(self):
        '''Shows a list of files to choose between.'''
        content = LoadFile(load=self.load_list, cancel=self.dismiss_popup)
        self._popup = Popup(title='Load file', content=content,
                            size_hint=(1, 1))
        self._popup.open()

    def load_list(self, path, filename):
        '''Loads the list of files.'''
        print path
        print filename
        pass

    def dismiss_popup(self):
        '''Hides the list view window.'''
        self._popup.dismiss()


class DmarcReport(App):

    '''Dmarc Report.'''

    def build(self):
        '''Creates the GNUI.'''
        return DmarcReportNui()
