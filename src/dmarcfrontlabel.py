# -*- coding: UTF-8 -*-

'''A module that overloads the boxlayout and label so that we can create
objects of boxlayouts with two labels in them where one label is static
and the other is dynamic.'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import src.config as cnf


class DmarcFrontLabel(BoxLayout):

    '''A grid with two labels in it where one, the left is static and the
    right is dynamic.'''

    def __init__(self, text='', **kwargs):
        super(DmarcFrontLabel, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        self.add_widget(Label(
            text=cnf.COLOR1BEGIN + text.title() + cnf.COLORSTOP, markup=True,
            halign='left', text_size=(100, None)))
        self.value = Label(text='', markup=True, halign='right')
        self.add_widget(self.value)

    def set_value(self, val):
        '''Sets the value.'''
        self.value.text = cnf.COLOR1BEGIN + val + cnf.COLORSTOP
