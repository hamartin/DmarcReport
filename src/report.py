# -*- coding: UTF-8 -*-

'''Report part of DMARC.'''

import Tkinter as tk


class Report(tk.Frame):

    '''Report frame.'''

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.config(bd=10, relief=tk.FLAT, bg='yellow')
        tk.Label(self, text='Report', bg='pink').pack()
