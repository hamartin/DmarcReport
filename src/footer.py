# -*- coding: UTF-8 -*-
# File name: footer.py

'''Dmarc Report footer module'''

import kivy
kivy.require('1.9.1')

from kivy.lang import Builder
from kivy.uix.label import Label

from src import config as cnf
from src.exceptions import FooterError


class Footer(Label):

    '''Dmarc Report Footer class.'''

    def __init__(self, **kwargs):
        # super(Footer, self).__init__(**kwargs)
        Label.__init__(self, **kwargs)
        Builder.load_file('{0}/footer.kv'.format(cnf.KV_DIRECTORY))

    def set_text(self, message):
        '''Sets the footer message.'''
        if isinstance(message, str):
            self.text = message
        else:
            raise FooterError('Message is not of type string!')
