''' DMARC XML parser. '''

import re
import xml.etree.ElementTree as et


def xml(filename):
    ''' Parses an XML file and returns the result. '''
    if filename and not re.match('^\s+$', filename):
        fp = open(filename, 'r')
    else:
        raise Exception('Xml::xml No filename defined.')

    if fp:
        ret = et.parse(fp)
        fp.close()
        return ret
    else:
        raise Exception('Xml::xml No file loaded to parse.')
