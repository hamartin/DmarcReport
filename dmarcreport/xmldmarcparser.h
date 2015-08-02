#ifndef XMLDMARCPARSER_H
#define XMLDMARCPARSER_H
#define DEBUG

#include <QFile>
#include <QXmlStreamReader>

#ifdef DEBUG
#include <QDebug>
#endif

class XmlDmarcParser
{
public:
    XmlDmarcParser(QFile *fp);
    ~XmlDmarcParser();
    void read();

    struct reportMetaData_t {
        QString orgName;
        QString email;
        QString extraContactInfo;
        QString reportID;
        reportMetaData_t() {
            orgName          = "";
            email            = "";
            extraContactInfo = "";
            reportID         = "";
        }
        struct dateRange_t {
            unsigned long begin;
            unsigned long end;
            dateRange_t() {
                begin = 0;
                end = 0;
            }
        } dateRange;
    };

    struct policyPublished_t {
        QString domain;
        QString adkim;
        QString aspf;
        QString p;
        QString sp;
        int pct;
        policyPublished_t()
        {
            domain = "";
            adkim  = "";
            aspf   = "";
            p      = "";
            sp     = "";
            pct    = 0;
        }
    };

    struct record_t {
        struct row_t {
            QString sourceIP;
            unsigned long count;
            row_t() {
                sourceIP = "";
                count = 0;
            }
            struct policyEvaluated_t {
                QString disposition;
                QString dkim;
                QString spf;
                policyEvaluated_t() {
                    disposition = "";
                    dkim = "";
                    spf = "";
                }
            } policyEvaluated;
        } row;
        struct identifiers_t {
            QString headerFrom;
            identifiers_t()
            {
                headerFrom = "";
            }
        } identifiers;
        struct authResults_t{
            struct authSPF_t {
                QString domain;
                QString result;
                authSPF_t()
                {
                    domain = "";
                    result = "";
                }
            } spf;
            struct authDKIM_t{
                QString domain;
                QString result;
                authDKIM_t()
                {
                    domain = "";
                    result = "";
                }
            } dkim;
        } authResults;
    };


    reportMetaData_t    *rep;
    policyPublished_t   *pol;
    record_t            *rec;

private:
    void processFeedback();
    void processDateRange();
    void processReportMetadata();
    void processPolicyPublished();
    void processRecord();
    void processRow();
    void processPolicyEvaluated();
    void processIdentifiers();
    void processAuthResults();
    void processSPF();
    void processDKIM();

    void debug();
    void debugUnknownElement();

    QString readNextText();
    unsigned long readNextULong();
    int readNextInt();

    QXmlStreamReader    *xml;
};

#endif // XMLDMARCPARSER_H
