# -*- coding: UTF-8 -*-

'''A box containing report information from a DMARC XML.'''

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class Report(GridLayout):

    '''A box containing the report information from a DMARC XML.'''

    def __init__(self, **kwargs):
        super(Report, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='foo'))
        self.add_widget(Label(text='bar'))
        self.add_widget(Label(text='baz'))
        self.add_widget(Label(text='boom'))
