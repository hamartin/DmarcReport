# -*- coding: latin-1 -*-

''' A simple Tkinter graphical user interface for reading DMARC XML files. '''

import re
import tkFileDialog as tkfd
import Tkinter as tk
import ttk
import src.xmldm as xmldm


class About(tk.Toplevel):

    ''' DmarcReports modal about window. '''

    def __init__(self, master):
        # TODO: I have been trying to make this window completely modal, but is
        # unable to do so. Will keep this TODO here to remember me to fix this
        # at a later time.
        tk.Toplevel.__init__(self, master)
        self.transient(master)
        self.master = master
        self.title('About DmarcReport')

        aboutcontent = '''
            Created by Hans Åge Martinsen
            Email: <hamartin@moshwire.com>
            URL: https://github.com/hamartin/DmarcReport
        '''

        destroy = self.register(self.killwin)
        self.protocol('WM_DELETE_WINDOW', destroy)

        self.fr_body = ttk.Frame(self, padding=5)
        self.fr_body.pack()
        ttk.Label(self.fr_body, text=aboutcontent,
                  padding=(0, 0, 50, 0)).pack()
        self.bu_ok = ttk.Button(self.fr_body, text='OK', command=self.destroy)
        self.bu_ok.focus()
        self.bu_ok.bind('<Return>', self.destroy)
        self.bu_ok.pack()

        self.master.wait_window(self)

    def killwin(self):
        ''' Will destroy the modal window and return focus to master. '''
        self.master.focus_set()
        tk.Toplevel.destroy(self)


class DmarcReport(tk.Tk):

    ''' A simple Tkinter graphical user interface for reading DMARC XML
    files. '''

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('DmarcReport')

        self.menu = Menu(self)
        self.fileopts = {
            'defaultextension': '.xml',
            'filetypes': [
                ('XML files', '.xml'),
                # ('ZIP files', '.zip'),
                ('ALL files', '.*')
                ]
            }
        self.rootxml = None
        self.fr_feedback = None

        self.fr_begin = ttk.Frame(self)
        self.init()

    def init(self):
        ''' Initializes the start screen. '''
        ttk.Button(self.fr_begin, text='Open', command=self.open,
                   padding=10).pack(side=tk.LEFT)
        ttk.Button(self.fr_begin, text='Quit', command=self.quit,
                   padding=10).pack(side=tk.LEFT)
        self.fr_begin.pack()

    def open(self):
        ''' Opens a file dialog which the user can select a file to open. '''
        filename = tkfd.askopenfilename(**self.fileopts)
        if filename and not re.match('^\d+$', filename):
            self.rootxml = xmldm.xmldict(filename)
            self.fr_feedback = Feedback(self.rootxml, self)
            self.fr_begin.pack_forget()
            self.fr_feedback.pack()


class Feedback(ttk.Frame):

    ''' A class that handles DMARC XML files and displays them. '''

    class Report(ttk.Frame):

        ''' Handles report metadata content in DMARC XML files. '''

        def __init__(self, root, master=None):
            ttk.Frame.__init__(self, master)
            self.root = root
            self.master = master
            self.config(padding=10)

            self.name = None
            self.orgname = None
            self.email = None
            self.reportid = None
            self.daterange = None
            self.begin = None
            self.end = None

            for key, val in root.iteritems():
                if key == 'name':
                    self.name = ttk.Label(self, text=val)
                elif key == 'org_name':
                    self.orgname = ttk.Label(self,
                            text='Organization name: {0}'.format(val['value']))
                elif key == 'email':
                    self.email = ttk.Label(self, text='Email: {0}'.format(
                        val['value']))
                elif key == 'report_id':
                    self.reportid = ttk.Label(self,
                                              text='Report ID: {0}'.format(
                                                  val['value']))
                elif key == 'date_range':
                    self.daterange = ttk.Label(self, text=val['name'])
                    self.begin = ttk.Label(self, text='Begin: {0}'.format(
                        val['begin']['value']))
                    self.end = ttk.Label(self, text='End: {0}'.format(
                        val['end']['value']))
                else:
                    print 'dmarcreport::Feedback::Report::init ',
                    print 'Unknown key {0}'.format(key)

            if self.name:
                self.name.pack()
            if self.orgname:
                self.orgname.pack()
            if self.email:
                self.email.pack()
            if self.reportid:
                self.reportid.pack()
            if self.daterange:
                self.daterange.pack()
            if self.begin:
                self.begin.pack()
            if self.end:
                self.end.pack()

    class Policy(ttk.Frame):

        ''' Handles policy published content in DMARC XML files. '''

        def __init__(self, root, master=None):
            ttk.Frame.__init__(self, master)
            self.root = root
            self.master = master
            self.config(padding=10)

            self.name = None
            self.domain = None
            self.adkim = None
            self.aspf = None
            self.p = None
            self.pct = None

            for key, val in root.iteritems():
                if key == 'name':
                    self.name = ttk.Label(self, text=val)
                elif key == 'domain':
                    self.domain = ttk.Label(self, text='Domain: {0}'.format(
                        val['value']))
                elif key == 'adkim':
                    self.adkim = ttk.Label(self, text='Adkim: {0}'.format(
                        val['value']))
                elif key == 'aspf':
                    self.aspf = ttk.Label(self, text='Aspf: {0}'.format(
                        val['value']))
                elif key == 'p':
                    self.p = ttk.Label(self, text='P: {0}'.format(
                        val['value']))
                elif key == 'pct':
                    self.pct = ttk.Label(self, text='Pct: {0}'.format(
                        val['value']))
                else:
                    print 'dmarcreport::Feedback::Policy::init ',
                    print 'Unknown key {0}'.format(key)

            if self.name:
                self.name.pack()
            if self.domain:
                self.domain.pack()
            if self.adkim:
                self.adkim.pack()
            if self.aspf:
                self.aspf.pack()
            if self.p:
                self.p.pack()
            if self.pct:
                self.pct.pack()

    class Record(ttk.Frame):

        ''' Handles record content in DMARC XML files. '''

        def __init__(self, root, master=None):
            ttk.Frame.__init__(self, master)
            self.root = root
            self.master = master
            self.config(padding=10)

    def __init__(self, root, master=None):
        ttk.Frame.__init__(self, master)
        self.root = root
        self.master = master
        self.config(padding=10)

        self.name = None
        self.report = None
        self.policy = None
        self.record = None

        for key, value in root.iteritems():
            if key == 'name':
                self.name = ttk.Label(self, text=value)
            elif key == 'report_metadata':
                self.report = self.Report(value, self)
            elif key == 'policy_published':
                self.policy = self.Policy(value, self)
            elif key == 'record':
                self.record = self.Record(value, self)
            else:
                print 'dmarcreport::Feedback::init ',
                print 'Unknown key {0}'.format(key)

        if self.name:
            self.name.pack()
        if self.report:
            self.report.pack(side=tk.LEFT)
        if self.policy:
            self.policy.pack(side=tk.LEFT)
        if self.record:
            self.record.pack(side=tk.LEFT)


class Menu(tk.Menu):

    ''' DmarcReports menu bar. '''

    def __init__(self, master=None):
        tk.Menu.__init__(self, master)
        self.master = master

        self.me_file = tk.Menu(self, tearoff=0)
        self.me_about = tk.Menu(self, tearoff=0)

        self.init()

    def init(self):
        ''' Initializes the menu bar. '''
        self.me_file.add_command(label='Open', command=self.master.open)
        self.me_file.add_separator()
        self.me_file.add_command(label='Quit', command=self.quit)
        self.add_cascade(label='File', menu=self.me_file)
        self.me_about.add_command(label='About', command=self.about)
        self.add_cascade(label='Help', menu=self.me_about)
        self.master.config(menu=self)

    def about(self):
        ''' Will display a modal window with information about. '''
        About(self.master)
