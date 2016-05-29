# -*- coding: UTF-8 -*-

'''A box containing policy information from a DMARC XML.'''

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class Policy(GridLayout):

    '''A box containing the policy information from a DMARC XML.'''

    def __init__(self, **kwargs):
        super(Policy, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='foo'))
        self.add_widget(Label(text='bar'))
        self.add_widget(Label(text='baz'))
        self.add_widget(Label(text='boom'))
