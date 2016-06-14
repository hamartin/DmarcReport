# -*- coding: UTF-8 -*-
# File name: dmarcreport.py

'''
Dmarc Report module.

Copyright 2016, Hans Åge Martinsen <hamartin@moshwire.com>

    This file is part of Dmarc Report.

    Dmarc Report is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Dmarc Report is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Dmarc Report.  If not, see <http://www.gnu.org/licenses/>
'''

import kivy
kivy.require('1.9.1')

import os

from datetime import datetime
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from src import config as cnf
from src.exceptions import ModelFileError
from src.model import Model


class DmarcReport(App):

    '''Dmarc Report.'''

    title = 'Dmarc Report'

    def build(self):
        '''Builds the NUI.'''
        return DmarcReportNui()


class DmarcReportNui(FloatLayout):

    '''Dmarc Report NUI.'''

    model = ObjectProperty(Model())


class ImageButton(ButtonBehavior, Image):

    '''Kivy button with image instead of label.'''

    body = ObjectProperty()
    footer = ObjectProperty()
    model = ObjectProperty()

    reportb = ObjectProperty()
    recordb = ObjectProperty()
    policyb = ObjectProperty()

    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_motion)
        self.source = cnf.IMAGENORMAL
        self.popup = None

        for key, val in kwargs.iteritems():
            if key == 'source':
                self.source = val

    def on_motion(self, etype, motionevent):
        '''When mouse is above image, change picture.'''
        if etype and motionevent:
            if self.collide_point(Window.mouse_pos[0], Window.mouse_pos[1]) \
                    and self.source != cnf.IMAGEOVER:
                self.source = cnf.IMAGEOVER
                self.footer.text = 'Open file…'
            elif(not self.collide_point(Window.mouse_pos[0],
                                        Window.mouse_pos[1]) and
                 self.source != cnf.IMAGENORMAL):
                self.source = cnf.IMAGENORMAL
                self.footer.text = ''

    def openfile(self):
        '''Creates a popup window where a file to open can be chosen.'''
        content = OpenFile(footer=self.footer, reportb=self.reportb,
                           recordb=self.recordb, policyb=self.policyb,
                           body=self.body)
        self.popup = Popup(title='Open file', content=content,
                           size_hint=(.8, .8))
        content.popup = self.popup
        content.model = self.model
        self.popup.open()


class OpenFile(BoxLayout):

    '''Open file popup window.'''

    body = ObjectProperty()
    footer = ObjectProperty()
    model = ObjectProperty()
    popup = ObjectProperty()

    reportb = ObjectProperty()
    recordb = ObjectProperty()
    policyb = ObjectProperty()

    def dismiss(self):
        '''Dismisses the popup we're in.'''
        self.popup.dismiss()

    def load(self, filename):
        '''Loads the file given to it.'''
        if filename:
            filename = filename[0]
        else:
            return

        try:
            self.model.load(filename)
        except ModelFileError as err:
            self.reportb.disabled = True
            self.recordb.disabled = True
            self.policyb.disabled = True
            self.body.bodydata.clear_widgets()
            self.footer.text = 'Error! {0}'.format(err.message)
        else:
            self.reportb.disabled = False
            self.recordb.disabled = False
            self.policyb.disabled = False
            self.body.reload('report', force=True)
            self.footer.text = 'File opened: {0}'.format(filename)
            self.dismiss()


class Body(BoxLayout):

    '''Dmarc Report body.'''

    bodydata = ObjectProperty()
    model = ObjectProperty()
    footer = ObjectProperty()

    def __init__(self, **kwargs):
        # super(Body, self).__init__(**kwargs)
        BoxLayout.__init__(self, **kwargs)

        self.loaded = ''

    def reload(self, group, force=False):
        '''Reloads the group widgets if group not the same as loaded.'''
        if force is False and group == self.loaded:
            return
        else:
            self.loaded = group

        self.bodydata.clear_widgets()

        if group == 'report':
            self.bodydata.add_widget(Report(model=self.model))
            self.footer.text = 'Showing Report Metadata group…'
        elif group == 'record':
            self.bodydata.add_widget(Record(model=self.model))
            self.footer.text = 'Showing Record group…'
        else:
            self.bodydata.add_widget(Policy(model=self.model))
            self.footer.text = 'Showing Policy Reported group…'


class Groups(BoxLayout):

    '''Dmarc Report groups.'''

    def __init__(self, **kwargs):
        # super(Groups, self).__init__(**kwargs)
        BoxLayout.__init__(self, **kwargs)
        self.size_hint_y = .9
        self.orientation = 'vertical'

        self.model = None
        if 'model' in kwargs:
            self.model = kwargs['model']


class Record(Groups):

    '''Dmarc Report Record group.'''

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
        # super(Record, self).__init__(**kwargs)
        Groups.__init__(self, **kwargs)

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


class Report(Groups):

    '''Dmarc Report Report group.'''

    rep_orgname = StringProperty()
    rep_email = StringProperty()
    rep_reportid = StringProperty()
    rep_begin = StringProperty()
    rep_end = StringProperty()

    def __init__(self, **kwargs):
        # super(Report, self).__init__(**kwargs)
        Groups.__init__(self, **kwargs)

        self.rep_begin = get_time_value(self.model.get_rep('begin',
                                                           'date_range'))
        self.rep_end = get_time_value(self.model.get_rep('end', 'date_range'))
        self.rep_reportid = self.model.get_rep('report_id')
        self.rep_orgname = self.model.get_rep('org_name')
        self.rep_email = self.model.get_rep('email')


class Policy(Groups):

    '''Dmarc Report Policy group.'''

    pol_p = StringProperty()
    pol_sp = StringProperty()
    pol_pct = StringProperty()
    pol_aspf = StringProperty()
    pol_adkim = StringProperty()
    pol_domain = StringProperty()

    def __init__(self, **kwargs):
        # super(Policy, self).__init__(**kwargs)
        Groups.__init__(self, **kwargs)

        self.pol_domain = self.model.get_pol('domain')
        self.pol_adkim = self.model.get_pol('adkim')
        self.pol_aspf = self.model.get_pol('aspf')
        self.pol_pct = self.model.get_pol('pct')
        self.pol_sp = self.model.get_pol('sp')
        self.pol_p = self.model.get_pol('p')


Builder.load_file(os.path.join(os.path.dirname(__file__), cnf.KV_DIRECTORY,
                               'dmarcreport.kv'))


def get_time_value(timestamp):
    '''Convert the timestamp into a time and date.'''
    return datetime.fromtimestamp(int(timestamp)).strftime('%d.%m.%Y')
