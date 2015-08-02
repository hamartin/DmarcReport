#-------------------------------------------------
#
# Project created by QtCreator 2015-07-30T09:54:12
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = DmarcReport
TEMPLATE = app


SOURCES += main.cpp\
        dmarcreport.cpp \
    xmldmarcparser.cpp \
    window.cpp

HEADERS  += dmarcreport.h \
    xmldmarcparser.h \
    window.h

FORMS    += dmarcreport.ui
