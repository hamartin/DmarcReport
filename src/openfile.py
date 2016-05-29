# -*- coding: UTF-8 -*-
# File name: openfile.py

'''Dmarc Report open file module.'''

import kivy
kivy.require('1.9.1')

import os

from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from src import config as cnf


class LoadDialog(FloatLayout):

    '''Dmarc Report open file dialog.'''

    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class OpenFile(Label):

    '''Dmarc Report open file.'''

    Builder.load_file('{0}/openfile.kv'.format(cnf.KV_DIRECTORY))
    _popup = None

    def dismiss_popup(self):
        '''Dismisses the load file popup window.'''
        self._popup.dismiss()

    def load(self, path, filename):
        '''Loads a file.'''
        fpr = open(os.path.join(path, filename[0]), 'r')
        self.text_input.text = fpr.read()

    def on_touch_down(self, touch):
        '''Triggers the open file window.'''
        if self.collide_point(touch.x, touch.y):
            content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
            self._popup = Popup(title='Load file', content=content,
                                size_hint=(.9, .9))
            self._popup.open()
            return True
        # return super(OpenFile, self).on_touch_down(touch)
        return Label.on_touch_down(self, touch)
