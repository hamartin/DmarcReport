''' DMARC XML parser. '''

import re
import xml.etree.ElementTree as et


def getroot(fpo):
    ''' Gets the root of the XML tree. '''
    tree = et.parse(fpo)
    root = tree.getroot()
    return root


def openxml(filename):
    ''' Opens a file and returns the result. '''
    if filename and not re.match(r'^\s+$', filename):
        return open(filename, 'r')
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
