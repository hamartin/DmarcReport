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
        pad = 10
        tk.Label(self, text='Row', pady=pad, padx=pad,
                 font=('courier', 18, 'bold')).pack(anchor=tk.W)
        self.label_sourceip = sc.LabelFrame(self, 'Source IP')
        self.label_sourceip.pack(anchor=tk.W)
        self.label_count = sc.LabelFrame(self, 'Count')
        self.label_count.pack(anchor=tk.W)
        tk.Label(self, text='Policy Evaluated', pady=pad, padx=pad,
                 font=('courier', 16, 'bold')).pack(anchor=tk.W)
        self.label_disposition = sc.LabelFrame(self, 'Disposition')
        self.label_disposition.pack(anchor=tk.W)
        self.label_ddkim = sc.LabelFrame(self, 'DKIM')
        self.label_ddkim.pack(anchor=tk.W)
        self.label_dspf = sc.LabelFrame(self, 'SPF')
        self.label_dspf.pack(anchor=tk.W)
        tk.Label(self, text='Identifiers', pady=pad, padx=pad,
                 font=('courier', 18, 'bold')).pack(anchor=tk.W)
        self.label_headerfrom = sc.LabelFrame(self, 'Header from')
        self.label_headerfrom.pack(anchor=tk.W)
        tk.Label(self, text='Auth results', pady=pad, padx=pad,
                 font=('courier', 18, 'bold')).pack(anchor=tk.W)
        tk.Label(self, text='DKIM', pady=pad, padx=pad,
                 font=('courier', 16, 'bold')).pack(anchor=tk.W)
        self.label_adomain = sc.LabelFrame(self, 'Domain')
        self.label_adomain.pack(anchor=tk.W)
        self.label_aresult = sc.LabelFrame(self, 'Result')
        self.label_aresult.pack(anchor=tk.W)
        tk.Label(self, text='SPF', pady=pad, padx=pad,
                 font=('courier', 16, 'bold')).pack(anchor=tk.W)
        self.label_adomain = sc.LabelFrame(self, 'Domain')
        self.label_adomain.pack(anchor=tk.W)
        self.label_result = sc.LabelFrame(self, 'Result')
        self.label_result.pack(anchor=tk.W)
