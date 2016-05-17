# -*- coding: UTF-8 -*-

'''Policy part of DMARC.'''

import Tkinter as tk


class Policy(tk.Frame):

    '''Policy frame.'''

    def __init__(self, root, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.root = root
        self.config(bd=10, relief=tk.FLAT, bg='white')
        tk.Label(self, text='Policy', bg='green').pack()
