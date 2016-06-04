# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''Dmarc Report module.'''

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from src import config as cnf


class DmarcReport(App):

    '''Dmarc Report.'''

    title = 'Dmarc Report'

    def build(self):
        '''Builds the NUI.'''
        return DmarcReportNui()


class DmarcReportNui(FloatLayout):

    '''Dmarc Report NUI.'''


class ImageButton(ButtonBehavior, Image):

    '''Kivy button with image instead of label.'''

    footer = ObjectProperty()

    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_motion)
        self.source = cnf.IMAGENORMAL
        self.popup = None

        for key, val in kwargs.iteritems():
            if key == 'source':
                self.source = val

    def on_motion(self, etype, motionevent):
        '''When mouse is above image, change picture.'''
        if etype and motionevent:
            if self.collide_point(Window.mouse_pos[0], Window.mouse_pos[1]) \
                    and self.source != cnf.IMAGEOVER:
                self.source = cnf.IMAGEOVER
                self.footer.text = 'Open file…'
            elif(not self.collide_point(Window.mouse_pos[0],
                                        Window.mouse_pos[1]) and
                 self.source != cnf.IMAGENORMAL):
                self.source = cnf.IMAGENORMAL
                self.footer.text = ''

    def openfile(self):
        '''Creates a popup window where a file to open can be chosen.'''
        content = OpenFile(footer=self.footer)
        self.popup = Popup(title='Open file', content=content,
                           size_hint=(.8, .8))
        content.popup = self.popup
        self.popup.open()


class OpenFile(BoxLayout):

    '''Open file popup window.'''

    footer = ObjectProperty()
    popup = ObjectProperty()

    def dismiss(self):
        '''Dismisses the popup we're in.'''
        self.popup.dismiss()

    def load(self, filename):
        '''Loads the file given to it.'''
        if not filename:
            return

        try:
            # Try to open file and get data.
            print filename
        except:
            self.footer.text = 'Something failed!'
        else:
            self.footer.text = 'File opened: {0}'.format(filename)
            self.dismiss()


Builder.load_file('{0}/dmarcreport.kv'.format(cnf.KV_DIRECTORY))
