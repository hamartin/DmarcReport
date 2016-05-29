# -*- coding: UTF-8 -*-
# File name: footer.py

'''Dmarc Report footer module.'''

import kivy
kivy.require('1.9.1')

from kivy.lang import Builder
from kivy.uix.label import Label

from src import config as cnf

Builder.load_file('{0}/footer.kv'.format(cnf.KV_DIRECTORY))


class Footer(Label):

    '''Dmarc Report footer.'''
    pass
