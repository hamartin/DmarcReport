#include "window.h"

Window::Window(QWidget *parent) :
    QWidget(parent)
{
    createDataLabels();
    layout = new QVBoxLayout;

    QLabel      *rmLabel                = createLabel("Report metadata", first);
    QHBoxLayout *rmOrgNameHBox          = createHBox("Org name", firstp, rm_OrgName);
    QHBoxLayout *rmEmailHBox            = createHBox("Email", firstp, rm_Email);
    QHBoxLayout *rmExtraContactInfoHBox = createHBox("Extra contact info", firstp, rm_ExtraContactInfo);
    QHBoxLayout *rmReportIDHBox         = createHBox("Report ID", firstp, rm_ReportID);
    QLabel      *rmDateRangeLabel       = createLabel("Date range", second);
    QHBoxLayout *rmDateRangeBeginHBox   = createHBox("Begin", secondp, rm_DateRangeBegin);
    QHBoxLayout *rmDateRangeEndHBox     = createHBox("End", secondp, rm_DateRangeEnd);

    layout->addWidget(rmLabel);
    layout->addLayout(rmOrgNameHBox);
    layout->addLayout(rmEmailHBox);
    layout->addLayout(rmExtraContactInfoHBox);
    layout->addLayout(rmReportIDHBox);
    layout->addWidget(rmDateRangeLabel);
    layout->addLayout(rmDateRangeBeginHBox);
    layout->addLayout(rmDateRangeEndHBox);

    QLabel      *ppLabel  = createLabel("Policy published", first);
    QHBoxLayout *ppDomain = createHBox("Domain", firstp, pp_Domain);
    QHBoxLayout *ppAdkim  = createHBox("adkim", firstp, pp_Adkim);
    QHBoxLayout *ppAspf   = createHBox("aspf", firstp, pp_Aspf);
    QHBoxLayout *ppP      = createHBox("p", firstp, pp_P);
    QHBoxLayout *ppSp     = createHBox("sp", firstp, pp_Sp);
    QHBoxLayout *ppPct    = createHBox("pct", firstp, pp_Pct);

    layout->addWidget(ppLabel);
    layout->addLayout(ppDomain);
    layout->addLayout(ppAdkim);
    layout->addLayout(ppAspf);
    layout->addLayout(ppP);
    layout->addLayout(ppSp);
    layout->addLayout(ppPct);

    QLabel      *rLabel                   = createLabel("Record", first);
    QLabel      *rRowLabel                = createLabel("Row", second);
    QHBoxLayout *rRowSourceIP             = createHBox("Source IP", secondp, re_SourceIP);
    QHBoxLayout *rRowCount                = createHBox("Count", secondp, re_Count);
    QLabel      *rRowPolicyEvaluatedLabel = createLabel("Policy evaluated", third);
    QHBoxLayout *rRowPEDisposition        = createHBox("Disposition", thirdp, re_Disposition);
    QHBoxLayout *rRowPEDKIM               = createHBox("DKIM", thirdp, re_DKIM);
    QHBoxLayout *rRowPESPF                = createHBox("SPF", thirdp, re_SPF);
    QLabel      *rIdentifiersLabel        = createLabel("Identifiers", second);
    QHBoxLayout *rIHeaderFrom             = createHBox("Header from", secondp, re_HeaderFrom);
    QLabel      *rAuthResultsLabel        = createLabel("Auth results", second);
    QLabel      *rARDKIMLabel             = createLabel("DKIM", third);
    QHBoxLayout *rARDKIMDomain            = createHBox("Domain", thirdp, re_ARDKIMDomain);
    QHBoxLayout *rARDKIMResult            = createHBox("Result", thirdp, re_ARDKIMResult);
    QLabel      *rARSPFLabel              = createLabel("SPF", third);
    QHBoxLayout *rARSPFDomain             = createHBox("Domain", thirdp, re_ARSPFDomain);
    QHBoxLayout *rARSPFResult             = createHBox("Result", thirdp, re_ARSPFResult);

    layout->addWidget(rLabel);
    layout->addWidget(rRowLabel);
    layout->addLayout(rRowSourceIP);
    layout->addLayout(rRowCount);
    layout->addWidget(rRowPolicyEvaluatedLabel);
    layout->addLayout(rRowPEDisposition);
    layout->addLayout(rRowPEDKIM);
    layout->addLayout(rRowPESPF);
    layout->addWidget(rIdentifiersLabel);
    layout->addLayout(rIHeaderFrom);
    layout->addWidget(rAuthResultsLabel);
    layout->addWidget(rARDKIMLabel);
    layout->addLayout(rARDKIMDomain);
    layout->addLayout(rARDKIMResult);
    layout->addWidget(rARSPFLabel);
    layout->addLayout(rARSPFDomain);
    layout->addLayout(rARSPFResult);

    setLayout(layout);
}

Window::~Window()
{
    delete rm_OrgName;
    delete rm_Email;
    delete rm_ExtraContactInfo;
    delete rm_ReportID;
    delete rm_DateRangeBegin;
    delete rm_DateRangeEnd;

    delete pp_Domain;
    delete pp_Adkim;
    delete pp_Aspf;
    delete pp_P;
    delete pp_Sp;
    delete pp_Pct;

    delete re_SourceIP;
    delete re_Count;
    delete re_Disposition;
    delete re_DKIM;
    delete re_SPF;
    delete re_HeaderFrom;
    delete re_ARDKIMDomain;
    delete re_ARDKIMResult;
    delete re_ARSPFDomain;
    delete re_ARSPFResult;

    delete layout;
}

void Window::createDataLabels()
{
    rm_OrgName = createLabel();
    rm_Email = createLabel();
    rm_ExtraContactInfo = createLabel();
    rm_ReportID = createLabel();
    rm_DateRangeBegin = createLabel();
    rm_DateRangeEnd = createLabel();

    pp_Domain = createLabel();
    pp_Adkim = createLabel();
    pp_Aspf = createLabel();
    pp_P = createLabel();
    pp_Sp = createLabel();
    pp_Pct = createLabel();

    re_SourceIP = createLabel();
    re_Count = createLabel();
    re_Disposition = createLabel();
    re_DKIM = createLabel();
    re_SPF = createLabel();
    re_HeaderFrom = createLabel();
    re_ARDKIMDomain = createLabel();
    re_ARDKIMResult = createLabel();
    re_ARSPFDomain = createLabel();
    re_ARSPFResult = createLabel();
}

QLabel *Window::createLabel(const QString &text, const LEVEL &level)
{
    QLabel *label = new QLabel;
    label->setText(text);
    if (level == none)
        return label;
    QFont font = label->font();

    unsigned int size = 9;
    bool bold = false;
    switch(level) {
        case first:   size = 16; bold = true;  break;
        case firstp:  size =  9; bold = false; break;
        case second:  size = 12; bold = true;  break;
        case secondp: size =  9; bold = false; break;
        case third:   size =  9; bold = true;  break;
        case thirdp:  size =  9; bold = false; break;
        case none:    size =  9; bold = false; break;   // It shouldn't be possible for the method to get here when none is specified.
    }

    font.setBold(bold);
    font.setPointSize(size);
    label->setFont(font);
    label->setIndent(level);
    return label;
}

QHBoxLayout *Window::createHBox(const QString &text, const LEVEL &level, QLabel *lbl)
{
    QHBoxLayout *box = new QHBoxLayout;
    QLabel *label = createLabel(text, level);
    box->addWidget(label);
    box->addWidget(lbl);
    return box;
}
