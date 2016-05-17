# -*- coding: UTF-8 -*-

'''Record part of DMARC.'''

import Tkinter as tk


class Record(tk.Frame):

    '''Record frame.'''

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.config(bd=10, relief=tk.FLAT, bg='blue')
        tk.Label(self, text='Record', bg='red').pack()
