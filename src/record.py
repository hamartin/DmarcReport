# -*- coding: UTF-8 -*-
# File name: record.py

'''Record part of DMARC.'''

import Tkinter as tk

import src.subclassed as sc


class RecordError(Exception):
    '''Base record error exception.'''
    pass


class Record(sc.DmParserFrame):

    '''Record frame.'''

    def __init__(self, root, **kwargs):
        sc.DmParserFrame.__init__(self, root, **kwargs)
        self.config(bd=10, relief=tk.FLAT)
        tk.Label(self, text='Record', pady=24, padx=24,
                 font=('courier', 24, 'bold')).pack()

        self.initialize()

    def initialize(self):
        '''Initializes the widgets used in record.'''
        pad = self.pad
        tk.Label(self, text='Row',
                 font=('courier', 18, 'bold')).pack(anchor=tk.W)
        self.label_sourceip = sc.LabelFrame(self, 'Source IP')
        self.label_sourceip.pack(padx=(pad, 0))
        self.label_count = sc.LabelFrame(self, 'Count')
        self.label_count.pack(padx=(pad, 0))
        tk.Label(self, text='Policy Evaluated',
                 font=('courier', 16, 'bold')).pack(anchor=tk.W, padx=(pad, 0))
        self.label_disposition = sc.LabelFrame(self, 'Disposition')
        self.label_disposition.pack(padx=(2*pad, 0))
        self.label_ddkim = sc.LabelFrame(self, 'DKIM')
        self.label_ddkim.pack(padx=(2*pad, 0))
        self.label_dspf = sc.LabelFrame(self, 'SPF')
        self.label_dspf.pack(padx=(2*pad, 0))
        tk.Label(self, text='Identifiers',
                 font=('courier', 18, 'bold')).pack(anchor=tk.W)
        self.label_headerfrom = sc.LabelFrame(self, 'Header from')
        self.label_headerfrom.pack(padx=(pad, 0))
        tk.Label(self, text='Auth results',
                 font=('courier', 18, 'bold')).pack(anchor=tk.W)
        tk.Label(self, text='DKIM',
                 font=('courier', 16, 'bold')).pack(anchor=tk.W, padx=(pad, 0))
        self.label_adomain = sc.LabelFrame(self, 'Domain')
        self.label_adomain.pack(padx=(2*pad, 0))
        self.label_aresult = sc.LabelFrame(self, 'Result')
        self.label_aresult.pack(padx=(2*pad, 0))
        tk.Label(self, text='SPF',
                 font=('courier', 16, 'bold')).pack(anchor=tk.W, padx=(pad, 0))
        self.label_aadomain = sc.LabelFrame(self, 'Domain')
        self.label_aadomain.pack(padx=(2*pad, 0))
        self.label_aaresult = sc.LabelFrame(self, 'Result')
        self.label_aaresult.pack(padx=(2*pad, 0))

    def parse_record(self, dic):
        '''Sets values for all record keys in the GUI.'''
        self.label_headerfrom.clear()
        self.label_adomain.clear()
        self.label_aresult.clear()
        self.label_aadomain.clear()
        self.label_aaresult.clear()
        self.label_count.clear()
        self.label_sourceip.clear()
        self.label_dspf.clear()
        self.label_ddkim.clear()
        self.label_disposition.clear()
        for key, val in dic.iteritems():
            if key == 'identifiers':
                if 'header_from' in val:
                    self.label_headerfrom.set_value(val['header_from'])
            elif key == 'auth_results':
                if 'dkim' in val:
                    dkim = val['dkim']
                    if 'domain' in dkim:
                        self.label_adomain.set_value(dkim['domain'])
                    if 'result' in dkim:
                        self.label_aresult.set_value(dkim['result'])
                if 'spf' in val:
                    spf = val['spf']
                    if 'domain' in spf:
                        self.label_aadomain.set_value(spf['domain'])
                    if 'result' in spf:
                        self.label_aaresult.set_value(spf['result'])
            elif key == 'row':
                if 'count' in val:
                    self.label_count.set_value(val['count'])
                if 'source_ip' in val:
                    self.label_sourceip.set_value(val['source_ip'])
                if 'policy_evaluated' in val:
                    peva = val['policy_evaluated']
                    if 'spf' in peva:
                        self.label_dspf.set_value(peva['spf'])
                    if 'dkim' in peva:
                        self.label_ddkim.set_value(peva['dkim'])
                    if 'disposition' in peva:
                        self.label_disposition.set_value(peva['disposition'])
            else:
                raise RecordError('Unknown key {0}!'.format(key))
