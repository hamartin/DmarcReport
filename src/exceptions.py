# -*- coding: UTF-8 -*-
# File name: exceptions.py

'''
Dmarc Report exceptions module.

Copyright 2016, Hans Åge Martinsen <hamartin@moshwire.com>
'''


class ModelError(Exception):
    '''General model error exception.'''
    pass


class ModelFileError(ModelError):
    '''Model file error exception.'''
    pass
