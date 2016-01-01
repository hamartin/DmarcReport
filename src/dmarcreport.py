# -*- coding: latin-1 -*-

''' A Tkinter GUI for reading DMARC XML files. '''

import datetime
import tkFileDialog as tkfd
import Tkinter as tk
import ttk

import src.xmldm as xml

# CONSTANTS.

# Record
REC_SOURCE_IP = 2
REC_COUNT = 3
REC_DISPOSITION = 5
REC_DKIM = 6
REC_SPF = 7
REC_HEADER_FROM = 9
REC_DKIM_DOMAIN = 12
REC_DKIM_RESULT = 13
REC_SPF_DOMAIN = 15
REC_SPF_RESULT = 16

# Policy Evaluated
POL_DOMAIN = 1
POL_ADKIM = 2
POL_ASPF = 3
POL_P = 4
POL_PCT = 5

# Report Metadata
REP_ORG_NAME = 1
REP_EMAIL = 2
REP_REPORT_ID = 3
REP_BEGIN = 5
REP_END = 6


def unixtimestamptodate(uts):
    ''' Converts unix time stamp to date. '''
    return datetime.datetime.fromtimestamp(int(uts)).strftime("%d.%m.%Y")


class About(tk.Toplevel):

    ''' A class to display information about the developer. '''

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.title('About Dmarc Report')

        self.transient(master)
        killwrapper = self.register(self.kill)
        self.protocol('WM_DELETE_WINDOW', killwrapper)

        aboutcontent = '''
            Created by Hans Åge Martinsen
            Email: <hamartin@moshwire.com>
            URL: https://github.com/hamartin/DmarcReport
        '''

        self.fr_main = ttk.Frame(self)
        self.fr_main.pack()
        ttk.Label(self.fr_main, text=aboutcontent,
                  padding=(0, 0, 50, 0)).pack()
        self.bu_ok = ttk.Button(self.fr_main, text='OK', command=killwrapper)
        self.bu_ok.focus()
        self.bu_ok.bind('<Return>', killwrapper)
        self.bu_ok.pack()

        master.wait_window(self)

    def kill(self):
        ''' Destroys the current modal window and returns focus to master. '''
        self.master.focus_set()
        tk.Toplevel.destroy(self)


class DmarcReport(tk.Tk):

    ''' A Tkinter GUI for reading DMARC XML files. '''

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Dmarc Report')

        self.menu = Menu(self)
        self.gui = ttk.Style()
        self.fileopts = {
            'defaultextension': '.xml',
            'filetypes': [
                ('XML files', '.xml'),
                ('ZIP files', '.zip'),
                ('ALL files', '.*')
            ]
        }

        self.fr_report = None
        self.fr_policy = None
        self.fr_record = None

        self.initgui()
        self.initstatics()

    def initgui(self):
        ''' Initiates the styling. '''
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(4, weight=1)

        gui = self.gui
        gui.configure('H1.TLabel', padding=30, font=('courier', 30, 'bold'))
        gui.configure('H2.TLabel', padding=24, font=('courier', 24, 'bold'))
        gui.configure('H3.TLabel', padding=4, font=('courier', 18, 'bold'))
        gui.configure('H4.TLabel', padding=2, font=('courier', 12, 'bold'))

        gui.configure('L1.TLabel', padding=(10, 0, 0, 0), font=('courier', 12))
        gui.configure('L1BOLD.TLabel', padding=(10, 0, 0, 0),
                      font=('courier', 12, 'bold'))
        gui.configure('L2.TLabel', padding=(20, 0, 0, 0), font=('courier', 12))

    def initstatics(self):
        ''' Initiates static widgets. '''
        # Frames.
        self.fr_record = rec = ttk.Frame(self)
        self.fr_record.grid(row=1, column=0, sticky=tk.N)
        ttk.Frame(self, width=50).grid(row=1, column=1)
        self.fr_policy = pol = ttk.Frame(self)
        self.fr_policy.grid(row=1, column=2, sticky=tk.N)
        ttk.Frame(self, width=50).grid(row=1, column=3)
        self.fr_report = rep = ttk.Frame(self)
        self.fr_report.grid(row=1, column=4, sticky=tk.N)
        ttk.Frame(self, height=20).grid(row=2, column=0, columnspan=6)

        # Headers.
        ttk.Label(self, text='Feedback',
                  style='H1.TLabel').grid(row=0, column=0, columnspan=6)
        ttk.Label(rec, text='Record',
                  style='H2.TLabel').grid(row=0, column=0, columnspan=2)
        ttk.Label(pol, text='Policy Published',
                  style='H2.TLabel').grid(row=0, column=0, columnspan=2)
        ttk.Label(rep, text='Report Metadata',
                  style='H2.TLabel').grid(row=0, column=0, columnspan=2)

        # Record.
        ttk.Label(rec, text='Row',
                  style='H3.TLabel').grid(row=1, column=0, sticky=tk.W)
        ttk.Label(rec, text='Source IP',
                  style='L1.TLabel').grid(row=REC_SOURCE_IP, column=0,
                                          sticky=tk.W)
        ttk.Label(rec, text='Count',
                  style='L1.TLabel').grid(row=REC_COUNT, column=0, sticky=tk.W)
        ttk.Label(rec, text='Policy Evaluated',
                  style='L1BOLD.TLabel').grid(row=4, column=0, sticky=tk.W)
        ttk.Label(rec, text='Disposition',
                  style='L2.TLabel').grid(row=REC_DISPOSITION, column=0,
                                          sticky=tk.W)
        ttk.Label(rec, text='DKIM',
                  style='L2.TLabel').grid(row=REC_DKIM, column=0, sticky=tk.W)
        ttk.Label(rec, text='SPF',
                  style='L2.TLabel').grid(row=REC_SPF, column=0, sticky=tk.W)
        ttk.Label(rec, text='Identifiers',
                  style='H3.TLabel').grid(row=8, column=0, sticky=tk.W)
        ttk.Label(rec, text='Header From',
                  style='L1.TLabel').grid(row=REC_HEADER_FROM, column=0,
                                          sticky=tk.W)
        ttk.Label(rec, text='Auth Results',
                  style='H3.TLabel').grid(row=10, column=0, sticky=tk.W)
        ttk.Label(rec, text='DKIM',
                  style='L1BOLD.TLabel').grid(row=11, column=0, sticky=tk.W)
        ttk.Label(rec, text='Domain',
                  style='L2.TLabel').grid(row=REC_DKIM_DOMAIN, column=0,
                                          sticky=tk.W)
        ttk.Label(rec, text='Result',
                  style='L2.TLabel').grid(row=REC_DKIM_RESULT, column=0,
                                          sticky=tk.W)
        ttk.Label(rec, text='SPF',
                  style='L1BOLD.TLabel').grid(row=14, column=0, sticky=tk.W)
        ttk.Label(rec, text='Domain',
                  style='L2.TLabel').grid(row=REC_SPF_DOMAIN, column=0,
                                          sticky=tk.W)
        ttk.Label(rec, text='Result',
                  style='L2.TLabel').grid(row=REC_SPF_RESULT, column=0,
                                          sticky=tk.W)

        # Policy Published.
        ttk.Label(pol, text='Domain',
                  style='L1.TLabel').grid(row=POL_DOMAIN, column=0,
                                          sticky=tk.W)
        ttk.Label(pol, text='Adkim',
                  style='L1.TLabel').grid(row=POL_ADKIM, column=0, sticky=tk.W)
        ttk.Label(pol, text='Aspf',
                  style='L1.TLabel').grid(row=POL_ASPF, column=0, sticky=tk.W)
        ttk.Label(pol, text='P',
                  style='L1.TLabel').grid(row=POL_P, column=0, sticky=tk.W)
        ttk.Label(pol, text='Pct',
                  style='L1.TLabel').grid(row=POL_PCT, column=0, sticky=tk.W)

        # Report metadata.
        ttk.Label(rep, text='Org Name',
                  style='L1.TLabel').grid(row=REP_ORG_NAME, column=0,
                                          sticky=tk.W)
        ttk.Label(rep, text='Email',
                  style='L1.TLabel').grid(row=REP_EMAIL, column=0, sticky=tk.W)
        ttk.Label(rep, text='Report ID',
                  style='L1.TLabel').grid(row=REP_REPORT_ID, column=0,
                                          sticky=tk.W)
        ttk.Label(rep, text='Date Range',
                  style='L1BOLD.TLabel').grid(row=4, column=0, sticky=tk.W)
        ttk.Label(rep, text='Begin',
                  style='L2.TLabel').grid(row=REP_BEGIN, column=0, sticky=tk.W)
        ttk.Label(rep, text='End',
                  style='L2.TLabel').grid(row=REP_END, column=0, sticky=tk.W)

    def open(self):
        ''' Opens a file dialog which the user can select a file to open. '''
        filename = tkfd.askopenfilename(**self.fileopts)
        if filename:
            if self.fr_record:
                self.fr_record.destroy()
            if self.fr_report:
                self.fr_report.destroy()
            if self.fr_policy:
                self.fr_policy.destroy()
            self.initstatics()

            self.parsedictionary(xml.xmldict(filename))

    def parsedictionary(self, dic):
        ''' Iterates over the dictionary and creates labels where they are
        supposed to be if the method finds a match. '''
        for key, val in dic.iteritems():
            if key == 'record':
                self.parserecord(val)
            elif key == 'policy_published':
                self.parsepolicy(val)
            elif key == 'report_metadata':
                self.parsereport(val)

    def parsepolicy(self, dic):
        ''' Parses the policy published part of the xml dictionary. '''
        for key, val in dic.iteritems():
            res = None

            if key == 'adkim':
                res = POL_ADKIM
            elif key == 'domain':
                res = POL_DOMAIN
            elif key == 'aspf':
                res = POL_ASPF
            elif key == 'pct':
                res = POL_PCT
            elif key == 'p':
                res = POL_P

            if res:
                ttk.Label(self.fr_policy, text=val).grid(row=res, column=1)

    def parserecord(self, dic):
        ''' Parses the record part of the xml dictionary. '''
        for key, val in dic.iteritems():
            res = None
            value = None

            if key == 'identifiers':
                if 'header_from' in val:
                    value = val['header_from']
                    res = REC_HEADER_FROM
            elif key == 'auth_results':
                self.parseauthresults(val)
            elif key == 'row':
                self.parserow(val)

            if res and value:
                ttk.Label(self.fr_record, text=value).grid(row=res, column=1)
            elif res:
                ttk.Label(self.fr_record, text=val).grid(row=res, column=1)

    def parsereport(self, dic):
        ''' Parses the report part of the xml dictionary. '''
        for key, val in dic.iteritems():
            res = None
            if key == 'org_name':
                res = REP_ORG_NAME
            elif key == 'email':
                res = REP_EMAIL
            elif key == 'report_id':
                res = REP_REPORT_ID
            elif key == 'date_range':
                dummy = ttk.Label(self.fr_report,
                                  text=unixtimestamptodate(val['begin']))
                dummy.grid(row=REP_BEGIN, column=1)
                dummy = ttk.Label(self.fr_report,
                                  text=unixtimestamptodate(val['end']))
                dummy.grid(row=REP_END, column=1)

            if res:
                ttk.Label(self.fr_report, text=val).grid(row=res, column=1)

    def parseauthresults(self, dic):
        ''' Parses the auth results part of record xml dictionary. '''
        for key, val in dic.iteritems():
            if key == 'dkim':
                ttk.Label(self.fr_record,
                          text=val['domain']).grid(row=REC_DKIM_DOMAIN,
                                                   column=1)
                ttk.Label(self.fr_record,
                          text=val['result']).grid(row=REC_DKIM_RESULT,
                                                   column=1)
            elif key == 'spf':
                ttk.Label(self.fr_record,
                          text=val['domain']).grid(row=REC_SPF_DOMAIN,
                                                   column=1)
                ttk.Label(self.fr_record,
                          text=val['result']).grid(row=REC_SPF_RESULT,
                                                   column=1)

    def parserow(self, dic):
        ''' Parses the row part of record xml dictionary. '''
        for key, val in dic.iteritems():
            res = None
            if key == 'source_ip':
                res = REC_SOURCE_IP
            elif key == 'count':
                res = REC_COUNT
            elif key == 'policy_evaluated':
                ttk.Label(self.fr_record,
                          text=val['disposition']).grid(row=REC_DISPOSITION,
                                                        column=1)
                ttk.Label(self.fr_record,
                          text=val['dkim']).grid(row=REC_DKIM, column=1)
                ttk.Label(self.fr_record,
                          text=val['spf']).grid(row=REC_SPF, column=1)

            if res:
                ttk.Label(self.fr_record, text=val).grid(row=res, column=1)


class Menu(tk.Menu):

    ''' The menu for this application. '''

    def __init__(self, master):
        tk.Menu.__init__(self, master)
        self.master = master

        self.me_file = tk.Menu(self, tearoff=0)
        self.me_file.add_command(label='Open', command=self.master.open)
        self.me_file.add_separator()
        self.me_file.add_command(label='Quit', command=self.quit)
        self.add_cascade(label='File', menu=self.me_file)
        self.me_about = tk.Menu(self, tearoff=0)
        self.me_about.add_command(label='About', command=self._about)
        self.add_cascade(label='Help', menu=self.me_about)
        self.master.config(menu=self)

    def _about(self):
        ''' Will display a modal window with some information. '''
        About(self.master)
