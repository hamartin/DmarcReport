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

        self._labels = self._getlabels()
        self._showlabels()
        self._showmenu()
        self._showbuttons()

        # These are to be removed and made into something else
        self._orgnametext = None
        self._emailtext = None
        self._extracontactinfotext = None
        self._reportidtext = None
        self._daterangebegintext = None
        self._daterangeendtext = None
        self._domaintext = None
        self._adkimtext = None
        self._aspftext = None
        self._ptext = None
        self._sptext = None
        self._pcttext = None
        self._sourceiptext = None
        self._counttext = None
        self._dispositiontext = None
        self._dkimtext = None
        self._spftext = None
        self._headerfromtext = None
        self._spftext2 = None
        self._domaintext2 = None
        self._resulttext = None
        self._domaintext3 = None
        self._resulttext2 = None

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

    def _createlabel(self, text):
        ''' Returns a label with text and self as root/master. '''
        return tk.Label(self, text=text)


    def _showbuttons(self):
        ''' Updates the buttons that the application need. '''
        self._quitbutton.grid(row=0, column=0)
        self._openbutton.grid(row=0, column=1)

    def _showlabels(self):
        ''' Shows the labels on GUI. '''

        lab = self._labels

        # Col 0
        lab['report_metadata'].grid(row=2, column=0)
        lab['org_name'].grid(row=4, column=0)
        lab['email'].grid(row=5, column=0)
        lab['report_id'].grid(row=6, column=0)
        lab['extra_contact_info'].grid(row=7, column=0)
        lab['date_range'].grid(row=8, column=0)
        lab['begin'].grid(row=9, column=0)
        lab['end'].grid(row=10, column=0)

        # Col 2
        lab['policy_published'].grid(row=2, column=2)
        lab['domain1'].grid(row=4, column=2)
        lab['adkim'].grid(row=5, column=2)
        lab['aspf'].grid(row=6, column=2)
        lab['p'].grid(row=7, column=2)
        lab['sp'].grid(row=8, column=2)
        lab['pct'].grid(row=9, column=2)

        # Col 4
        lab['record'].grid(row=2, column=4)
        lab['row'].grid(row=4, column=4)
        lab['source_ip'].grid(row=5, column=4)
        lab['count'].grid(row=6, column=4)
        lab['policy_evaluated'].grid(row=7, column=4)
        lab['disposition'].grid(row=8, column=4)
        lab['dkim1'].grid(row=9, column=4)
        lab['spf1'].grid(row=10, column=4)
        lab['identifiers'].grid(row=11, column=4)
        lab['header_from'].grid(row=12, column=4)
        lab['auth_results'].grid(row=13, column=4)
        lab['spf2'].grid(row=14, column=4)
        lab['domain2'].grid(row=15, column=4)
        lab['result1'].grid(row=16, column=4)
        lab['dkim2'].grid(row=17, column=4)
        lab['domain3'].grid(row=18, column=4)
        lab['result2'].grid(row=19, column=4)

    def _getlabels(self):
        ''' Creates a dictionary of labels that are to be used in the GUI. '''

        cla = self._createlabel

        ret = {}
        ret['adkim'] = cla('ADKIM')
        ret['aspf'] = cla('ASPF')
        ret['auth_results'] = cla('Auth Results')
        ret['begin'] = cla('Begin')
        ret['count'] = cla('Count')
        ret['date_range'] = cla('Date Range')
        ret['disposition'] = cla('Disposition')
        ret['dkim1'] = cla('DKIM')
        ret['dkim2'] = cla('DKIM')
        ret['domain1'] = cla('Domain')
        ret['domain2'] = cla('Domain')
        ret['domain3'] = cla('Domain')
        ret['email'] = cla('Email')
        ret['end'] = cla('End')
        ret['extra_contact_info'] = cla('Extra Contact Info')
        ret['feedback'] = cla('Feedback')
        ret['header_from'] = cla('Header From')
        ret['identifiers'] = cla('Identifiers')
        ret['org_name'] = cla('Org Name')
        ret['p'] = cla('P')
        ret['pct'] = cla('PCT')
        ret['policy_evaluated'] = cla('Policy Evaluated')
        ret['policy_published'] = cla('Policy Published')
        ret['record'] = cla('Record')
        ret['report_id'] = cla('Report ID')
        ret['report_metadata'] = cla('Report Metadata')
        ret['result1'] = cla('Result')
        ret['result2'] = cla('Result')
        ret['row'] = cla('Row')
        ret['source_ip'] = cla('Source IP')
        ret['sp'] = cla('SP')
        ret['spf1'] = cla('SPF')
        ret['spf2'] = cla('SPF')
        return ret

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

        for child in root:
            if child.tag == 'org_name':
                self._orgnametext = self._createlabel(child.text)
                self._orgnametext.grid(row=4, column=1)
            elif child.tag == 'email':
                self._emailtext = self._createlabel(child.text)
                self._emailtext.grid(row=5, column=1)
            elif child.tag == 'extra_contact_info':
                self._extracontactinfotext = self._createlabel(child.text)
                self._extracontactinfotext.grid(row=6, column=1)
            elif child.tag == 'report_id':
                self._reportidtext = self._createlabel(child.text)
                self._reportidtext.grid(row=7, column=1)
            elif child.tag == 'date_range':
                self._daterangebegintext = self._createlabel(child[0].text)
                self._daterangebegintext.grid(row=9, column=1)
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

        for child in root:
            if child.tag == 'domain':
                self._domaintext = self._createlabel(child.text)
                self._domaintext.grid(row=4, column=3)
            elif child.tag == 'adkim':
                self._adkimtext = self._createlabel(child.text)
                self._adkimtext.grid(row=5, column=3)
            elif child.tag == 'aspf':
                self._aspftext = self._createlabel(child.text)
                self._aspftext.grid(row=6, column=3)
            elif child.tag == 'p':
                self._ptext = self._createlabel(child.text)
                self._ptext.grid(row=7, column=3)
            elif child.tag == 'sp':
                self._sptext = self._createlabel(child.text)
                self._sptext.grid(row=8, column=3)
            elif child.tag == 'pct':
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

        for child in root:
            if child.tag == 'source_ip':
                self._sourceiptext = self._createlabel(child.text)
                self._sourceiptext.grid(row=5, column=5)
            elif child.tag == 'count':
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

        for child in root:
            if child.tag == 'disposition':
                self._dispositiontext = self._createlabel(child.text)
                self._dispositiontext.grid(row=8, column=5)
            elif child.tag == 'dkim':
                self._dkimtext = self._createlabel(child.text)
                self._dkimtext.grid(row=9, column=5)
            elif child.tag == 'spf':
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

        for child in root:
            if child.tag == 'header_from':
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

        for child in root:
            if child.tag == 'domain':
                self._domaintext2 = self._createlabel(child.text)
                self._domaintext2.grid(row=15, column=5)
            elif child.tag == 'result':
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

        for child in root:
            if child.tag == 'domain':
                self._domaintext3 = self._createlabel(child.text)
                self._domaintext3.grid(row=18, column=5)
            elif child.tag == 'result':
                self._resulttext2 = self._createlabel(child.text)
                self._resulttext2.grid(row=19, column=5)
            else:
                raise xmle.XmlDmarcParserException("Unknown tag: {0}".format(
                                                                    child.tag))





