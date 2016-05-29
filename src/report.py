# -*- coding: UTF-8 -*-

'''A box containing report information from a DMARC XML.'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import src.dmarcfrontlabel as dmfl


class Report(BoxLayout):

    '''A box containing the report information from a DMARC XML.'''

    def __init__(self, **kwargs):
        super(Report, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.var_org_name = dmfl.DmarcFrontLabel(text='Org Name')
        self.var_email = dmfl.DmarcFrontLabel(text='Email')
        self.var_report_id = dmfl.DmarcFrontLabel(text='Report ID')
        self.var_begin = dmfl.DmarcFrontLabel(text='Begin')
        self.var_end = dmfl.DmarcFrontLabel(text='End')

        self.initialize()

    def initialize(self):
        '''Initializes all the widgets.'''
        self.add_widget(Label(text='[b]Report Metadata[/b]', markup=True,
                        font_size='25sp'))
        self.add_widget(self.var_org_name)
        self.add_widget(self.var_email)
        self.add_widget(self.var_report_id)
        self.add_widget(Label(text='[b]Date Range[/b]', markup=True,
                        font_size='15sp'))
        self.add_widget(self.var_begin)
        self.add_widget(self.var_end)
