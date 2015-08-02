#include "xmldmarcparser.h"

XmlDmarcParser::XmlDmarcParser(QFile *fp)
{
    if(fp == NULL)
        return;

    xml = new QXmlStreamReader;
    xml->setDevice(fp);

    rep = new reportMetaData_t;
    pol = new policyPublished_t;
    rec = new record_t;
}

XmlDmarcParser::~XmlDmarcParser()
{
    if (xml && xml->device()) {
        if (xml->tokenType() == QXmlStreamReader::Invalid)
            xml->readNext();
        if (xml->hasError())
            xml->raiseError();
    }
    if (xml)
        delete xml;
    if (rep)
        delete rep;
    if (pol)
        delete pol;
    if (rec)
        delete rec;
}

void XmlDmarcParser::debug()
{
    qDebug() << "Report Metadata";
    qDebug() << "  Org Name:           " << rep->orgName;
    qDebug() << "  Email:              " << rep->email;
    qDebug() << "  Extra contact info: " << rep->extraContactInfo;
    qDebug() << "  Report ID:          " << rep->reportID;
    qDebug() << "  Date range";
    qDebug() << "    Begin:            " << rep->dateRange.begin;
    qDebug() << "    End:              " << rep->dateRange.end;
    qDebug() << "Policy Published";
    qDebug() << "  Domain:             " << pol->domain;
    qDebug() << "  adkim:              " << pol->adkim;
    qDebug() << "  aspf:               " << pol->aspf;
    qDebug() << "  p:                  " << pol->p;
    qDebug() << "  sp:                 " << pol->sp;
    qDebug() << "  pct:                " << pol->pct;
    qDebug() << "Record";
    qDebug() << "  Row";
    qDebug() << "    Source IP:        " << rec->row.sourceIP;
    qDebug() << "    Count:            " << rec->row.count;
    qDebug() << "    Policy Evaluated";
    qDebug() << "      Disposition:    " << rec->row.policyEvaluated.disposition;
    qDebug() << "      DKIM:           " << rec->row.policyEvaluated.dkim;
    qDebug() << "      SPF:            " << rec->row.policyEvaluated.spf;
    qDebug() << "  Identifiers";
    qDebug() << "    Header from:      " << rec->identifiers.headerFrom;
    qDebug() << "  Auth Results";
    qDebug() << "    SPF";
    qDebug() << "      Domain:         " << rec->authResults.spf.domain;
    qDebug() << "      Result:         " << rec->authResults.spf.result;
    qDebug() << "    DKIM";
    qDebug() << "      Domain:         " << rec->authResults.dkim.domain;
    qDebug() << "      Result:         " << rec->authResults.dkim.result;
}

void XmlDmarcParser::debugUnknownElement()
{
    QString name = xml->name().toString();
    QString value = xml->readElementText();
    qDebug() << "Unknown element: " << name;
    qDebug() << "  Value: " << value;
}

QString XmlDmarcParser::readNextText()
{
    return xml->readElementText();
}

int XmlDmarcParser::readNextInt()
{
    bool ok;
    QString textInput = xml->readElementText();
    int intInput = textInput.toInt(&ok);
    if(ok)
        return intInput;
    xml->raiseError("Could not convert text to int.");
    return 0; // This is redundant but has to be in the function to avoid compiler issues.
}

unsigned long XmlDmarcParser::readNextULong()
{
    bool ok;
    QString textInput = xml->readElementText();
    unsigned long ulongInput = textInput.toULong(&ok);
    if(ok)
        return ulongInput;
    xml->raiseError("Could not convert text to unsigned long.");
    return 0; // This is redundant but has to be in the function to avoid compiler issues.
}

void XmlDmarcParser::read()
{
    if (xml == NULL)
        return;
    if (rec) {
        delete rec;
        rec = new record_t;
    }
    if (pol) {
        delete pol;
        pol = new policyPublished_t;
    }
    if (rep) {
        delete rep;
        rep = new reportMetaData_t;
    }
    if (xml->readNextStartElement() && xml->name() == "feedback")
        processFeedback();
    if (xml->tokenType() == QXmlStreamReader::Invalid)
        xml->readNext();
    if (xml->hasError())
        xml->raiseError();

    // Debugging information.
#ifdef DEBUG
    debug();
#endif
}

void XmlDmarcParser::processFeedback()
{
    if (!xml->isStartElement() || xml->name() != "feedback")
            return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "report_metadata") {
            processReportMetadata();
        } else if (xml->name() == "policy_published") {
            processPolicyPublished();
        } else if (xml->name() == "record") {
            processRecord();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif
        }
    }
}

void XmlDmarcParser::processReportMetadata()
{
    if (!xml->isStartElement() || xml->name() != "report_metadata")
        return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "org_name") {
            rep->orgName = readNextText();
        } else if (xml->name() == "email") {
            rep->email = readNextText();
        } else if (xml->name() == "extra_contact_info") {
            rep->extraContactInfo = readNextText();
        } else if (xml->name() == "report_id") {
            rep->reportID = readNextText();
        } else if (xml->name() == "date_range") {
            processDateRange();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif
        }
    }
}

void XmlDmarcParser::processDateRange()
{
    if (!xml->isStartElement() || xml->name() != "date_range")
        return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "begin") {
            rep->dateRange.begin = readNextULong();
        } else if (xml->name() == "end") {
            rep->dateRange.end = readNextULong();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif
        }
    }
}

void XmlDmarcParser::processPolicyPublished()
{
    if (!xml->isStartElement() || xml->name() != "policy_published")
        return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "domain") {
            pol->domain = readNextText();
        } else if (xml->name() == "adkim") {
            pol->adkim = readNextText();
        } else if (xml->name() == "aspf") {
            pol->aspf = readNextText();
        } else if (xml->name() == "p") {
            pol->p = readNextText();
        } else if (xml->name() == "sp") {
            pol->sp = readNextText();
        } else if (xml->name() == "pct") {
            pol->pct = readNextInt();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif
        }
    }
}

void XmlDmarcParser::processRecord()
{
    if (!xml->isStartElement() || xml->name() != "record")
        return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "row") {
            processRow();
        } else if (xml->name() == "identifiers") {
            processIdentifiers();
        } else if (xml->name() == "auth_results") {
            processAuthResults();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif
        }
    }
}

void XmlDmarcParser::processRow()
{
    if (!xml->isStartElement() || xml->name() != "row")
        return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "source_ip") {
            rec->row.sourceIP = readNextText();
        } else if (xml->name() == "count") {
            rec->row.count = readNextULong();
        } else if (xml->name() == "policy_evaluated") {
            processPolicyEvaluated();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif
        }
    }
}

void XmlDmarcParser::processPolicyEvaluated()
{
    if (!xml->isStartElement() || xml->name() != "policy_evaluated")
        return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "disposition") {
            rec->row.policyEvaluated.disposition = readNextText();
        } else if (xml->name() == "dkim") {
            rec->row.policyEvaluated.dkim = readNextText();
        } else if (xml->name() == "spf") {
            rec->row.policyEvaluated.spf = readNextText();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif            
        }
    }
}

void XmlDmarcParser::processIdentifiers()
{
    if (!xml->isStartElement() || xml->name() != "identifiers")
        return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "header_from") {
            rec->identifiers.headerFrom = readNextText();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif            
        }
    }
}

void XmlDmarcParser::processAuthResults()
{
    if (!xml->isStartElement() || xml->name() != "auth_results")
        return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "spf") {
            processSPF();
        } else if (xml->name() == "dkim") {
            processDKIM();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif            
        }
    }
}

void XmlDmarcParser::processSPF()
{
    if (!xml->isStartElement() || xml->name() != "spf")
        return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "domain") {
            rec->authResults.spf.domain = readNextText();
        } else if (xml->name() == "result") {
            rec->authResults.spf.result = readNextText();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif        
        }
    }
}

void XmlDmarcParser::processDKIM()
{
    if (!xml->isStartElement() || xml->name() != "dkim")
        return;

    while (xml->readNextStartElement()) {
        if (xml->name() == "domain") {
            rec->authResults.dkim.domain = readNextText();
        } else if (xml->name() == "result") {
            rec->authResults.dkim.result = readNextText();
#ifdef DEBUG
        } else {
            debugUnknownElement();
#endif            
        }
    }
}
