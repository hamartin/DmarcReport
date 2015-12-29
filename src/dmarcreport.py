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

        self.fr_body = ttk.Frame(self)
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

        self.gui = ttk.Style()
        self.initgui()

        self.menu = Menu(self)
        self.fileopts = {
            'defaultextension': '.xml',
            'filetypes': [
                ('XML files', '.xml'),
                # TODO: Make zip files work.
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

    def initgui(self):
        ''' Initializes the styling for widgets. '''
        self.gui.configure('Header.TFrame', padding=20)
        self.gui.configure('Header.TLabel', padding=20, relief=tk.FLAT,
                           font=('courier', 18, 'bold'))
        self.gui.configure('Header2.TFrame', padding=20, relief=tk.RIDGE)
        self.gui.configure('Header2.TLabel', padding=20, relief=tk.FLAT,
                           font=('courier', 13, 'bold'))

    def open(self):
        ''' Opens a file dialog which the user can select a file to open. '''
        filename = tkfd.askopenfilename(**self.fileopts)
        if filename and not re.match(r'^\d+$', filename):
            self.rootxml = xmldm.xmldict(filename)
            self.fr_feedback = Feedback(self.rootxml, self)
            self.fr_begin.pack_forget()
            self.fr_feedback.pack(expand=True, fill=tk.BOTH)


class Feedback(ttk.Frame):

    ''' Creates a frame with widgets. '''

    def __init__(self, root, master=None):
        ttk.Frame.__init__(self, master)
        self.root = root
        self.master = master

        if not root or 'name' not in root or root['name'] != 'feedback':
            err = 'dmarcreport::Feedback::init'
            err = '{0} Expected tag (feedback), got ({1})'.format(err,
                                                                  root.tag)
            raise Exception(err)

        self.fr_header = ttk.Frame(self, style='Header.TFrame')
        self.fr_header.pack(expand=True, fill=tk.Y, side=tk.TOP)
        self.la_header = ttk.Label(self.fr_header, text='Feedback',
                                   style='Header.TLabel')
        self.la_header.pack(expand=True, fill=tk.X, side=tk.TOP)

        self.fr_report = None
        self.fr_record = None
        self.fr_policy = None

        for key, val in root.iteritems():
            if key == 'report_metadata':
                self.fr_report = Report(val, self)
            elif key == 'policy_published':
                self.fr_policy = Policy(val, self)
            elif key == 'record':
                self.fr_record = Record(val, self)

        self.fr_report.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.fr_policy.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.fr_record.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


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


class Policy(ttk.Frame):

    ''' Handles policy pyblished xml content. '''

    def __init__(self, root, master=None):
        ttk.Frame.__init__(self, master)
        self.root = root
        self.master = master
        self.config(style='Header2.TFrame')

        self.fr_body = ttk.Frame(self, style='Header2.TFrame')
        self.fr_body.pack(expand=True, fill=tk.Y)
        self.la_heading = ttk.Label(self.fr_body, text='Policy Published',
                                    style='Header2.TLabel')
        self.la_heading.pack(expand=True, fill=tk.Y)

        self._getdata(root):
            ''' Gets the rest of the data in root. '''
            for key, val in root.iteritems():
                # TODO: FIX FIX FIX


class Record(ttk.Frame):

    ''' Handles policy pyblished xml content. '''

    def __init__(self, root, master=None):
        ttk.Frame.__init__(self, master)
        self.root = root
        self.master = master
        self.config(style='Header2.TFrame')

        self.fr_body = ttk.Frame(self, style='Header2.TFrame')
        self.fr_body.pack(expand=True, fill=tk.Y)
        self.la_heading = ttk.Label(self.fr_body, text='Record',
                                    style='Header2.TLabel')
        self.la_heading.pack(expand=True, fill=tk.Y)


class Report(ttk.Frame):

    ''' Handles report metadata xml content. '''

    def __init__(self, root, master=None):
        ttk.Frame.__init__(self, master)
        self.root = root
        self.master = master
        self.config(style='Header2.TFrame')

        self.fr_body = ttk.Frame(self, style='Header2.TFrame')
        self.fr_body.pack(expand=True, fill=tk.Y)
        self.la_heading = ttk.Label(self.fr_body, text='Report Metadata',
                                    style='Header2.TLabel')
        self.la_heading.pack(expand=True, fill=tk.Y)
