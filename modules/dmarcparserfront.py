''' Frontend graphics for the dmarcparser. '''

import datetime
import Tkinter as tk
import tkFileDialog as tfd
import xmldmarcparser as xml
import xmldmarcparserexceptions as xmle

class DmarcParserFront(tk.Frame):

    ''' Frontend graphics for the dmarcparser. '''

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title('DMARC Parser')

        self._xml = xml.XmlDmarcParser()
        self._fileopts = None

        # Widgets
        self._menubar = tk.Menu(self.master)
        self._filemenu = tk.Menu(self._menubar, tearoff=0)
        self._aboutmenu = tk.Menu(self._menubar, tearoff=0)
        self._quitbutton = tk.Button(self, text='Quit', command=self.quit)
        self._openbutton = tk.Button(self, text='Open', command=self._openfile)

        self._labels = {}

        self._showmenu()
        self._showbuttons()

    def __str__(self):
        return 'DmarcParserFrontend'

    def __repr__(self):
        return repr('DmarcParserFrontend')

    def _closefile(self):
        ''' Closes the XML file if open. '''
        try:
            self._xml.close()
        except xmle.XmlDmarcParserFileException:
            pass

    def _createlabel(self, *args, **kwargs):
        ''' Returns a tupple with label and if passed, a value to. '''
        if 'bold' in kwargs:
            label = tk.Label(self, text=args[0], font="Verdana 16 bold")
        else:
            label = tk.Label(self, text=args[0])

        value = None
        try:
            if 'bg' in kwargs and kwargs['bg'] == 'green':
                value = tk.Label(self, text=args[1], bg='green')
            elif 'bg' in kwargs and kwargs['bg'] == 'red':
                value = tk.Label(self, text=args[1], bg='red')
            else:
                value = tk.Label(self, text=args[1])
        except IndexError:
            pass

        return (label, value)

    def _openfile(self):
        ''' Opens a file dialog and sets the file for the XML parser. '''
        self._fileopts = opts = {}
        opts['defaultextension'] = '.xml'
        opts['filetypes'] = [('all files', '.*'), ('XML files', '.xml')]
        filename = tfd.askopenfilename(**self._fileopts)
        self._xml.setfilename(filename)
        self._xml.open()
        tree = self._xml.parsexml()
        root = tree.getroot()
        self._labels = self._getdic(root, {})
        self._showlabels(self._labels, 2, 0)

    def _showbuttons(self):
        ''' Updates the buttons that the application need. '''
        self._quitbutton.grid(row=0, column=0)
        self._openbutton.grid(row=0, column=1)

    def _showlabels(self, labels, row, column):
        ''' Grids the labels. '''

        if 'name' in labels:
            labels['name'][0].grid(row=row, column=column, sticky=tk.W)
            row += 1

        for key, value in labels.iteritems():
            if key == 'name':
                continue
            elif key == 'report_metadata':
                column = 0
                row = 3
                row = self._showlabels(value, row+1, column)
            elif key == 'policy_published':
                column = 2
                row = 3
                row = self._showlabels(value, row+1, column)
            elif key == 'record':
                column = 4
                row = 3
                row = self._showlabels(value, row+1, column)
            else:
                try:
                    value[0].grid(row=row, column=column, sticky=tk.W,
                                                                padx=(100, 10))
                    value[1].grid(row=row, column=column+1, sticky=tk.W,
                                                                padx=(0, 30))
                except KeyError:
                    row = self._showlabels(value, row+1, column)
                else:
                    row += 1

        return row

    def _showmenu(self):
        ''' Updates the file menu for the application. '''
        self._filemenu.add_command(label="Open", command=self._openfile)
        self._filemenu.add_separator()
        self._filemenu.add_command(label="Quit", command=self.quit)
        self._menubar.add_cascade(label="File", menu=self._filemenu)

        self._aboutmenu.add_command(label="About", command=self.quit)
        self._menubar.add_cascade(label="Help", menu=self._aboutmenu)

        self.master.config(menu=self._menubar)

    def _getdic(self, root, dic):
        ''' Iterates over root and puts the headers and values in dic. '''
        cla = self._createlabel

        if root.getchildren():
            dic['name'] = cla(root.tag.title().replace('_', ' '), bold=True)
            for child in root:
                dic[child.tag] = self._getdic(child, {})
        else:
            if root.tag == 'begin' or root.tag == 'end':
                dic[root.tag] = cla(root.tag.title().replace('_', ' '),
                                                unixtimestamptodate(root.text))
            elif root.text == 'pass':
                dic[root.tag] = cla(root.tag.title().replace('_', ' '),
                                                        root.text, bg='green')
            elif root.text == 'fail':
                dic[root.tag] = cla(root.tag.title().replace('_', ' '),
                                                        root.text, bg='red')
            else:
                dic[root.tag] = cla(root.tag.title().replace('_', ' '),
                                                                    root.text)

        return dic

def unixtimestamptodate(uts):
    ''' Converts unix time stamp to date. '''
    return datetime.datetime.fromtimestamp(int(uts)).strftime("%d.%m.%Y")
