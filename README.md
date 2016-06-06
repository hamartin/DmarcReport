# Dmarc Report

A simple application to make DMARC XML files human readble. The DMARC XML can
be opened while packaged as a ZIP file as long as the XML is the only file
within that ZIP file.

## Requirements

    1. python-libxml
    2. kivy >= 1.9.1

## Misc

Code testet on Fedora 23 using Python 2.7.11 and Kivy 1.9.1.
I try in all my code to follow the versioning rules described in on
[semver.org][01].

## Repository

There are 3 branches in this repository.

    1. master
    2. kivy
    3. tkinter

The master branch always contains the latest stable of this kivy application.
The kivy branch contains the latest code for this kivy application and the
tkinter branch contains the latest code for the tkinter code when this
application was actively being developed using tkinter instead of kivy.


[01]: http://semver.org/ "Semantic Versioning."
