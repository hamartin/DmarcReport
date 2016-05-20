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

        self.header_box = DmarcReportHeader()
        self.add_widget(self.header_box)
        self.center_box = DmarcReportCenter()
        self.add_widget(self.center_box)
        self.footer_box = DmarcReportFooter()
        self.add_widget(self.footer_box)


class DmarcReportHeader(Label):

    '''The DmarcReportFront header.'''

    def __init__(self, **kwargs):
        super(DmarcReportHeader, self).__init__(**kwargs)
        self.text = cnf.PROGRAM_NAME


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
