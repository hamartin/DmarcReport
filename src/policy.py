# -*- coding: UTF-8 -*-

'''A box containing policy information from a DMARC XML.'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import src.dmarcfrontlabel as dmfl


class Policy(BoxLayout):

    '''A box containing the policy information from a DMARC XML.'''

    def __init__(self, **kwargs):
        super(Policy, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.var_domain = dmfl.DmarcFrontLabel(text='Domain')
        self.var_adkim = dmfl.DmarcFrontLabel(text='Adkim')
        self.var_aspf = dmfl.DmarcFrontLabel(text='Aspf')
        self.var_p = dmfl.DmarcFrontLabel(text='P')
        self.var_sp = dmfl.DmarcFrontLabel(text='Sp')
        self.var_pct = dmfl.DmarcFrontLabel(text='Pct')

        self.initialize()

    def initialize(self):
        '''Initializes all the widgets.'''
        self.add_widget(Label(text='[b]Policy Published[/b]', markup=True,
                              font_size='25sp'))
        self.add_widget(self.var_domain)
        self.add_widget(self.var_adkim)
        self.add_widget(self.var_aspf)
        self.add_widget(self.var_p)
        self.add_widget(self.var_sp)
        self.add_widget(self.var_pct)
