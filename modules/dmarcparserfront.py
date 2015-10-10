''' Frontend graphics for the dmarcparser. '''

import Tkinter as tk
import tkFileDialog as tfd
import xmldmarcparser as xml
import dmarcparserfrontexceptions as dpfe

class DmarcParserFront(tk.Frame):

    ''' Frontend graphics for the dmarcparser. '''

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title('DMARC Parser')

        self._xml = xml.XmlDmarcParser()
        self._fileopts = None

        # Widgets
        self._menubar = None
        self._filemenu = None
        self._aboutmenu = None
        self._quitbutton = None
        self._openbutton = None

        self._createbuttons()
        self._createmenu()

    def __str__(self):
        return 'DmarcParserFrontend'

    def __repr__(self):
        return repr('DmarcParserFrontend')

    def _createbuttons(self):
        ''' Creates the buttons that the application need. '''
        self._quitbutton = tk.Button(self, text='Quit', command=self.quit)
        self._quitbutton.grid()
        self._openbutton = tk.Button(self, text='Open', command=self._openfile)
        self._openbutton.grid()

    def _createmenu(self):
        ''' Creates the file menu for the application. '''
        if self._menubar or self._filemenu:
            raise dpfe.DmarcParserFrontException(
                                            'Menubar and filemenu defined.')
        self._menubar = tk.Menu(self.master)
        self._filemenu = tk.Menu(self._menubar, tearoff=0)
        self._filemenu.add_command(label="Open", command=self._openfile)
        self._filemenu.add_separator()
        self._filemenu.add_command(label="Quit", command=self.quit)
        self._menubar.add_cascade(label="File", menu=self._filemenu)

        self._aboutmenu = tk.Menu(self._menubar, tearoff=0)
        self._aboutmenu.add_command(label="About", command=self.quit)
        self._menubar.add_cascade(label="Help", menu=self._aboutmenu)

        self.master.config(menu=self._menubar)

    def _openfile(self):
        ''' Opens a file dialog and sets the file for the XML parser. '''
        self._fileopts = opts = {}
        opts['defaultextension'] = '.xml'
        opts['filetypes'] = [('all files', '.*'), ('XML files', '.xml')]
        filename = tfd.askopenfilename(**self._fileopts)
        self._xml.setfilename(filename)
