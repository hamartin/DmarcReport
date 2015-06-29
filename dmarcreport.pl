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

sub openDBH()
{
    return DBI->connect(
        "dbi:SQLite:dbname=$dbname",
        $user,
        $pass,
        { RaiseError => 1 }
    ) or die($DBI::errstr);
}

sub closeDBH($)
{
    my ($dbh) = @_;
    $dbh->disconnect();
}

sub createDatabase()
{
    my $dbh = openDBH();

    $dbh->do('DROP TABLE IF EXISTS policy_published');

    $dbh->do('CREATE TABLE policy_published(
        id INTEGER PRIMARY KEY,
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

    closeDBH($dbh);
}

sub _addPolicyRecord($%)
{
    my ($dbh, %policy) = @_;

    my $sth = $dbh->prepare('INSERT INTO policy_published("domain", "aspf", "adkim", "p", "pct") VALUES(?,?,?,?,?)');
    $sth->execute(@{$policy{'domain'}}[0], @{$policy{'aspf'}}[0], @{$policy{'adkim'}}[0], @{$policy{'p'}}[0], @{$policy{'pct'}}[0]);
    return $dbh->func('last_insert_rowid');
}

sub _addReportRecord($%)
{
    my ($dbh, %report) = @_;
    my $sth = $dbh->prepare('INSERT INTO report_metadata("organization", "email", "extra_contact_information", "report_id", "date_range_begin", "date_range_end") VALUES(?,?,?,?,?,?)');
    $sth->execute(@{$report{'org_name'}}[0], @{$report{'email'}}[0], , @{$report{'report_id'}}[0], @{%{@{$report{'date_range'}}[0]}{'begin'}}[0], @{%{@{$report{'date_range'}}[0]}{'end'}}[0]);
    return $dbh->func('last_insert_rowid');
}

sub _addRecordRecord($$$%)
{
    my ($dbh, $policyID, $reportID, %record) = @_;
}

sub addReport($)
{
    my ($xmlref) = @_;
    my $dbh = openDBH();

    # Check if database exists before trying to add data to nothing.
    my @tables = ('policy_published', 'report_metadata', 'records');
    foreach my $table (@tables) {
        my $sth = $dbh->prepare('SELECT name FROM sqlite_master WHERE type="table" AND name=?');
        $sth->execute($table);
        my ($name) = $sth->fetchrow();
        if(!defined($name)) {
            die("Could not find table $table.\nPlease create database first.\n");
        }
    }

    my %policy = %{ @{ $xmlref->{'policy_published'} }[0] };
    my %report = %{ @{ $xmlref->{'report_metadata'} }[0] };
    my %record = %{ @{ $xmlref->{'record'} }[0] };

    my $policyID = _addPolicyRecord($dbh, %policy);
    my $reportID = _addReportRecord($dbh, %report);
    _addRecordRecord($dbh, $policyID, $reportID, %record);

    closeDBH($dbh);
}

#
# BEGIN
#

getopts('cf:', \%opts);
if(defined($opts{'f'})) {
    if($opts{'f'} =~ m/^(.*\.xml)$/) {
        my $xml = parseXML($1);
        addReport($xml);
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
