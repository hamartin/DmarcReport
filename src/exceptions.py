# -*- coding: UTF-8 -*-
# File name: exceptions.py

'''Dmarc Report exceptions module.'''


class ModelError(Exception):
    '''Dmarc Report Model general error exception.'''
    pass


class ModelFileError(ModelError):
    '''Dmarc Report Model file error exception.'''
    pass


class GroupsError(Exception):
    '''Dmarc Report Groups general error exception.'''
    pass


class PolicyError(GroupsError):
    '''Dmarc Report Policy general error exception.'''
    pass
