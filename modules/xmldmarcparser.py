''' Xml parser for the dmarcparser. '''

import xml.etree.ElementTree as et
import xmldmarcparserexceptions as xmle


class XmlDmarcParser:

    ''' Class that will parse DMARC XML files. '''

    def __init__(self, **kwargs):
        self._filename = None
        self._file = None

        for key, value in kwargs.iteritems():
            if key == 'filename':
                self._filename = value
            elif key == 'file':
                self._file = value

    def __str__(self):
        return "XmlDmarcParser: {0}".format(self._filename)

    def __repr__(self):
        return repr("XmlDmarcParser: {0}".format(self._filename))

    def close(self):
        ''' Closes an open XML file. '''
        if not self._file:
            raise xmle.XmlDmarcParserFileException("No file is open.")
        self._file.close()

    def open(self):
        ''' Opens an XML file. '''
        if not self._filename:
            raise xmle.XmlDmarcParserFileException("No file name defined.")

        if self._file:
            self._file.close()

        try:
            self._file = open(self._filename, 'r')
        except IOError, err:
            # err[0] is the error message error number on the system.
            raise xmle.XmlDmarcParserFileException(err[1])

    def setfilename(self, filename):
        ''' Sets a new file name. This method will close an open file. '''
        if self._file:
            self.close()

        self._filename = filename

    def parsexml(self):
        ''' Parses the loaded xml file. '''
        if not self._file:
            raise xmle.XmlDmarcParserFileException('No file loaded.')
        return et.parse(self._file)
