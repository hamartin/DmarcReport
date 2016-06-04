# -*- coding: UTF-8 -*-
# File name: exceptions.py

'''Dmarc Report exceptions module.'''


class ModelError(Exception):
    '''General model error exception.'''
    pass


class ModelFileError(ModelError):
    '''Model file error exception.'''
    pass
