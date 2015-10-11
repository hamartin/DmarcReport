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

        # Record
        self._rowlabel = self._createlabel('Row')
        self._sourceiplabel = self._createlabel('Source IP')
        self._sourceiptext = None
        self._countlabel = self._createlabel('Count')
        self._counttext = None
        self._policyevaluatedlabel = self._createlabel('Policy Evaluated')
        self._dispositionlabel = self._createlabel('Disposition')
        self._dispositiontext = None
        self._dkimlabel = self._createlabel('DKIM')
        self._dkimtext = None
        self._spflabel = self._createlabel('SPF')
        self._spftext = None
        self._identifierslabel = self._createlabel('Identifiers')
        self._headerfromlabel = self._createlabel('Header From')
        self._headerfromtext = None
        self._authresultslabel = self._createlabel('Auth Results')
        self._spflabel2 = self._createlabel('SPF')
        self._spftext2 = None
        self._domainlabel2 = self._createlabel('Domain')
        self._domaintext2 = None
        self._resultlabel = self._createlabel('Result')
        self._resulttext = None
        self._dkimlabel2 = self._createlabel('DKIM')
        self._domainlabel3 = self._createlabel('Domain')
        self._domaintext3 = None
        self._resultlabel2 = self._createlabel('Result')
        self._resulttext2 = None

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
        self._quitbutton.grid(row=0, column=0)
        self._openbutton.grid(row=0, column=1)

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
                self._parserecord(child)
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

    def _parserecord(self, root):
        ''' Parse the root of the record child. '''
        if root.tag != 'record':
            raise xmle.XmlDmarcParserException(
                            "Tag is not record: {0}".format(root.tag))

        self._recordlabel.grid(row=2, column=4)
        for child in root:
            if child.tag == 'row':
                self._parserow(child)
            elif child.tag == 'identifiers':
                self._parseidentifiers(child)
            elif child.tag == 'auth_results':
                self._parseauthresults(child)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))

    def _parserow(self, root):
        ''' Parse the root of the row child. '''
        if root.tag != 'row':
            raise xmle.XmlDmarcParserException(
                                        "Tag is not row: {0}".format(root.tag))

        self._rowlabel.grid(row=4, column=4)
        for child in root:
            if child.tag == 'source_ip':
                self._sourceiplabel.grid(row=5, column=4)
                self._sourceiptext = self._createlabel(child.text)
                self._sourceiptext.grid(row=5, column=5)
            elif child.tag == 'count':
                self._countlabel.grid(row=6, column=4)
                self._counttext = self._createlabel(child.text)
                self._counttext.grid(row=6, column=5)
            elif child.tag == 'policy_evaluated':
                self._parsepolicyevaluated(child)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))

    def _parsepolicyevaluated(self, root):
        ''' Parse the root of the policy evaluated child. '''
        if root.tag != 'policy_evaluated':
            raise xmle.XmlDmarcParserException(
                        "Tag is not policy_evaluated: {0}".format(root.tag))

        self._policyevaluatedlabel.grid(row=7, column=4)
        for child in root:
            if child.tag == 'disposition':
                self._dispositionlabel.grid(row=8, column=4)
                self._dispositiontext = self._createlabel(child.text)
                self._dispositiontext.grid(row=8, column=5)
            elif child.tag == 'dkim':
                self._dkimlabel.grid(row=9, column=4)
                self._dkimtext = self._createlabel(child.text)
                self._dkimtext.grid(row=9, column=5)
            elif child.tag == 'spf':
                self._spflabel.grid(row=10, column=4)
                self._spftext = self._createlabel(child.text)
                self._spftext.grid(row=10, column=5)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))

    def _parseidentifiers(self, root):
        ''' Parse the root of the identifiers child. '''
        if root.tag != 'identifiers':
            raise xmle.XmlDmarcParserException(
                                "Tag is not identifiers: {0}".format(root.tag))

        self._identifierslabel.grid(row=11, column=4)
        for child in root:
            if child.tag == 'header_from':
                self._headerfromlabel.grid(row=12, column=4)
                self._headerfromtext = self._createlabel(child.text)
                self._headerfromtext.grid(row=12, column=5)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))

    def _parseauthresults(self, root):
        ''' Parse the root of the auth results child. '''
        if root.tag != 'auth_results':
            raise xmle.XmlDmarcParserException(
                            "Tag is not auth_results: {0}".format(root.tag))

        self._authresultslabel.grid(row=13, column=4)
        for child in root:
            if child.tag == 'spf':
                self._parsespf(child)
            elif child.tag == 'dkim':
                self._parsedkim(child)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))

    def _parsespf(self, root):
        ''' Parse the root of the spf child. '''
        if root.tag != 'spf':
            raise xmle.XmlDmarcParserException(
                                    "Tag is not spf: {0}".format(root.tag))

        self._spflabel2.grid(row=14, column=4)
        for child in root:
            if child.tag == 'domain':
                self._domainlabel2.grid(row=15, column=4)
                self._domaintext2 = self._createlabel(child.text)
                self._domaintext2.grid(row=15, column=5)
            elif child.tag == 'result':
                self._resultlabel.grid(row=16, column=4)
                self._resulttext = self._createlabel(child.text)
                self._resulttext.grid(row=16, column=5)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))

    def _parsedkim(self, root):
        ''' Parse the root of the dkim child. '''
        if root.tag != 'dkim':
            raise xmle.XmlDmarcParserException(
                                    "Tag is not dkim: {0}".format(root.tag))

        self._dkimlabel2.grid(row=17, column=4)
        for child in root:
            if child.tag == 'domain':
                self._domainlabel3.grid(row=18, column=4)
                self._domaintext3 = self._createlabel(child.text)
                self._domaintext3.grid(row=18, column=5)
            elif child.tag == 'result':
                self._resultlabel2.grid(row=19, column=4)
                self._resulttext2 = self._createlabel(child.text)
                self._resulttext2.grid(row=19, column=5)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))





