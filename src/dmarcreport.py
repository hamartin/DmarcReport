''' A simple Tkinter graphical user interface for reading DMARC XML files. '''

import Tkinter as tk
import ttk


class About(tk.Toplevel):

    ''' DmarcParsers modal about window. '''

    def __init__(self, master):
        # TODO: I have been trying to make this window completely modal, but is
        # unable to do so. Will keep this TODO here to make it possible for me
        # to fix this at a later time.
        tk.Toplevel.__init__(self, master)
        self.transient(master)
        self.master = master
        self.title('About DmarcParser')

        self.destroy = self.register(self.killwin)
        self.protocol('WM_DELETE_WINDOW', self.destroy)

        self.fr_body = ttk.Frame(self, padding=5)
        self.la_about = ttk.Label(self.fr_body, text='About')
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
        # TODO: Arguments for this call has to be changed into something that
        # actually work as intended.
        self.menu.init(self.quit)


class Menu(tk.Menu):

    ''' DmarcParsers menu bar. '''

    def __init__(self, master=None):
        tk.Menu.__init__(self, master)
        self.master = master

        self.me_file = tk.Menu(self, tearoff=0)
        self.me_about = tk.Menu(self, tearoff=0)

    def init(self, openfile):
        ''' Initializes the menu bar. '''
        self.me_file.add_command(label='Open', command=openfile)
        self.me_file.add_separator()
        self.me_file.add_command(label='Quit', command=self.quit)
        self.add_cascade(label='File', menu=self.me_file)
        self.me_about.add_command(label='About', command=self.about)
        self.add_cascade(label='Help', menu=self.me_about)
        self.master.config(menu=self)

    def about(self):
        ''' Will display a modal window with information about. '''
        About(self.master)
