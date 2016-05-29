# -*- coding: UTF-8 -*-
# File name: report.py

'''Report part of DMARC.'''

import Tkinter as tk

import src.subclassed as sc


class ReportError(Exception):
    '''Base report error exception.'''
    pass


class Report(sc.DmParserFrame):

    '''Report frame.'''

    def __init__(self, root, **kwargs):
        sc.DmParserFrame.__init__(self, root, **kwargs)
        self.config(bd=10, relief=tk.FLAT)
        tk.Label(self, text='Report Metadata', pady=24, padx=24,
                 font=('courier', 24, 'bold')).pack()

        self.initialize()

    def initialize(self):
        '''Initializes the widgets used in report.'''
        pad = self.pad
        self.label_orgname = sc.LabelFrame(self, 'Org name')
        self.label_orgname.pack()
        self.label_email = sc.LabelFrame(self, 'Email')
        self.label_email.pack()
        self.label_reportid = sc.LabelFrame(self, 'Report ID')
        self.label_reportid.pack()
        tk.Label(self, text='Date range',
                 font=('courier', 16, 'bold')).pack(anchor=tk.W)
        self.label_begin = sc.LabelFrame(self, 'Begin')
        self.label_begin.pack(padx=(pad, 0))
        self.label_end = sc.LabelFrame(self, 'End')
        self.label_end.pack(padx=(pad, 0))

    def parse_report(self, dic):
        '''Sets values for all report keys in the GUI.'''
        self.label_orgname.clear()
        self.label_email.clear()
        self.label_reportid.clear()
        self.label_begin.clear()
        self.label_end.clear()
        for key, val in dic.iteritems():
            if key == 'org_name':
                self.label_orgname.set_value(val)
            elif key == 'email':
                self.label_email.set_value(val)
            elif key == 'report_id':
                self.label_reportid.set_value(val)
            elif key == 'date_range':
                self.label_begin.set_time_value(val['begin'])
                self.label_end.set_time_value(val['end'])
            else:
                raise ReportError('Unknown key {0}!'.format(key))
