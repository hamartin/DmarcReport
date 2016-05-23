# -*- coding: UTF-8 -*-
# File name: footer.py

'''Dmarc Report footer module.'''

import kivy
kivy.require('1.9.1')

from kivy.uix.label import Label

from src.exceptions import FooterError


class Footer(Label):

    '''Dmarc Report footer.'''

    def set_message(self, message):
        '''Sets the footer message.'''
        if isinstance(message, str):
            self.text = message.strip()
        else:
            raise FooterError('The message is not of type str!')
