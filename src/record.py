# -*- coding: UTF-8 -*-

'''A box containing record information from a DMARC XML.'''

from kivy.uix.boxlayout import BoxLayout

import src.dmarcfrontlabel as dmfl


class Record(BoxLayout):

    '''A box containing the record information from a DMARC XML.'''

    def __init__(self, **kwargs):
        super(Record, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.goo1 = dmfl.DmarcFrontLabel('bar')
        self.goo2 = dmfl.DmarcFrontLabel('testing')
        self.goo3 = dmfl.DmarcFrontLabel('bax')
        self.goo4 = dmfl.DmarcFrontLabel('terror')
        self.add_widget(self.goo1)
        self.add_widget(self.goo2)
        self.add_widget(self.goo3)
        self.add_widget(self.goo4)

        self.goo3.set_value('testing this out.')
