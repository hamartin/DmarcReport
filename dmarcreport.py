#!/usr/bin/env python
# -*- coding: latin-1 -*-

''' Script that will parse a DMARC report and add it to an SQLite database
provided it has not been added from before. '''

import sqlite3
import sys
import xml.sax

__author__ = 'Hans Åge Martinsen'
__version__ = '0.1'


class DBHandler:

    ''' Class that handles SQLite connections for this application. '''

    def __init__(self, filename):
        self.dbh = None
        self.filename = filename
        self.tablenames = ('policy_published', 'records', 'report_metadata')

        self.open()

        try:
            self._checkdb()
        except Exception:
            self._createdatabase()

        self.close()

    def _checkdb(self):
        ''' Check if the tables needed are defined, if not, raises an
            exception. '''
        cursor = self.dbh.cursor()
        tstring = 'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=?'
        for table in self.tablenames:
            cursor.execute(tstring, (table,))
            if cursor.fetchone() is None:
                raise Exception

    def _createdatabase(self):
        ''' Note that rollback on table creation is not currently supported by
            the default SQLite driver in Python. I have in case this comes
            later prepared for it anyway. '''

        cursor = self.dbh.cursor()

        # Remove any defined tables that belong to this namespace.
        tstring = 'DROP TABLE IF EXISTS {0}'
        for table in self.tablenames:
            try:
                cursor.execute(tstring.format(table))
            except Exception:
                self.dbh.rollback()
                raise

        # Create new tables belonging to this namespace.
        tstring = '''CREATE TABLE policy_published(
                    id INTEGER PRIMARY KEY,
                    domain TEXT,
                    aspf TINYTEXT,
                    adkim TINYTEXT,
                    p TEXT,
                    pct INTEGER DEFAULT NULL)
            '''
        try:
            cursor.execute(tstring)
        except Exception:
            self.dbh.rollback()
            raise

        tstring = '''CREATE TABLE report_metadata(
                    id INTEGER PRIMARY KEY,
                    organization TEXT,
                    email TEXT,
                    report_id TEXT,
                    date_range_begin INTEGER DEFAULT NULL,
                    date_range_end INTEGER DEFAULT NULL)
            '''
        try:
            cursor.execute(tstring)
        except Exception:
            self.dbh.rollback()
            raise

        tstring = '''CREATE TABLE records(
                    id INTEGER PRIMARY KEY,
                    source_ip CHAR(15) DEFAULT NULL,
                    count INTEGER DEFAULT NULL,
                    disposition CHAR(11) DEFAULT NULL,
                    dkim CHAR(11) DEFAULT NULL,
                    spf CHAR(11) DEFAULT NULL,
                    header_from CHAR(255) DEFAULT NULL,
                    dkim_domain CHAR(255) DEFAULT NULL,
                    dkim_result CHAR(11) DEFAULT NULL,
                    spf_domain CHAR(255) DEFAULT NULL,
                    spf_result CHAR(11) DEFAULT NULL,
                    metadata_fk UNSIGNED INTEGER NOT NULL,
                    published_fk UNSIGNED INTEGER NOT NULL,
                    FOREIGN KEY(metadata_fk) REFERENCES report_metadata(id),
                    FOREIGN KEY(published_fk) REFERENCES policy_published(id))
            '''
        try:
            cursor.execute(tstring)
        except Exception:
            self.dbh.rollback()
            raise

        tstring = 'CREATE INDEX report_metadata_fk ON records (metadata_fk)'
        try:
            cursor.execute(tstring)
        except Exception:
            self.dbh.rollback()
            raise
        tstring = 'CREATE INDEX policy_published_fk ON records (published_fk)'
        try:
            cursor.execute(tstring)
        except Exception:
            self.dbh.rollback()
            raise

        self.dbh.commit()

    def close(self):
        ''' Closes the SQLite database connection. '''
        self.dbh.close()

    def open(self):
        ''' Opens a connection to the SQLite database specified.'''
        self.dbh = sqlite3.connect(self.filename, isolation_level='immediate')


class XMLParser(xml.sax.ContentHandler):

    ''' Class that parses an XML file passed to it. '''

    def __init__(self, filename):
        self.filename = filename
        self.policypublished = {'domain': None, 'aspf': None, 'adkim': None,
                'p': None, 'pct': None}
        self.reportmetadata = {'organization': None, 'email': None, 'reportid':
                None, 'daterangebegin': None, 'daterangeend': None}
        self.records = {'sourceip': None, 'count': None, 'disposition': None,
                'dkim': None, 'spf': None, 'headerfrom': None, 'dkimdomain':
                None, 'dkimresult': None, 'spfdomain': None, 'spfresult': None,
                'metadatafk': None, 'publishedfk': None}

        self.currentdata = None
        self.priordata = None

        # We create an XML parser.
        self.parser = xml.sax.make_parser()
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.parser.setContentHandler(self)
        self.parser.parse(self.filename)

    def startElement(self, tag, attributes):
        self.currentdata = tag

        # Feedback.
        if tag == 'feedback':
            pass

        # Record
        elif tag == 'record':
            print '==========================================================='
            print 'Parsing records.'
            print '==========================================================='
            self.priordata =  None
        elif tag == 'identifiers' and self.priordata is None:
            print 'Identifiers:'
            self.priordata = 'record'
        elif tag == 'header_from' and self.priordata == 'record':
            self.priordata = 'identifiers'
        elif tag == 'row' and self.priordata is None:
            print 'Row:'
            self.priordata = 'record'
        elif tag == 'policy_evaluated' and self.priordata == 'record':
            print '\tPolicy evaluated:'
            self.priordata = 'row'
        elif tag == 'disposition' and self.priordata == 'row':
            self.priordata = 'policy_evaluated'
        elif tag == 'dkim' and self.priordata == 'row':
            self.priordata = 'policy_evaluated'
        elif tag == 'spf' and self.priordata == 'row':
            self.priordata = 'policy_evaluated'
        elif tag == 'count' and self.priordata == 'record':
            self.priordata = 'row'
        elif tag == 'source_ip' and self.priordata == 'record':
            self.priordata = 'row'
        elif tag == 'auth_results' and self.priordata is None:
            print 'Auth results:'
            self.priordata = 'record'
        elif tag == 'dkim' and self.priordata == 'record':
            print '\tDKIM:'
            self.priordata = 'auth_results'
        elif tag == 'domain' and self.priordata == 'auth_results':
            self.priordata = 'dkim'
        elif tag == 'result' and self.priordata == 'auth_results':
            self.priordata = 'dkim'
        elif tag == 'spf' and self.priordata == 'record':
            print '\tSPF:'
            self.priordata = 'auth_results'
        elif tag == 'domain' and self.priordata == 'auth_results':
            self.priordata = 'spf'
        elif tag == 'result' and self.priordata == 'auth_results':
            self.priordata = 'spf'

        # Report meta data.
        elif tag == 'report_metadata':
            print '==========================================================='
            print 'Parsing report metadata.'
            print '==========================================================='
            self.priordata = None
        elif tag == 'email' and self.priordata is None:
            self.priordata = 'report_metadata'
        elif tag == 'org_name' and self.priordata is None:
            self.priordata = 'report_metadata'
        elif tag == 'date_range' and self.priordata is None:
            self.priordata = 'report_metadata'
        elif tag == 'begin' and self.priordata == 'report_metadata':
            self.priordata = 'date_range'
        elif tag == 'end' and self.priordata == 'report_metadata':
            self.priordata = 'date_range'
        elif tag == 'report_id' and self.priordata is None:
            self.priordata = 'report_metadata'

        # Policy published.
        elif tag == 'policy_published':
            print '==========================================================='
            print 'Parsing policy published.'
            print '==========================================================='
            self.priordata = None
        elif tag == 'pct' and self.priordata is None:
            self.priordata = 'policy_published'
        elif tag == 'sp' and self.priordata is None:
            self.priordata = 'policy_published'
        elif tag == 'p' and self.priordata is None:
            self.priordata = 'policy_published'
        elif tag == 'adkim' and self.priordata is None:
            self.priordata = 'policy_published'
        elif tag == 'domain' and self.priordata is None:
            self.priordata = 'policy_published'
        elif tag == 'aspf' and self.priordata is None:
            self.priordata = 'policy_published'

        else:
            print '***********************************************************'
            print 'Something went wrong.'
            print 'Tag: {0}'.format(tag)
            print 'Current: {0}'.format(self.currentdata)
            print 'Prior: {0}'.format(self.priordata)
            print '***********************************************************'

    def endElement(self, tag):

        # Feedback.
        if tag == 'feedback':
            pass

        # Record.
        elif tag == 'record':
            self.priordata = None
        elif tag == 'identifiers' and self.priordata == 'record':
            self.priordata = None
        elif tag == 'header_from' and self.priordata == 'identifiers':
            print '\tHeader From:', self.records['headerfrom']
            self.priordata = 'record'
        elif tag == 'row' and self.priordata == 'record':
            self.priordata = None
        elif tag == 'policy_evaluated' and self.priordata == 'row':
            self.priordata = 'record'
        elif tag == 'disposition' and self.priordata == 'policy_evaluated':
            print '\t\tDisposition:', self.records['disposition']
            self.priordata = 'row'
        elif tag == 'dkim' and self.priordata == 'policy_evaluated':
            print '\t\tDKIM:', self.records['dkim']
            self.priordata = 'row'
        elif tag == 'spf' and self.priordata == 'policy_evaluated':
            print '\t\tSPF:', self.records['spf']
            self.priordata = 'row'
        elif tag == 'count' and self.priordata == 'row':
            print '\tCount:', self.records['count']
            self.priordata = 'record'
        elif tag == 'source_ip' and self.priordata == 'row':
            print '\tSource IP:', self.records['sourceip']
            self.priordata = 'record'
        elif tag == 'auth_results' and self.priordata == 'record':
            self.priordata = None
        elif tag == 'dkim' and self.priordata == 'auth_results':
            self.priordata = 'record'
        elif tag == 'domain' and self.priordata == 'dkim':
            print '\t\tDomain:', self.records['dkimdomain']
            self.priordata = 'auth_results'
        elif tag == 'result' and self.priordata == 'dkim':
            print '\t\tResult:', self.records['dkimresult']
            self.priordata = 'auth_results'
        elif tag == 'spf' and self.priordata == 'auth_results':
            self.priordata = 'record'
        elif tag == 'domain' and self.priordata == 'spf':
            print '\t\tDomain:', self.records['spfdomain']
            self.priordata = 'auth_results'
        elif tag == 'result' and self.priordata == 'spf':
            print '\t\tResult:', self.records['spfresult']
            self.priordata = 'auth_results'

        # Report meta data.
        elif tag == 'report_metadata':
            self.priordata = None
        elif tag == 'email' and self.priordata == 'report_metadata':
            print 'Email:', self.reportmetadata['email']
            self.priordata = None
        elif tag == 'org_name' and self.priordata == 'report_metadata':
            print 'Organization:', self.reportmetadata['organization']
            self.priordata = None
        elif tag == 'date_range' and self.priordata == 'report_metadata':
            print 'Date range:'
            print '\tBegin:', self.reportmetadata['daterangebegin']
            print '\tEnd:', self.reportmetadata['daterangeend']
            self.priordata = None
        elif tag == 'begin' and self.priordata == 'date_range':
            self.priordata = 'report_metadata'
        elif tag == 'end' and self.priordata == 'date_range':
            self.priordata = 'report_metadata'
        elif tag == 'report_id' and self.priordata == 'report_metadata':
            print 'Report ID:', self.reportmetadata['reportid']
            self.priordata = None

        # Policy published.
        elif tag == 'policy_published' and self.priordata is None:
            self.priordata = None
        elif tag == 'domain' and self.priordata == 'policy_published':
            print 'Domain:', self.policypublished['domain']
            self.priordata = None
        elif tag == 'adkim' and self.priordata == 'policy_published':
            print 'ADKIM:', self.policypublished['adkim']
            self.priordata = None
        elif tag == 'aspf' and self.priordata == 'policy_published':
            print 'ASPF:', self.policypublished['aspf']
            self.priordata = None
        elif tag == 'p' and self.priordata == 'policy_published':
            print 'P:', self.policypublished['p']
            self.priordata = None
        elif tag == 'sp' and self.priordata == 'policy_published':
            print 'SP:', self.policypublished['sp']
            self.priordata = None
        elif tag == 'pct' and self.priordata == 'policy_published':
            print 'PCT:', self.policypublished['pct']
            self.priordata = None

        else:
            print '***********************************************************'
            print 'Something went wrong.'
            print 'Tag: {0}'.format(tag)
            print 'Current: {0}'.format(self.currentdata)
            print 'Prior: {0}'.format(self.priordata)
            print '***********************************************************'

    def characters(self, content):

        # Feedback.
        if self.currentdata == 'feedback':
            pass

        # Report meta data.
        elif self.currentdata == 'org_name' and self.priordata == 'report_metadata':
            self.reportmetadata['organization'] = content
        elif self.currentdata == 'email' and self.priordata == 'report_metadata':
            self.reportmetadata['email'] = content
        elif self.currentdata == 'report_id' and self.priordata == 'report_metadata':
            self.reportmetadata['reportid'] = content
        elif self.currentdata == 'begin' and self.priordata == 'date_range':
            self.reportmetadata['daterangebegin'] = content
        elif self.currentdata == 'end' and self.priordata == 'date_range':
            self.reportmetadata['daterangeend'] = content

        # Policy published.
        elif self.currentdata == 'domain' and self.priordata == 'policy_published':
            self.policypublished['domain'] = content
        elif self.currentdata == 'adkim' and self.priordata == 'policy_published':
            self.policypublished['adkim'] = content
        elif self.currentdata == 'aspf' and self.priordata == 'policy_published':
            self.policypublished['aspf'] = content
        elif self.currentdata == 'p' and self.priordata == 'policy_published':
            self.policypublished['p'] = content
        elif self.currentdata == 'sp' and self.priordata == 'policy_published':
            self.policypublished['sp'] = content
        elif self.currentdata == 'pct' and self.priordata == 'policy_published':
            self.policypublished['pct'] = content

        # Records.
        elif self.currentdata == 'source_ip' and self.priordata == 'row':
            self.records['sourceip'] = content
        elif self.currentdata == 'count' and self.priordata == 'row':
            self.records['count'] = content
        elif self.currentdata == 'domain' and self.priordata == 'dkim':
            self.records['dkimdomain'] = content
        elif self.currentdata == 'domain' and self.priordata == 'spf':
            self.records['spfdomain'] = content
        elif self.currentdata == 'result' and self.priordata == 'dkim':
            self.records['dkimresult'] = content
        elif self.currentdata == 'result' and self.priordata == 'spf':
            self.records['spfresult'] = content
        elif self.currentdata == 'header_from' and self.priordata == 'identifiers':
            self.records['headerfrom'] = content
        elif self.currentdata == 'spf' and self.priordata == 'policy_evaluated':
            self.records['spf'] = content
        elif self.currentdata == 'dkim' and self.priordata == 'policy_evaluated':
            self.records['dkim'] = content
        elif self.currentdata == 'disposition' and self.priordata == 'policy_evaluated':
            self.records['disposition'] = content

        else:
            print '***********************************************************'
            print 'Something went wrong.'
            print 'Tag: {0}'.format(tag)
            print 'Current: {0}'.format(self.currentdata)
            print 'Prior: {0}'.format(self.priordata)
            print '***********************************************************'


#
# BEGIN
#

if __name__ == '__main__':

    try:
        FILENAMEDB = sys.argv[1]
        FILENAMEXML = sys.argv[2]
    except IndexError:
        print 'Example: {0} <DB FILENAME> <XML FILENAME>'.format(sys.argv[0])
        sys.exit(1)

    DBH = DBHandler(FILENAMEDB)
    XML = XMLParser(FILENAMEXML)
    DBH.close()

#
# END
#
