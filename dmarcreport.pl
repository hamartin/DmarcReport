#!/usr/bin/perl -T -w

use strict;
use warnings;

use DBI;
use Getopt::Std;
use XML::Simple qw(:strict);

my %opts;
my $user = 'default';
my $pass = 'default';
my $dbname = 'dmarcreport.db';

sub help()
{
    my $exampleText = "Example: $0 -f <XMLFILE>  # Must match regex '^.*\\\.xml\$'\n" .
                      "         $0 -c            # Create database in current folder.\n";
    die($exampleText);
}

sub parseXML($)
{
    my ($fileName) = @_;
    return XMLin($fileName, KeyAttr => 'feedback', ForceArray => 1);
}

sub createDatabase()
{
    my $dbh = DBI->connect(
        "dbi:SQLite:dbname=$dbname",
        $user,
        $pass,
        { RaiseError => 1 }
    ) or die($DBI::errstr);

    $dbh->do('DROP TABLE IF EXISTS policy_published');

    $dbh->do('CREATE TABLE policy_published(
        id UNSIGNED INTEGER NOT NULL PRIMARY KEY,
        domain TEXT,
        aspf TINYTEXT,
        adkim TINYTEXT,
        p TEXT,
        pct INTEGER DEFAULT NULL
        )');

    $dbh->do('CREATE TABLE report_metadata(
        id UNSIGNED INTEGER NOT NULL PRIMARY KEY,
        organization TEXT,
        email TEXT,
        extra_contact_information TEXT,
        report_id TEXT,
        date_range_begin INTEGER DEFAULT NULL,
        date_range_end INTEGER DEFAULT NULL
        )');

    $dbh->do('CREATE TABLE records(
        id UNSIGNED INTEGER NOT NULL PRIMARY KEY,
        source_ip CHAR(15) DEFAULT NULL,
        count INTEGER DEFAULT NULL,
        disposition CHAR(11) DEFAULT NULL,
        dkim CHAR(11) DEFAULT NUll,
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
        FOREIGN KEY(published_fk) REFERENCES policy_published(id)
    )');

    $dbh->do('CREATE INDEX report_metadata_fk ON records (metadata_fk)');
    $dbh->do('CREATE INDEX policy_published_fk ON records (published_fk)');

    $dbh->disconnect();
}

#
# BEGIN
#

getopts('cf:', \%opts);
if(defined($opts{'f'})) {
    if($opts{'f'} =~ m/^(.*\.xml)$/) {
        my $XML = parseXML($1);
    } else {
        help();
    }
} elsif(defined($opts{'c'})) {
    createDatabase();
} else {
    help();
}

#
# END
#
