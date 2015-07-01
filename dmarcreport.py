#!/usr/bin/env python
# -*- coding: latin-1 -*-

# Script that will parse a DMARC report and add it to an SQLite database
# provided it has not been added from before.

import sqlite3
import sys

__author__ = 'Hans Åge Martinsen'
__version__ = '0.1'

class DBHandler:

    def __init__(self, fileName):
        self.db = sqlite3.connect(fileName, isolation_level='immediate')
        self.tableNames = ('policy_published', 'records', 'report_metadata')

        try:
            self._checkDB()
        except Exception:
            self._createDatabase()

    def _checkDB(self):
        c = self.db.cursor()
        t = 'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=?'
        for table in self.tableNames:
            c.execute(t, (table,))
            if c.fetchone() is None:
                raise Exception

    def _createDatabase(self):
        ''' Note that rollback on table creation is not currently supported by
            the default SQLite driver in Python. I have in case this comes
            later prepared for it anyway.
        '''

        c = self.db.cursor()

        # Remove any defined tables that belong to this namespace.
        t = 'DROP TABLE IF EXISTS {0}'
        for table in self.tableNames:
            try:
                c.execute(t.format(table))
            except Exception:
                self.db.rollback()
                raise

        # Create new tables belonging to this namespace.
        t = '''CREATE TABLE policy_published(
                    id INTEGER PRIMARY KEY,
                    domain TEXT,
                    aspf TINYTEXT,
                    adkim TINYTEXT,
                    p TEXT,
                    pct INTEGER DEFAULT NULL)
            '''
        try:
            c.execute(t)
        except Exception:
            self.db.rollback()
            raise

        t = '''CREATE TABLE report_metadata(
                    id INTEGER PRIMARY KEY,
                    organization TEXT,
                    email TEXT,
                    extra_contact_information TEXT,
                    report_id TEXT,
                    date_range_begin INTEGER DEFAULT NULL,
                    date_range_end INTEGER DEFAULT NULL)
            '''
        try:
            c.execute(t)
        except Exception:
            self.db.rollback()
            raise

        t = '''CREATE TABLE records(
                    id INTEGER PRIMARY KEY,
                    source_ip CHAR(15) DEFAULT NULL,
                    count INTEGER DEFAULT NULL,
                    disposition CHAR(11) DEFAULT NULL,
                    dkim CHAR(11) DEFAULT NULL,
                    spf CHAR(11) DEFAULT NULL,
                    type CHAR(20) DEFAULT NULL,
                    comment TEXT,
                    header_from CHAR(255) DEFAULT NULL,
                    dkim_domain CHAR(255) DEFAULT NULL,
                    dkim_result CHAR(11) DEFAULT NULL,
                    dkim_hresult CHAR(255) DEFAULT NULL,
                    spf_domain CHAR(255) DEFAULT NULL,
                    spf_result CHAR(11) DEFAULT NULL,
                    metadata_fk UNSIGNED INTEGER NOT NULL,
                    published_fk UNSIGNED INTEGER NOT NULL,
                    FOREIGN KEY(metadata_fk) REFERENCES report_metadata(id),
                    FOREIGN KEY(published_fk) REFERENCES policy_published(id))
            '''
        try:
            c.execute(t)
        except Exception:
            self.db.rollback()
            raise

        t = 'CREATE INDEX report_metadata_fk ON records (metadata_fk)'
        try:
            c.execute(t)
        except Exception:
            self.db.rollback()
            raise
        t = 'CREATE INDEX policy_published_fk ON records (published_fk)'
        try:
            c.execute(t)
        except Exception:
            self.db.rollback()
            raise

        self.db.commit()


#
# BEGIN
#

if __name__ == '__main__':

    try:
        fileNameDB = sys.argv[1]
        fileNameXML = sys.argv[2]
    except IndexError:
        print 'Example: {0} <DB FILENAME> <XML FILENAME>'.format(sys.argv[0])
        sys.exit(1)

    dbh = DBHandler(fileNameDB)

#
# END
#
