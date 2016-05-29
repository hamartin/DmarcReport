# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''Dmarc Report module.'''

import kivy
kivy.require('1.9.1')

from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout

from src import config as cnf
from src.exceptions import ModelError
from src.model import Model

Builder.load_file('{0}/dmarcreport.kv'.format(cnf.KV_DIRECTORY))


class DmarcReport(App):

    '''Dmarc Report.'''

    title = 'Dmarc Report'

    def build(self):
        '''Builds the NUI.'''
        return DmarcReportNui()


class DmarcReportNui(FloatLayout):

    '''Dmarc Report NUI.'''

    # Model
    model = ObjectProperty()

    # Policy.
    pol_p = StringProperty()
    pol_sp = StringProperty()
    pol_pct = StringProperty()
    pol_aspf = StringProperty()
    pol_adkim = StringProperty()
    pol_domain = StringProperty()

    # Report metadata.
    rep_orgname = StringProperty()
    rep_email = StringProperty()
    rep_reportid = StringProperty()
    rep_begin = StringProperty()
    rep_end = StringProperty()

    # Record.
    rec_sourceip = StringProperty()
    rec_count = StringProperty()
    rec_disposition = StringProperty()
    rec_ddkim = StringProperty()
    rec_dspf = StringProperty()
    rec_headerfrom = StringProperty()
    rec_aspfdomain = StringProperty()
    rec_aspfresult = StringProperty()
    rec_adkimdomain = StringProperty()
    rec_adkimresult = StringProperty()

    def __init__(self, **kwargs):
        # super(DmarcReportNui, self).__init__(**kwargs)
        FloatLayout.__init__(self, **kwargs)

        self.model = Model()
        self.reset_labels()

    def reset_labels(self):
        '''Resets all the labels to N/A.'''
        # Policy.
        self.pol_domain = 'N/A'
        self.pol_adkim = 'N/A'
        self.pol_aspf = 'N/A'
        self.pol_pct = 'N/A'
        self.pol_sp = 'N/A'
        self.pol_p = 'N/A'

        # Report metadata.
        self.rep_orgname = 'N/A'
        self.rep_email = 'N/A'
        self.rep_reportid = 'N/A'
        self.rep_begin = 'N/A'
        self.rep_end = 'N/A'

        # Record.
        self.rec_sourceip = 'N/A'
        self.rec_count = 'N/A'
        self.rec_disposition = 'N/A'
        self.rec_ddkim = 'N/A'
        self.rec_dspf = 'N/A'
        self.rec_headerfrom = 'N/A'
        self.rec_aspfdomain = 'N/A'
        self.rec_aspfresult = 'N/A'
        self.rec_adkimdomain = 'N/A'
        self.rec_adkimresult = 'N/A'

    def load(self, path, sel):
        '''Loads the selected file stored in path.'''
        self.reset_labels()
        if path and sel:
            try:
                self.model.load(sel[0])
            except ModelError:
                return False
            else:
                self.set_policy_labels()
                self.set_report_labels()
                self.set_record_labels()
                return True
        else:
            return False

    def set_policy_labels(self):
        '''Sets policy labels in the NUI using model data.'''
        self.pol_domain = self.model.get_pol('domain')
        self.pol_adkim = self.model.get_pol('adkim')
        self.pol_aspf = self.model.get_pol('aspf')
        self.pol_pct = self.model.get_pol('pct')
        self.pol_sp = self.model.get_pol('sp')
        self.pol_p = self.model.get_pol('p')

    def set_report_labels(self):
        '''Sets report labels in the NUI using model data.'''
        self.rep_begin = get_time_value(self.model.get_rep('begin',
                                                           'date_range'))
        self.rep_end = get_time_value(self.model.get_rep('end', 'date_range'))
        self.rep_reportid = self.model.get_rep('report_id')
        self.rep_orgname = self.model.get_rep('org_name')
        self.rep_email = self.model.get_rep('email')

    def set_record_labels(self):
        '''Sets record labels in the NUI using model data.'''
        self.rec_sourceip = self.model.get_rec('source_ip', 'row')
        self.rec_count = self.model.get_rec('count', 'row')
        self.rec_disposition = self.model.get_rec('disposition', 'row',
                                                  'policy_evaluated')
        self.rec_ddkim = self.model.get_rec('dkim', 'row', 'policy_evaluated')
        self.rec_dspf = self.model.get_rec('spf', 'row', 'policy_evaluated')
        self.rec_headerfrom = self.model.get_rec('header_from', 'identifiers')
        self.rec_aspfdomain = self.model.get_rec('domain', 'auth_results',
                                                 'spf')
        self.rec_aspfresult = self.model.get_rec('result', 'auth_results',
                                                 'spf')
        self.rec_adkimdomain = self.model.get_rec('domain', 'auth_results',
                                                  'dkim')
        self.rec_adkimresult = self.model.get_rec('result', 'auth_results',
                                                  'dkim')


def get_time_value(timestamp):
    '''Convert the timestamp into a time and date.'''
    return datetime.fromtimestamp(int(timestamp)).strftime('%d.%m.%Y')
