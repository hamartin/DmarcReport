# -*- coding: latin-1 -*-

''' A simple Tkinter graphical user interface for reading DMARC XML files. '''

import datetime
import re
import tkFileDialog as tkfd
import Tkinter as tk
import ttk
import src.xmldm as xmldm


def stdframe(key, value, fr_l, fr_r):
    ''' Creates a frame with two labels in it and packs it. '''
    ttk.Label(fr_l, text=key.replace('_', ' ').title(),
              anchor=tk.W).pack()
    ttk.Label(fr_r, text=value).pack()


def unixtimestamptodate(uts):
    ''' Converts Unix time stamp to date. '''
    return datetime.datetime.fromtimestamp(int(uts)).strftime("%d.%m.%Y")


class About(tk.Toplevel):

    ''' DmarcReports modal about window. '''

    def __init__(self, master):
        # TODO: I have been trying to make this window completely modal, but is
        # unable to do so. Will keep this here to remember me to fix this at a
        # later time.
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
        self.gui.configure('H1.TLabel', padding=30,
                           font=('courier', 30, 'bold'))
        self.gui.configure('H2.TLabel', padding=24,
                           font=('courier', 24, 'bold'))

    def open(self):
        ''' Opens a file dialog which the user can select a file to open. '''
        filename = tkfd.askopenfilename(**self.fileopts)
        if filename and not re.match(r'^\d+$', filename):
            self.fr_feedback = Feedback(xmldm.xmldict(filename), self)
            self.fr_begin.pack_forget()
            self.fr_feedback.pack(expand=True, fill=tk.BOTH)


class Feedback(ttk.Frame):

    ''' Creates a frame with widgets. '''

    def __init__(self, root, master=None):
        ttk.Frame.__init__(self, master)
        self.root = root
        self.master = master

        ttk.Label(self, text='Feedback', style='H1.TLabel').pack()

        for key, val in root.iteritems():
            if key == 'report_metadata':
                Report(val, self).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            elif key == 'policy_published':
                Policy(val, self).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            elif key == 'record':
                Record(val, self).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


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
        # self.config()

        ttk.Label(self, text='Policy Published', style='H2.TLabel').pack()

        self.fr_left = ttk.Frame(self)
        self.fr_left.pack(side=tk.LEFT)
        self.fr_right = ttk.Frame(self)
        self.fr_right.pack(side=tk.LEFT)

        self._getdata(root)

    def _getdata(self, root):
        ''' Iterates over a dictionary and retrieves information. '''
        for key, val in root.iteritems():
            stdframe(key, val, self.fr_left, self.fr_right)


class Record(ttk.Frame):

    ''' Handles policy pyblished xml content. '''

    def __init__(self, root, master=None):
        ttk.Frame.__init__(self, master)
        self.root = root
        self.master = master
        # self.config()

        ttk.Label(self, text='Record', style='H2.TLabel').pack()

        self.fr_body = ttk.Frame(self)
        self.fr_body.pack(expand=True, fill=tk.Y)


class Report(ttk.Frame):

    ''' Handles report metadata xml content. '''

    def __init__(self, root, master=None):
        ttk.Frame.__init__(self, master)
        self.root = root
        self.master = master
        # self.config()

        ttk.Label(self, text='Report Metadata', style='H2.TLabel').pack()

        self.fr_left = ttk.Frame(self)
        self.fr_left.pack(side=tk.LEFT)
        self.fr_right = ttk.Frame(self)
        self.fr_right.pack(side=tk.LEFT)

        self._getdata(root)

    def _getdata(self, root):
        ''' Iterates over a dictionary and retrieves information. '''
        for key, val in root.iteritems():
            if key == 'org_name' or key == 'email' or key == 'report_id':
                stdframe(key, val, self.fr_left, self.fr_right)
            elif key == 'date_range':
                ttk.Label(self.fr_left,
                          text=key.replace('_', ' ').title()).pack()
                for k in val:
                    stdframe(k, unixtimestamptodate(val[k]), self.fr_left,
                             self.fr_right)
