# -*- coding: UTF-8 -*-

'''A module that overloads the boxlayout and label so that we can create
objects of boxlayouts with two labels in them where one label is static
and the other is dynamic.'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class DmarcFrontLabel(BoxLayout):

    '''A grid with two labels in it where one, the left is static and the
    right is dynamic.'''

    def __init__(self, text='', **kwargs):
        super(DmarcFrontLabel, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        self.add_widget(Label(text=text))
        self.value = Label(text='')
        self.add_widget(self.value)

    def set_value(self, val):
        '''Sets the value.'''
        self.value.text = val
