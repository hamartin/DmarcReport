# -*- coding: UTF-8 -*-

'''Dmarc Parser.'''

import kivy
kivy.require('1.9.1')
import cProfile

from kivy.app import App
from kivy.base import EventLoop

import src.config as cnf
import src.dmarcfront as dmf
import src.xmlmodel as xml


class DmarcReport(App):

    '''Dmarc Parser.'''

    def __init__(self, args, **kwargs):
        super(DmarcReport, self).__init__(**kwargs)
        self.args = args
        self.kv_directory = cnf.KV_DIRECTORY
        self.use_kivy_settings = False

        # Variables used by the application itself.
        self.profile = None
        self.front = dmf.DmarcReportFront()
        self.model = xml.XmlModel()

    def build(self):
        '''Builds Dmarc Report.'''
        self.front.set_footer_message('Ready…')
        return self.front

    def open_settings(self, *largs):
        '''Handles the settings window.'''
        # Hinder the settings window from opening at all.
        pass

    # Profiling stuff.
    def on_start(self):
        '''Does some initial setting of GUI. Also starts a cProfile session.'''
        # Starting cProfile session.
        if self.args.profile:
            self.profile = cProfile.Profile()
            self.profile.enable()
        # Setting new title.
        EventLoop.window.title = cnf.PROGRAM_NAME

    def on_stop(self):
        '''Stops the running profiling session.'''
        # Stopping the cProfile session.
        if self.args.profile:
            self.profile.disable()
            self.profile.dump_stats('{0}.profile'.format(cnf.PROGRAM_NAME))
