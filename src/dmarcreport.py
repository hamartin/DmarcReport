# -*- coding: UTF-8 -*-

'''A simple Tkinter graphical user interface for reading and displaying
DMARC XML/Zip information.'''

import Tkinter as tk

import src.config as cnf
import src.exceptions as excp
import src.policy as policy
import src.record as record
import src.report as report
import src.subclassed as sc


class DmarcReport(tk.Tk):

    '''A simple Tkinter graphical user interface for reading and
    displaying DMARC XML/Zip information.'''

    def __init__(self):
        tk.Tk.__init__(self)
        self.title(cnf.PROG_NAME)

        self.initialize()
        self.set_message('Ready…')

    def clear_message(self):
        '''Clears the message label.'''
        self.msg_label.config(text='')

    def initialize(self):
        '''Initializes the graphical user interface.'''
        # Header.
        sc.Menu(self)
        header = tk.Frame(self)
        header.pack(fill=tk.X)
        header_label = tk.Label(header, text='Feedback', pady=30,
                                padx=30, font=('courier', 30, 'bold'))
        header_label.pack(fill=tk.BOTH, expand=True)

        # Body.
        body = tk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True)
        self.record = record.Record(body)
        self.record.pack(fill=tk.Y, expand=True, side=tk.LEFT)
        self.policy = policy.Policy(body)
        self.policy.pack(fill=tk.Y, expand=True, side=tk.LEFT)
        self.report = report.Report(body)
        self.report.pack(fill=tk.Y, expand=True, side=tk.LEFT)

        # Footer.
        sc.SepLineFrame(self)
        self.msg_label = sc.MsgLabel(self)

    def set_message(self, msg, seconds=None):
        '''Sets a message to be shown in the bottom of the program.'''
        if isinstance(msg, str):
            self.msg_label.config(text=msg)
        else:
            err = 'set_message::Attribute msg is not of type str.'
            raise excp.DmarcReportError(err)

        if seconds and isinstance(seconds, int):
            self.msg_label.after(1000 * seconds, self.clear_message)
        if seconds and not isinstance(seconds, int):
            err = 'set_message::Attribute seconds is not of type int.'
            raise excp.DmarcReportError(err)
