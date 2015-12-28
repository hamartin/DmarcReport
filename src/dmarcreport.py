# -*- coding: latin-1 -*-

''' A simple Tkinter graphical user interface for reading DMARC XML files. '''

import Tkinter as tk
import ttk


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

        self.aboutcontent = '''
            Created by Hans Åge Martinsen
            Email: <hamartin@moshwire.com>
            URL: https://github.com/hamartin/DmarcReport
        '''

        self.destroy = self.register(self.killwin)
        self.protocol('WM_DELETE_WINDOW', self.destroy)

        self.fr_body = ttk.Frame(self, padding=5)
        self.la_about = ttk.Label(self.fr_body, text=self.aboutcontent,
                                  padding=(0, 0, 50, 0))
        self.bu_ok = ttk.Button(self.fr_body, text='OK', command=self.destroy)
        self.bu_ok.focus()
        self.bu_ok.bind('<Return>', self.destroy)

        self.fr_body.pack()
        self.la_about.pack()
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

        self.fr_begin = ttk.Frame(self)
        self.fr_begin.pack()
        self.bu_quit = ttk.Button(self, text='Quit', command=self.quit)
        self.bu_quit.pack()
        self.bu_open = ttk.Button(self, text='Open', command=self.open)
        self.bu_open.pack()

    def open(self):
        ''' foo '''
        print "foo"


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
