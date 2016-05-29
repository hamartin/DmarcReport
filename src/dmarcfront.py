# -*- coding: UTF-8 -*-

'''The Dmarc Report front.'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import src.config as cnf
import src.record as record
import src.policy as policy
import src.report as report


class DmarcReportFront(BoxLayout):

    '''The grid which header, report, policy and record "frames" are
    placed within.'''

    def __init__(self, **kwargs):
        super(DmarcReportFront, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10

        self.header_box = DmarcReportHeader(size_hint=(1, .15))
        self.add_widget(self.header_box)
        self.center_box = DmarcReportCenter(size_hint=(1, .80))
        self.add_widget(self.center_box)
        # TODO: Add divider bar here!
        self.footer_box = DmarcReportFooter(size_hint=(1, .05))
        self.add_widget(self.footer_box)

    def set_footer_message(self, text=''):
        '''Sets the footer message.'''
        self.footer_box.set_value(text=text)


class DmarcReportHeader(Label):

    '''The DmarcReportFront header.'''

    def __init__(self, **kwargs):
        super(DmarcReportHeader, self).__init__(**kwargs)
        self.text = '[b]' + cnf.PROGRAM_NAME + '[/b]'
        self.markup = True
        self.font_size = '30sp'
        self.size = self.texture_size


class DmarcReportCenter(BoxLayout):

    '''The DmarcReportFront center.'''

    def __init__(self, **kwargs):
        super(DmarcReportCenter, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        self.record = record.Record()
        self.add_widget(self.record)
        self.policy = policy.Policy()
        self.add_widget(self.policy)
        self.report = report.Report()
        self.add_widget(self.report)


class DmarcReportFooter(Label):

    '''The DmarcReportFront footer.'''

    def __init__(self, **kwargs):
        super(DmarcReportFooter, self).__init__(**kwargs)
        self.text = '# TODO: Add footer stuff here!'

    def set_value(self, text=''):
        '''Sets the text shown in the footer.'''
        self.markup = True
        self.text = cnf.COLOR1BEGIN + text + cnf.COLORSTOP
