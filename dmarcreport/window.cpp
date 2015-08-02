#include "window.h"

Window::Window(QWidget *parent) :
    QWidget(parent)
{
    createDataLabels();
    this->layout = new QVBoxLayout;

    QLabel      *rmLabel                = createLabel("Report metadata", first);
    QHBoxLayout *rmOrgNameHBox          = createHBox("Org name", firstp, this->rmOrgName);
    QHBoxLayout *rmEmailHBox            = createHBox("Email", firstp, this->rmEmail);
    QHBoxLayout *rmExtraContactInfoHBox = createHBox("Extra contact info", firstp, this->rmExtraContactInfo);
    QHBoxLayout *rmReportIDHBox         = createHBox("Report ID", firstp, this->rmReportID);
    QLabel      *rmDateRangeLabel       = createLabel("Date range", second);
    QHBoxLayout *rmDateRangeBeginHBox   = createHBox("Begin", secondp, this->rmDateRangeBegin);
    QHBoxLayout *rmDateRangeEndHBox     = createHBox("End", secondp, this->rmDateRangeEnd);

    layout->addWidget(rmLabel);
    layout->addLayout(rmOrgNameHBox);
    layout->addLayout(rmEmailHBox);
    layout->addLayout(rmExtraContactInfoHBox);
    layout->addLayout(rmReportIDHBox);
    layout->addWidget(rmDateRangeLabel);
    layout->addLayout(rmDateRangeBeginHBox);
    layout->addLayout(rmDateRangeEndHBox);

    QLabel      *ppLabel  = createLabel("Policy published", first);
    QHBoxLayout *ppDomain = createHBox("Domain", firstp, this->ppDomain);
    QHBoxLayout *ppAdkim  = createHBox("adkim", firstp, this->ppAdkim);
    QHBoxLayout *ppAspf   = createHBox("aspf", firstp, this->ppAspf);
    QHBoxLayout *ppP      = createHBox("p", firstp, this->ppP);
    QHBoxLayout *ppSp     = createHBox("sp", firstp, this->ppSp);
    QHBoxLayout *ppPct    = createHBox("pct", firstp, this->ppPct);

    layout->addWidget(ppLabel);
    layout->addLayout(ppDomain);
    layout->addLayout(ppAdkim);
    layout->addLayout(ppAspf);
    layout->addLayout(ppP);
    layout->addLayout(ppSp);
    layout->addLayout(ppPct);

    QLabel      *rLabel                   = createLabel("Record", first);
    QLabel      *rRowLabel                = createLabel("Row", second);
    QHBoxLayout *rRowSourceIP             = createHBox("Source IP", secondp, this->reSourceIP);
    QHBoxLayout *rRowCount                = createHBox("Count", secondp, this->reCount);
    QLabel      *rRowPolicyEvaluatedLabel = createLabel("Policy evaluated", third);
    QHBoxLayout *rRowPEDisposition        = createHBox("Disposition", thirdp, this->reDisposition);
    QHBoxLayout *rRowPEDKIM               = createHBox("DKIM", thirdp, this->reDKIM);
    QHBoxLayout *rRowPESPF                = createHBox("SPF", thirdp, this->reSPF);
    QLabel      *rIdentifiersLabel        = createLabel("Identifiers", second);
    QHBoxLayout *rIHeaderFrom             = createHBox("Header from", secondp, this->reHeaderFrom);
    QLabel      *rAuthResultsLabel        = createLabel("Auth results", second);
    QLabel      *rARDKIMLabel             = createLabel("DKIM", third);
    QHBoxLayout *rARDKIMDomain            = createHBox("Domain", thirdp, this->reARDKIMDomain);
    QHBoxLayout *rARDKIMResult            = createHBox("Result", thirdp, this->reARDKIMResult);
    QLabel      *rARSPFLabel              = createLabel("SPF", third);
    QHBoxLayout *rARSPFDomain             = createHBox("Domain", thirdp, this->reARSPFDomain);
    QHBoxLayout *rARSPFResult             = createHBox("Result", thirdp, this->reARSPFResult);

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

    this->setLayout(layout);
}

void Window::createDataLabels()
{
    this->rmOrgName = createLabel();
    this->rmOrgName->setText("Dette");
    this->rmEmail = createLabel();
    this->rmEmail->setText("er");
    this->rmExtraContactInfo = createLabel();
    this->rmExtraContactInfo->setText("en");
    this->rmReportID = createLabel();
    this->rmReportID->setText("test");
    this->rmDateRangeBegin = createLabel();
    this->rmDateRangeBegin->setText("uten");
    this->rmDateRangeEnd = createLabel();
    this->rmDateRangeEnd->setText("like.");

    this->ppDomain = createLabel();
    this->ppAdkim = createLabel();
    this->ppAspf = createLabel();
    this->ppP = createLabel();
    this->ppSp = createLabel();
    this->ppPct = createLabel();

    this->reSourceIP = createLabel();
    this->reCount = createLabel();
    this->reDisposition = createLabel();
    this->reDKIM = createLabel();
    this->reSPF = createLabel();
    this->reHeaderFrom = createLabel();
    this->reARDKIMDomain = createLabel();
    this->reARDKIMResult = createLabel();
    this->reARSPFDomain = createLabel();
    this->reARSPFResult = createLabel();
}

QLabel *Window::createLabel(const QString &text, const LEVEL &level)
{
    QLabel *label = new QLabel;
    label->setText(text);
    if (level == none)
        return label;
    QFont font = label->font();

    unsigned int size;
    bool bold;
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
