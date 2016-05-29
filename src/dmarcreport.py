# -*- coding: UTF-8 -*-

'''Dmarc Parser.'''

import kivy
kivy.require('1.9.1')
import cProfile

from kivy.app import App
from kivy.base import EventLoop

import src.config as cnf
import src.dmarcfront as dmf


class DmarcReport(App):

    '''Dmarc Parser.'''

    def __init__(self, **kwargs):
        super(DmarcReport, self).__init__(**kwargs)
        self.kv_directory = cnf.KV_DIRECTORY
        self.use_kivy_settings = False

        # Variables used by the application itself.
        self.profile = None

    def build(self):
        '''Builds Dmarc Report.'''
        return dmf.DmarcReportFront()

    def open_settings(self, *largs):
        '''Handles the settings window.'''
        # Hinder the settings window from opening at all.
        pass

    # Profiling stuff.
    def on_start(self):
        '''Does some initial setting of GUI. Also starts a cProfile session.'''
        # Starting cProfile session.
        self.profile = cProfile.Profile()
        self.profile.enable()
        # Setting new title.
        EventLoop.window.title = cnf.PROGRAM_NAME

    def on_stop(self):
        '''Stops the running profiling session.'''
        # Stopping the cProfile session.
        self.profile.disable()
        self.profile.dump_stats('{0}.profile'.format(cnf.PROGRAM_NAME))
