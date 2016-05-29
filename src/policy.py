# -*- coding: UTF-8 -*-

'''Policy part of DMARC.'''

import Tkinter as tk

import src.subclassed as sc


class PolicyError(Exception):
    '''Base policy error exception.'''
    pass


class Policy(sc.DmParserFrame):

    '''Policy frame.'''

    def __init__(self, root, **kwargs):
        sc.DmParserFrame.__init__(self, root, **kwargs)
        self.config(bd=10, relief=tk.FLAT)
        tk.Label(self, text='Policy Published', pady=24, padx=24,
                 font=('courier', 24, 'bold')).pack()

        self.initialize()

    def initialize(self):
        '''Initializes the widgets used in policy.'''
        self.label_domain = sc.LabelFrame(self, 'Domain')
        self.label_domain.pack()
        self.label_adkim = sc.LabelFrame(self, 'Adkim')
        self.label_adkim.pack()
        self.label_aspf = sc.LabelFrame(self, 'Aspf')
        self.label_aspf.pack()
        self.label_p = sc.LabelFrame(self, 'P')
        self.label_p.pack()
        self.label_sp = sc.LabelFrame(self, 'SP')
        self.label_sp.pack()
        self.label_pct = sc.LabelFrame(self, 'Pct')
        self.label_pct.pack()

    def parse_policy(self, dic):
        '''Sets values for all policy keys in the GUI.'''
        self.label_domain.clear()
        self.label_p.clear()
        self.label_pct.clear()
        self.label_aspf.clear()
        self.label_adkim.clear()
        self.label_sp.clear()
        for key, val in dic.iteritems():
            if key == 'domain':
                self.label_domain.set_value(val)
            elif key == 'p':
                self.label_p.set_value(val)
            elif key == 'pct':
                self.label_pct.set_value(val)
            elif key == 'aspf':
                self.label_aspf.set_value(val)
            elif key == 'adkim':
                self.label_adkim.set_value(val)
            elif key == 'sp':
                self.label_sp.set_value(val)
            else:
                raise PolicyError('Unknown key {0}!'.format(key))
