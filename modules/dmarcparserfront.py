''' Frontend graphics for the dmarcparser. '''

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

        self._recordlabel = self._createlabel('Record')
        self._reportmetadatalabel = self._createlabel('Report Metadata')
        self._policypublishedlabel = self._createlabel('Policy Published')

        # Report Meta Data
        self._orgnamelabel = self._createlabel('Org Name')
        self._orgnametext = None
        self._emaillabel = self._createlabel('Email')
        self._emailtext = None
        self._extracontactinfolabel = self._createlabel('Extra Contact Info')
        self._extracontactinfotext = None
        self._reportidlabel = self._createlabel('Report ID')
        self._reportidtext = None
        self._daterangelabel = self._createlabel('Date Range')
        self._daterangebeginlabel = self._createlabel('Begin')
        self._daterangebegintext = None
        self._daterangeendlabel = self._createlabel('End')
        self._daterangeendtext = None

        # Policy Published
        self._domainlabel = self._createlabel('Domain')
        self._domaintext = None
        self._adkimlabel = self._createlabel('ADKIM')
        self._adkimtext = None
        self._aspflabel = self._createlabel('ASPF')
        self._aspftext = None
        self._plabel = self._createlabel('P')
        self._ptext = None
        self._splabel = self._createlabel('SP')
        self._sptext = None
        self._pctlabel = self._createlabel('PCT')
        self._pcttext = None

        self._showbuttons()
        self._showmenu()

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

    def _showbuttons(self):
        ''' Updates the buttons that the application need. '''
        self._quitbutton.grid(row=0, column=2)
        self._openbutton.grid(row=0, column=4)

    def _createlabel(self, text):
        ''' Returns a label with text and self as root/master. '''
        return tk.Label(self, text=text)

    def _showmenu(self):
        ''' Updates the file menu for the application. '''
        self._filemenu.add_command(label="Open", command=self._openfile)
        self._filemenu.add_separator()
        self._filemenu.add_command(label="Quit", command=self.quit)
        self._menubar.add_cascade(label="File", menu=self._filemenu)

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
        self._xml.open()
        tree = self._xml.parsexml()
        root = tree.getroot()
        self._parseroot(root)

    def _parseroot(self, root):
        ''' Parse the root of the xml. '''
        if root.tag != 'feedback':
            raise xmle.XmlDmarcParserException(
                                'Tag is not feedback: {0}'.format(root.tag))

        for child in root:
            if child.tag == 'report_metadata':
                self._parsereportmetadata(child)
            elif child.tag == 'policy_published':
                self._parsepolicypublished(child)
            elif child.tag == 'record':
                self._recordlabel.grid(row=2, column=4)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))

    def _parsereportmetadata(self, root):
        ''' Parse the root of the report metadata child. '''
        if root.tag != 'report_metadata':
            raise xmle.XmlDmarcParserException(
                            "Tag is not report_metadata: {0}".format(root.tag))

        self._reportmetadatalabel.grid(row=2, column=0)
        for child in root:
            if child.tag == 'org_name':
                self._orgnamelabel.grid(row=4, column=0)
                self._orgnametext = self._createlabel(child.text)
                self._orgnametext.grid(row=4, column=1)
            elif child.tag == 'email':
                self._emaillabel.grid(row=5, column=0)
                self._emailtext = self._createlabel(child.text)
                self._emailtext.grid(row=5, column=1)
            elif child.tag == 'extra_contact_info':
                self._extracontactinfolabel.grid(row=6, column=0)
                self._extracontactinfotext = self._createlabel(child.text)
                self._extracontactinfotext.grid(row=6, column=1)
            elif child.tag == 'report_id':
                self._reportidlabel.grid(row=7, column=0)
                self._reportidtext = self._createlabel(child.text)
                self._reportidtext.grid(row=7, column=1)
            elif child.tag == 'date_range':
                self._daterangelabel.grid(row=8, column=0)
                self._daterangebeginlabel.grid(row=9, column=0)
                self._daterangebegintext = self._createlabel(child[0].text)
                self._daterangebegintext.grid(row=9, column=1)
                self._daterangeendlabel.grid(row=10, column=0)
                self._daterangeendtext = self._createlabel(child[1].text)
                self._daterangeendtext.grid(row=10, column=1)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))

    def _parsepolicypublished(self, root):
        ''' Parse the root of the policy published child. '''
        if root.tag != 'policy_published':
            raise xmle.XmlDmarcParserException(
                        "Tag is not policy_published: {0}".format(root.tag))

        self._policypublishedlabel.grid(row=2, column=2)
        for child in root:
            if child.tag == 'domain':
                self._domainlabel.grid(row=4, column=2)
                self._domaintext = self._createlabel(child.text)
                self._domaintext.grid(row=4, column=3)
            elif child.tag == 'adkim':
                self._adkimlabel.grid(row=5, column=2)
                self._adkimtext = self._createlabel(child.text)
                self._adkimtext.grid(row=5, column=3)
            elif child.tag == 'aspf':
                self._aspflabel.grid(row=6, column=2)
                self._aspftext = self._createlabel(child.text)
                self._aspftext.grid(row=6, column=3)
            elif child.tag == 'p':
                self._plabel.grid(row=7, column=2)
                self._ptext = self._createlabel(child.text)
                self._ptext.grid(row=7, column=3)
            elif child.tag == 'sp':
                self._splabel.grid(row=8, column=2)
                self._sptext = self._createlabel(child.text)
                self._sptext.grid(row=8, column=3)
            elif child.tag == 'pct':
                self._pctlabel.grid(row=9, column=2)
                self._pcttext = self._createlabel(child.text)
                self._pcttext.grid(row=9, column=3)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))
