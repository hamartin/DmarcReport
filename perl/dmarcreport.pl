#!/usr/bin/perl -T -w

use strict;
use warnings;

use DBI;
use Getopt::Std;
use XML::Simple qw(:strict);

my %opts;

my $DEBUG = 0;
my $user = 'default';
my $pass = 'default';
my $dbname = 'dmarcreport.db';

sub help()
{
    my $exampleText = "Example: $0 -f <XMLFILE>  # Must match regex '^.*\\\.xml\$'\n" .
                      "         $0 -c            # Create database in current folder.\n";
    die($exampleText);
}

sub Dump
{
    my $var = shift;
    my $die = shift;

    use Data::Dumper;
    print Dumper($var);
    die("Dying\n") if($die);
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
        id INTEGER PRIMARY KEY,
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

sub addPolicyRecord($%)
{
    my ($dbh, %policy) = @_;

    my $domain = @{$policy{'domain'}}[0];
    my $aspf   = @{$policy{'aspf'}}[0];
    my $adkim  = @{$policy{'adkim'}}[0];
    my $p      = @{$policy{'p'}}[0];
    my $pct    = @{$policy{'pct'}}[0];

    my $sth = $dbh->prepare('INSERT INTO policy_published("domain", "aspf", "adkim", "p", "pct") VALUES(?,?,?,?,?)');
    $sth->execute($domain, $aspf, $adkim, $p, $pct);
    die('ERROR! return code: '.$sth->err.' error msg: '.$sth->errstr."\n") if($sth->err);

    return $dbh->func('last_insert_rowid');
}

sub addReportRecord($%)
{
    my ($dbh, %report) = @_;

    my $organization = @{$report{'org_name'}}[0];
    my $email        = @{$report{'email'}}[0];
    #my $extraCI     = ???
    my $reportID     = @{$report{'report_id'}}[0];
    my %dateRange    = %{@{$report{'date_range'}}[0]};
    my $dateBegin    = @{$dateRange{'begin'}}[0];
    my $dateEnd      = @{$dateRange{'end'}}[0];

    my $sth = $dbh->prepare('SELECT 1 FROM report_metadata WHERE report_id=?');
    $sth->execute($reportID);
    $sth->fetchrow();
    die('ERROR! return code: '.$sth->err.' error msg: '.$sth->errstr."\n") if($sth->err);
    die("Report has already been added to database.\n") if($sth->rows() ne 0 && !$DEBUG);

    $sth = $dbh->prepare('INSERT INTO report_metadata("organization", "email", "extra_contact_information", "report_id", "date_range_begin", "date_range_end") VALUES(?,?,?,?,?,?)');
    $sth->execute($organization, $email, undef, $reportID, $dateBegin, $dateEnd);
    die('ERROR! return code: '.$sth->err.' error msg: '.$sth->errstr."\n") if($sth->err);

    return $dbh->func('last_insert_rowid');
}

sub addRecordRecord($$$%)
{
    my ($dbh, $policyID, $reportID, %record) = @_;

    my %identifiers = %{@{$record{'identifiers'}}[0]};
    my %row = %{@{$record{'row'}}[0]};
    my %policyEvaluated = %{@{$row{'policy_evaluated'}}[0]};
    my %authResults = %{@{$record{'auth_results'}}[0]};
    my %arDKIM = %{@{$authResults{'dkim'}}[0]};
    my %arSPF = %{@{$authResults{'spf'}}[0]};

    my $headerFrom = @{$identifiers{'header_from'}}[0];
    my $count = @{$row{'count'}}[0];
    my $sourceIP = @{$row{'source_ip'}}[0];
    my $disposition = @{$policyEvaluated{'disposition'}}[0];
    my $peDkim = @{$policyEvaluated{'dkim'}}[0];
    my $peSpf = @{$policyEvaluated{'spf'}}[0];
    my $arDkimDomain = @{$arDKIM{'domain'}}[0];
    my $arDkimResult = @{$arDKIM{'result'}}[0];
    my $arSpfDomain = @{$arSPF{'domain'}}[0];
    my $arSpfResult = @{$arSPF{'result'}}[0];
    #my $type             =
    #my $comment          = 
    my $metadataFK       = $reportID;
    my $publishedFK      = $policyID;

    #my $sth = $dbh->prepare('');
    #$sth->execute();
    #die('ERROR! return code: '.$sth->err.' error msg: '.$sth->errstr."\n") if($sth->err);

    #return $dbh->func('last_insert_rowid');

#        id UNSIGNED INTEGER NOT NULL PRIMARY KEY,
#        source_ip CHAR(15) DEFAULT NULL,
#        count INTEGER DEFAULT NULL,
#        disposition CHAR(11) DEFAULT NULL,
#        dkim CHAR(11) DEFAULT NUll,
#        spf CHAR(11) DEFAULT NULL,
#        type CHAR(20) DEFAULT NULL,
#        comment TEXT,
#        header_from CHAR(255) DEFAULT NULL,
#        dkim_domain CHAR(255) DEFAULT NULL,
#        dkim_result CHAR(11) DEFAULT NULL,
#        dkim_hresult CHAR(255) DEFAULT NULL,
#        spf_domain CHAR(255) DEFAULT NULL,
#        spf_result CHAR(11) DEFAULT NULL,
#        metadata_fk UNSIGNED INTEGER NOT NULL,
#        published_fk UNSIGNED INTEGER NOT NULL,
#        FOREIGN KEY(metadata_fk) REFERENCES report_metadata(id),
#        FOREIGN KEY(published_fk) REFERENCES policy_published(id)
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

    my %report = %{ @{ $xmlref->{'report_metadata'} }[0] };
    my %policy = %{ @{ $xmlref->{'policy_published'} }[0] };
    my %record = %{ @{ $xmlref->{'record'} }[0] };

    my $reportID = addReportRecord($dbh, %report);
    my $policyID = addPolicyRecord($dbh, %policy);
    my $recordID = addRecordRecord($dbh, $policyID, $reportID, %record);

    closeDBH($dbh);
}

#
# BEGIN
#

getopts('cdf:', \%opts);

if(defined($opts{'d'})) {
    $DEBUG = 1;
}

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
