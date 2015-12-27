#!/usr/bin/env python

''' DmarcParser.
    A script that will parse DMARC XML files and show the result in a
    Tkinter graphical user interface. '''

import modules.dmarcparserfront as gui

if __name__ == '__main__':

    GUI = gui.DmarcParserFront()
    GUI.mainloop()
