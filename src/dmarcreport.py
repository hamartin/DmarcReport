''' A simple Tkinter graphical user interface for reading DMARC XML files. '''

import Tkinter as tk


class DmarcReport(tk.Tk):

    ''' A simple Tkinter graphical user interface for reading DMARC XML
    files. '''

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("DmarcReport")

        self.menu = Menu(self)


class Menu(tk.Menu):

    ''' DmarcParsers menu bar. '''

    def __init__(self, master=None):
        tk.Menu.__init__(self, master)
        self.master = master

        self.me_file = tk.Menu(self, tearoff=0)
        self.me_about = tk.Menu(self, tearoff=0)
        self.init()

    def init(self):
        ''' Initializes the menu bar. '''
        self.me_file.add_command(label='Open', command=self.quit)
        self.me_file.add_separator()
        self.me_file.add_command(label='Quit', command=self.quit)
        self.add_cascade(label='File', menu=self.me_file)
        self.me_about.add_command(label='About', command=self.quit)
        self.add_cascade(label='Help', menu=self.me_about)
        self.master.config(menu=self)
