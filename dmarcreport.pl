#!/usr/bin/perl -T -w

use strict;
use warnings;

use DBI;
use XML::Simple;

#
# Statics.
#

my $uid  = 'STATIC';
my $pwd  = 'STATIC';

#
# Functions.
#

sub openDB($$$)
{
    my ($db, $uid, $pwd) = @_;
    my $dsn = "dbi:SQLite:dbname=$db";
    my $dbh = DBI->connect($dsn, $uid, $pwd, { RaiseError => 1 }) or die("$DBI::errstr");
    return $dbh;
}

sub closeDB($)
{
    my ($dbh) = @_;
    $dbh->disconnect;
}

sub createDB($$$)
{
    my ($db, $uid, $pwd) = @_;
    my $dbh = openDB($db, $uid, $pwd);
    my $sth = $dbh->prepare("CREATE TABLE dmarcreport") or die("$DBI::errstr");
    $sth->execute() or die("$DBI::errstr");
    closeDB($dbh);
}

#
# Start of script.
#

if($#ARGV+1 ne 2) {
    print "Example: $0 <FILE> <DB>\n";
    print "         $0 CREATE <DB>\n";
    exit(0);
}

if(uc($ARGV[0]) =~ m/^CREATE$/) {
    createDB($ARGV[1], $uid, $pwd);
    exit(0);
}













my $file = $ARGV[0];
my $db   = $ARGV[1];

my $xml = new XML::Simple;
my $data = $xml->XMLin($file);


use Data::Dumper;
print Dumper($data);
