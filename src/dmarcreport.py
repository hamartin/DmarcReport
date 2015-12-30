# -*- coding: latin-1 -*-

''' A Tkinter GUI for reading DMARC XML files. '''

import tkFileDialog as tkfd
import Tkinter as tk
import ttk


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
                # TODO: Make ZIP files work.
                # ('ZIP files', '.zip'),
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
        self.record = rec = ttk.Frame(self)
        self.record.grid(row=1, column=0, sticky=tk.N)
        ttk.Frame(self, width=50).grid(row=1, column=1)
        self.policy = pol = ttk.Frame(self)
        self.policy.grid(row=1, column=2, sticky=tk.N)
        ttk.Frame(self, width=50).grid(row=1, column=3)
        self.report = rep = ttk.Frame(self)
        self.report.grid(row=1, column=4, sticky=tk.N)

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
                  style='L1.TLabel').grid(row=2, column=0, sticky=tk.W)
        ttk.Label(rec, text='Count',
                  style='L1.TLabel').grid(row=3, column=0, sticky=tk.W)
        ttk.Label(rec, text='Policy Evaluated',
                  style='L1BOLD.TLabel').grid(row=4, column=0, sticky=tk.W)
        ttk.Label(rec, text='Disposition',
                  style='L2.TLabel').grid(row=5, column=0, sticky=tk.W)
        ttk.Label(rec, text='DKIM',
                  style='L2.TLabel').grid(row=6, column=0, sticky=tk.W)
        ttk.Label(rec, text='SPF',
                  style='L2.TLabel').grid(row=7, column=0, sticky=tk.W)
        ttk.Label(rec, text='Identifiers',
                  style='H3.TLabel').grid(row=8, column=0, sticky=tk.W)
        ttk.Label(rec, text='Header From',
                  style='L1.TLabel').grid(row=9, column=0, sticky=tk.W)
        ttk.Label(rec, text='Auth Results',
                  style='H3.TLabel').grid(row=10, column=0, sticky=tk.W)
        ttk.Label(rec, text='DKIM',
                  style='L1BOLD.TLabel').grid(row=11, column=0, sticky=tk.W)
        ttk.Label(rec, text='Domain',
                  style='L2.TLabel').grid(row=12, column=0, sticky=tk.W)
        ttk.Label(rec, text='Result',
                  style='L2.TLabel').grid(row=13, column=0, sticky=tk.W)
        ttk.Label(rec, text='SPF',
                  style='L1BOLD.TLabel').grid(row=14, column=0, sticky=tk.W)
        ttk.Label(rec, text='Domain',
                  style='L2.TLabel').grid(row=15, column=0, sticky=tk.W)
        ttk.Label(rec, text='Result',
                  style='L2.TLabel').grid(row=16, column=0, sticky=tk.W)

        # Policy Published.
        ttk.Label(pol, text='Domain',
                  style='L1.TLabel').grid(row=1, column=0, sticky=tk.W)
        ttk.Label(pol, text='Adkim',
                  style='L1.TLabel').grid(row=2, column=0, sticky=tk.W)
        ttk.Label(pol, text='Aspf',
                  style='L1.TLabel').grid(row=3, column=0, sticky=tk.W)
        ttk.Label(pol, text='P',
                  style='L1.TLabel').grid(row=4, column=0, sticky=tk.W)
        ttk.Label(pol, text='Pct',
                  style='L1.TLabel').grid(row=5, column=0, sticky=tk.W)

        # Report metadata.
        ttk.Label(rep, text='Org Name',
                  style='L1.TLabel').grid(row=1, column=0, sticky=tk.W)
        ttk.Label(rep, text='Email',
                  style='L1.TLabel').grid(row=2, column=0, sticky=tk.W)
        ttk.Label(rep, text='Report ID',
                  style='L1.TLabel').grid(row=3, column=0, sticky=tk.W)
        ttk.Label(rep, text='Date Range',
                  style='L1BOLD.TLabel').grid(row=4, column=0, sticky=tk.W)
        ttk.Label(rep, text='Begin',
                  style='L2.TLabel').grid(row=5, column=0, sticky=tk.W)
        ttk.Label(rep, text='End',
                  style='L2.TLabel').grid(row=6, column=0, sticky=tk.W)

        # TEST
        ttk.Label(rec, text='test').grid(row=1, column=1)
        ttk.Label(pol, text='test').grid(row=1, column=1)
        ttk.Label(rep, text='test').grid(row=1, column=1)

    def open(self):
        ''' Opens a file dialog which the user can select a file to open. '''
        filename = tkfd.askopenfilename(**self.fileopts)
        if filename:
            # TODO Do something with the filename.
            pass


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
