# -*- coding: UTF-8 -*-

'''Record part of DMARC.'''

import Tkinter as tk

import src.subclassed as sc


class Record(sc.DmParserFrame):

    '''Record frame.'''

    def __init__(self, root, **kwargs):
        sc.DmParserFrame.__init__(self, root, **kwargs)
        self.config(bd=10, relief=tk.FLAT, bg='blue')
        tk.Label(self, text='Record', bg='red', pady=24, padx=24,
                 font=('courier', 24, 'bold')).pack()

        self.initialize()

    def initialize(self):
        '''Initializes the widgets used in record.'''
        self.label_row = sc.LabelFrame(self, 'Row')
        self.label_row.pack()
        self.label_sourceip = sc.LabelFrame(self, 'Source IP')
        self.label_sourceip.pack()
        self.label_count = sc.LabelFrame(self, 'Count')
        self.label_count.pack()
        self.label_policyevaluated = sc.LabelFrame(self, 'Policy Evaluated')
        self.label_policyevaluated.pack()
        self.label_disposition = sc.LabelFrame(self, 'Disposition')
        self.label_disposition.pack()
        self.label_ddkim = sc.LabelFrame(self, 'DKIM')
        self.label_ddkim.pack()
        self.label_dspf = sc.LabelFrame(self, 'SPF')
        self.label_dspf.pack()
        self.label_identifiers = sc.LabelFrame(self, 'Identifiers')
        self.label_identifiers.pack()
        self.label_headerfrom = sc.LabelFrame(self, 'Header from')
        self.label_headerfrom.pack()
        self.label_authresults = sc.LabelFrame(self, 'Auth results')
        self.label_authresults.pack()
        self.label_adkim = sc.LabelFrame(self, 'DKIM')
        self.label_adkim.pack()
        self.label_adomain = sc.LabelFrame(self, 'Domain')
        self.label_adomain.pack()
        self.label_aresult = sc.LabelFrame(self, 'Result')
        self.label_aresult.pack()
        self.label_aspf = sc.LabelFrame(self, 'SPF')
        self.label_aspf.pack()
        self.label_adomain = sc.LabelFrame(self, 'Domain')
        self.label_adomain.pack()
        self.label_result = sc.LabelFrame(self, 'Result')
        self.label_result.pack()
