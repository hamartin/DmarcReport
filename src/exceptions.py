# -*- coding: UTF-8 -*-
# File name: exceptions.py

'''Dmarc Report exceptions module.'''


class ModelError(Exception):
    '''General Model error exception.'''
    pass


class ModelFileError(ModelError):
    '''Model File error.'''
    pass
