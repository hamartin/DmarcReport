# Dmarc Report

This application will read an DMARC XML file and present it to the user
through a Tkinter graphical user interface.

## Bad programming.

I got so tired of finding good ways to handle the XML etree result from the XML
file that at some point I just decided to let it be as it is now. If you open a
file and then open some other file, the result from the new file will be put on
top of the previous results making everything cluttered.

This can be easily fixed with frames that are "forgotten" and then remade using
the same method I am currently using.. But.. Meh..

## Dependencies

    As far as I am aware, all imports used in this application is by default
    provided with Python.
