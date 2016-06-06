# -*- coding: UTF-8 -*-
# File name: model.py

'''
Dmarc Report model module.

Copyright 2016, Hans Åge Martinsen <hamartin@moshwire.com>

    This file is part of Dmarc Report.

    Dmarc Report is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Dmarc Report is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Dmarc Report.  If not, see <http://www.gnu.org/licenses/>
'''

import zipfile

from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError

from src.exceptions import ModelError, ModelFileError


class Model(object):

    '''Dmarc Report model.'''

    def __init__(self, **kwargs):
        # super(Model, self).__init__()
        object.__init__(self, **kwargs)

        self.filename = None
        self.data = None

    def load(self, filename):
        '''Loads the module with data from file.'''
        fpn = None
        if filename and isinstance(filename, str):
            if zipfile.is_zipfile(filename):
                try:
                    fpz = zipfile.ZipFile(filename)
                except IOError, err:
                    raise ModelFileError(err)
                else:
                    if len(fpz.infolist()) != 1:
                        raise ModelFileError(
                            'Zip file does not contain just 1 file!')
                    else:
                        zipfp = fpz.infolist()[0]
                        fpn = fpz.open(zipfp)
            else:
                try:
                    fpn = open(filename, 'r')
                except IOError, err:
                    raise ModelFileError(err)
        else:
            raise ModelFileError('File name is not ok')

        self.populate(fpn)
        self.filename = filename

    def populate(self, fpn):
        '''Reads the file and populates the NUI.'''
        if not fpn:
            raise ModelError('No file pointer given.')

        root = get_root(fpn)
        fpn.close()
        self.data = parse(root)

    def get_pol(self, attr):
        '''Returns the attr value for policy report.'''
        try:
            pol = self.data[1]['policy_published']
            return pol[attr]
        except (KeyError, TypeError):
            return 'N/A'

    def get_rep(self, attr, sub=None):
        '''Returns the attr value for report metadata.'''
        try:
            rep = self.data[1]['report_metadata']
            if not sub:
                return rep[attr]
            else:
                return rep[sub][attr]
        except (KeyError, TypeError):
            return 'N/A'

    def get_rec(self, attr, sub=None, subsub=None):
        '''Returns the attr value for record.'''
        try:
            rec = self.data[1]['record']
            if sub and subsub:
                return rec[sub][subsub][attr]
            elif sub:
                return rec[sub][attr]
            else:
                return rec[attr]
        except (KeyError, TypeError):
            return 'N/A'


def get_root(fpn):
    '''Gets the root of the XML tree.'''
    if not fpn:
        raise ModelError('No file pointer given.')

    try:
        tree = ElementTree.parse(fpn)
    except ParseError, err:
        raise ModelError(err)
    root = tree.getroot()
    return root


def parse(root):
    '''Returns a two value tupple with tag and subroot where tag is key
    and subroot is a dictionary.'''
    return root.tag, dict(map(parse, root)) or root.text
