#ifndef WINDOW_H
#define WINDOW_H

#include <QWidget>
#include <QLabel>
#include <QVBoxLayout>
#include <QLabel>
#include <QFont>

enum LEVEL { first=0, none=1, firstp=10, second=30, secondp=40, third=60, thirdp=70 };

class Window : public QWidget
{
    Q_OBJECT
public:
    explicit Window(QWidget *parent = 0);

    QLabel *rmOrgName;
    QLabel *rmEmail;
    QLabel *rmExtraContactInfo;
    QLabel *rmReportID;
    QLabel *rmDateRangeBegin;
    QLabel *rmDateRangeEnd;

    QLabel *ppDomain;
    QLabel *ppAdkim;
    QLabel *ppAspf;
    QLabel *ppP;
    QLabel *ppSp;
    QLabel *ppPct;

    QLabel *reSourceIP;
    QLabel *reCount;
    QLabel *reDisposition;
    QLabel *reDKIM;
    QLabel *reSPF;
    QLabel *reHeaderFrom;
    QLabel *reARDKIMDomain;
    QLabel *reARDKIMResult;
    QLabel *reARSPFDomain;
    QLabel *reARSPFResult;
    
signals:
    
public slots:

private:
    QLabel *createLabel(const QString &text = "", const LEVEL &level = none);
    QHBoxLayout *createHBox(const QString &text, const LEVEL &level, QLabel *lbl);
    void createDataLabels();

    QWidget *win;
    QVBoxLayout *layout;
};

#endif // WINDOW_H
