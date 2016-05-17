# -*- coding: UTF-8 -*-

'''Report part of DMARC.'''

import Tkinter as tk

import src.subclassed as sc


class Report(sc.DmParserFrame):

    '''Report frame.'''

    def __init__(self, root, **kwargs):
        sc.DmParserFrame.__init__(self, root, **kwargs)
        self.config(bd=10, relief=tk.FLAT, bg='yellow')
        tk.Label(self, text='Report', bg='pink', pady=24, padx=24,
                 font=('courier', 24, 'bold')).pack()

        self.initialize()

    def initialize(self):
        '''Initializes the widgets used in report.'''
        self.label_orgname = sc.LabelFrame(self, 'Org name')
        self.label_orgname.pack(anchor=tk.W)
        self.label_email = sc.LabelFrame(self, 'Email')
        self.label_email.pack(anchor=tk.W)
        self.label_reportid = sc.LabelFrame(self, 'Report ID')
        self.label_reportid.pack(anchor=tk.W)
        tk.Label(self, text='Date range').pack(anchor=tk.W)
        self.label_begin = sc.LabelFrame(self, 'Begin')
        self.label_begin.pack(anchor=tk.W)
        self.label_end = sc.LabelFrame(self, 'End')
        self.label_end.pack(anchor=tk.W)
