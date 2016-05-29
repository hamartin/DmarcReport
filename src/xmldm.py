# -*- coding: UTF-8 -*-
# File name: xmldm.py

'''Module to parse XML files.'''

import re
import xml.etree.ElementTree as et
import zipfile


class XmlDmError(Exception):

    '''Base XML error exception.'''

    def __init__(self, message):
        super(XmlDmError, self).__init__(message)
        self.message = message


class XmlDmFileError(XmlDmError):

    '''XmlDm fil error exception.'''

    def __init__(self, message):
        super(XmlDmFileError, self).__init__(message)
        self.message = message


class XmlDm(object):

    '''Class to do various things with XML files.'''

    def __init__(self, file_name):
        if not file_name or re.match(r'^\s+$', file_name):
            raise XmlDmError('File name not specified!')
        self.file_name = file_name

    def open(self):
        '''Opens a standard XML file or Zip file and returns it.'''
        if not self.file_name or re.match(r'^\s+$', self.file_name):
            raise XmlDmError('File name not specified!')
        if zipfile.is_zipfile(self.file_name):
            fpz = zipfile.ZipFile(self.file_name)
            if len(fpz.infolist()) > 1:
                raise XmlDmFileError('More than 1 file stored in zip file!')
            else:
                zipfp = fpz.infolist()[0]
                return fpz.open(zipfp)
        else:
            return open(self.file_name, 'r')

    def get_dictionary(self):
        '''Returns an XML parsed and populated into a dictionary.'''
        fpo = self.open()
        if not fpo:
            raise XmlDmFileError('No file is open!')
        root = get_root(fpo)
        fpo.close()
        return parse(root)


def parse(root):
    '''Returns a two value tupple with tag and subroot where tag is key and
    subroot is a dictionary.'''
    return root.tag, dict(map(parse, root)) or root.text


def get_root(fpo):
    '''Gets the root of the XML tree.'''
    if fpo:
        tree = et.parse(fpo)
        root = tree.getroot()
        return root
    else:
        raise XmlDmFileError('No file opened!')
