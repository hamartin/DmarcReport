# -*- coding: UTF-8 -*-

'''A box containing record information from a DMARC XML.'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import src.dmarcfrontlabel as dmfl


class Record(BoxLayout):

    '''A box containing the record information from a DMARC XML.'''

    def __init__(self, **kwargs):
        super(Record, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.var_source_ip = dmfl.DmarcFrontLabel(text='Source IP')
        self.var_count = dmfl.DmarcFrontLabel(text='Count')
        self.var_disposition = dmfl.DmarcFrontLabel(text='Disposition')
        self.var_dkim = dmfl.DmarcFrontLabel(text='DKIM')
        self.var_spf = dmfl.DmarcFrontLabel(text='SPF')
        self.var_header_from = dmfl.DmarcFrontLabel(text='Header From')
        self.var_dkim_domain = dmfl.DmarcFrontLabel(text='Domain')
        self.var_dkim_result = dmfl.DmarcFrontLabel(text='Result')
        self.var_spf_domain = dmfl.DmarcFrontLabel(text='Domain')
        self.var_spf_result = dmfl.DmarcFrontLabel(text='Result')

        self.initialize()

    def initialize(self):
        '''Initializes all the widgets.'''
        self.add_widget(Label(text='[b]Record[/b]', markup=True,
                              font_size='25sp'))
        self.add_widget(Label(text='[b]Row[/b]', markup=True,
                              font_size='20sp'))
        self.add_widget(self.var_source_ip)
        self.add_widget(self.var_count)
        self.add_widget(Label(text='[b]Policy Evaluated[/b]', markup=True,
                              font_size='20sp'))
        self.add_widget(self.var_disposition)
        self.add_widget(self.var_dkim)
        self.add_widget(self.var_spf)
        self.add_widget(Label(text='[b]Identifiers[/b]', markup=True,
                              font_size='20sp'))
        self.add_widget(self.var_header_from)
        self.add_widget(Label(text='[b]Auth Results[/b]', markup=True,
                              font_size='20sp'))
        self.add_widget(Label(text='[b]DKIM[/b]', markup=True,
                              font_size='15sp'))
        self.add_widget(self.var_dkim_domain)
        self.add_widget(self.var_dkim_result)
        self.add_widget(Label(text='[b]SPF[/b]', markup=True,
                              font_size='15sp'))
        self.add_widget(self.var_spf_domain)
        self.add_widget(self.var_spf_result)
