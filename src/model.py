# -*- coding: UTF-8 -*-
# File name: model.py

'''Dmarc Report model module.'''

import zipfile

from xml.etree import ElementTree

from src.exceptions import ModelError


class Model(object):

    '''Dmarc Report model.'''

    def __init__(self):
        super(Model, self).__init__()

        self.filename = None

    def load(self, filename):
        '''Loads the module with data from file.'''
        fpn = None
        if filename and isinstance(filename, str):
            if zipfile.is_zipfile(filename):
                try:
                    fpz = zipfile.ZipFile(filename)
                except IOError:
                    return False
                else:
                    if len(fpz.infolist()) != 1:
                        return False
                    else:
                        zipfp = fpz.infolist()[0]
                        fpn = fpz.open(zipfp)
            else:
                try:
                    fpn = open(filename, 'r')
                except IOError:
                    return False
        else:
            return False

        try:
            self.populate(fpn)
        except ModelError:
            return False
        else:
            return True

    def populate(self, fpn):
        '''Reads the file and populates the NUI.'''
        if not fpn:
            raise ModelError('No file pointer given.')

        root = get_root(fpn)
        fpn.close()
        self.data = parse(root)


def get_root(fpn):
    '''Gets the root of the XML tree.'''
    if not fpn:
        raise ModelError('No file pointer given.')

    tree = ElementTree.parse(fpn)
    root = tree.getroot()
    return root


def parse(root):
    '''Returns a two value tupple with tag and subroot where tag is key
    and subroot is a dictionary.'''
    return root.tag, dict(map(parse, root)) or root.text
