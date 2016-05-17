# -*- coding: UTF-8 -*-

'''Policy part of DMARC.'''

import Tkinter as tk

import src.subclassed as sc


class Policy(sc.DmParserFrame):

    '''Policy frame.'''

    def __init__(self, root, **kwargs):
        sc.DmParserFrame.__init__(self, root, **kwargs)
        self.config(bd=10, relief=tk.FLAT, bg='white')
        tk.Label(self, text='Policy', bg='green', pady=24, padx=24,
                 font=('courier', 24, 'bold')).pack()

        self.initialize()

    def initialize(self):
        '''Initializes the widgets used in policy.'''
        self.label_domain = sc.LabelFrame(self, 'Domain')
        self.label_domain.pack(anchor=tk.W)
        self.label_adkim = sc.LabelFrame(self, 'Adkim')
        self.label_adkim.pack(anchor=tk.W)
        self.label_aspf = sc.LabelFrame(self, 'Aspf')
        self.label_aspf.pack(anchor=tk.W)
        self.label_p = sc.LabelFrame(self, 'P')
        self.label_p.pack(anchor=tk.W)
        self.label_pct = sc.LabelFrame(self, 'Pct')
        self.label_pct.pack(anchor=tk.W)
