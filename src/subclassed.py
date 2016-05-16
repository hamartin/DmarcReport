# -*- coding: UTF-8 -*-

'''Tkinter widgets subclassed for DmarcReport purposes.'''

import Tkinter as tk
import ttk


class About(tk.Toplevel):

    ''' A class to display information about the developer. '''

    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.root = root
        self.title('About Dmarc Report')

        self.transient(root)
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

        root.wait_window(self)

    def kill(self):
        ''' Destroys the current modal window and returns focus to root. '''
        self.root.focus_set()
        tk.Toplevel.destroy(self)


class Menu(tk.Menu):

    '''Sets the menu for this program.'''

    def __init__(self, root):
        tk.Menu.__init__(self, root)
        self.root = root

        self.me_file = tk.Menu(self, tearoff=0)
        self.me_file.add_command(label='Open', underline=0,
                                 command=self.quit)
        self.me_file.add_separator()
        self.me_file.add_command(label='Quit', underline=0,
                                 command=self.quit)
        self.add_cascade(label='File', underline=0, menu=self.me_file)
        self.meabout = tk.Menu(self, tearoff=0)
        self.meabout.add_command(label='About', underline=0,
                                 command=self.about)
        self.add_cascade(label='Help', underline=0, menu=self.meabout)
        self.root.config(menu=self)

    def about(self):
        ''' Will display a modal window with some information. '''
        About(self.root)


class MsgLabel(tk.Label):

    '''Creates a message label.'''

    def __init__(self, root, **kwargs):
        tk.Label.__init__(self, root, **kwargs)
        self.root = root

        canchor = tk.E
        justify = tk.RIGHT
        fill = tk.X
        expand = True
        side = tk.LEFT
        panchor = tk.E
        padx = 20
        pady = (0, 5)

        for key, val in kwargs.iteritems():
            if key == 'canchor' and isinstance(val, str):
                canchor = val
            elif key == 'justify' and isinstance(val, str):
                justify = val
            elif key == 'fill' and isinstance(val, str):
                fill = val
            elif key == 'expand' and isinstance(val, bool):
                expand = val
            elif key == 'side' and isinstance(val, str):
                side = val
            elif key == 'panchor' and isinstance(val, str):
                panchor = val
            elif key == 'padx' and isinstance(val, int):
                padx = val
            elif key == 'pady' and (isinstance(val, int) or
                                    isinstance(val, tuple)):
                pady = val

        self.config(anchor=canchor, justify=justify)
        self.pack(fill=fill, expand=expand, side=side, anchor=panchor,
                  padx=padx, pady=pady)


class SepLineFrame(tk.Frame):

    '''Creates a separator line using Tkinter Frame and packs it.'''

    def __init__(self, root, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)

        relief = tk.RIDGE
        height = 2
        fbg = 'white'
        padx = 20
        pady = 5
        fill = tk.X

        for key, val in kwargs.iteritems():
            if key == 'relief' and isinstance(val, str):
                relief = val
            elif key == 'height' and isinstance(val, int):
                height = val
            elif key == 'bg' and isinstance(val, str):
                fbg = val
            elif key == 'padx' and isinstance(val, int):
                padx = val
            elif key == 'pady' and isinstance(val, int):
                pady = val
            elif key == 'fill' and isinstance(val, str):
                fill = val

        self.config(relief=relief, height=height, bg=fbg)
        self.pack(padx=padx, pady=pady, fill=fill)
