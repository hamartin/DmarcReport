#!/usr/bin/env python

''' Dmarcparser. A script that will parse DMARC XML files and show the in a
graphical interface. '''

import modules.dmarcparserfront as gui

if __name__ == '__main__':

    GUI = gui.DmarcParserFront()
    GUI.mainloop()
