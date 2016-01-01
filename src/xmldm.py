''' DMARC XML parser. '''

import re
import xml.etree.ElementTree as et
import zipfile


class OpenXMLError(Exception):

    ''' Used when opening zip files fail. '''

    def __init__(self, message):
        super(OpenXMLError, self).__init__(self, message)
        self.message = message

    def __str__(self):
        return self.message


def getroot(fpo):
    ''' Gets the root of the XML tree. '''
    tree = et.parse(fpo)
    root = tree.getroot()
    return root


def openxml(filename):
    ''' Opens a file and returns the result. '''
    if(filename and not re.match(r'^\s+$', filename)
       and not zipfile.is_zipfile(filename)):
        return open(filename, 'r')
    elif(filename and not re.match(r'^\s+$', filename)
         and zipfile.is_zipfile(filename)):
        archive = zipfile.ZipFile(filename)
        if len(archive.infolist()) > 1:
            err = 'xmldm::openxml More than 1 file stored in zip file.'
            raise OpenXMLError(err)
        else:
            zipobj = archive.infolist()[0]
            return archive.open(zipobj)
    else:
        raise Exception('Xml::openxml No filename defined.')


def parse(root):
    ''' Takes the root from an XML tree and parses it. '''
    if len(root) == 0:
        return root.text
    else:
        dic = {}
        for child in root:
            dic[child.tag] = parse(child)
        return dic


def xmldict(filename):
    ''' Parses an XML file and returns the result as a dictionary. '''
    fpo = openxml(filename)
    if fpo:
        root = getroot(fpo)
        fpo.close()
        dic = parse(root)
        return dic
    else:
        raise Exception('Xml::xmldict No file loaded to parse.')
