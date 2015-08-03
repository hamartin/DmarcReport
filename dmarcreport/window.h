#ifndef WINDOW_H
#define WINDOW_H

#include <QWidget>
#include <QLabel>
#include <QVBoxLayout>
#include <QLabel>
#include <QFont>
#include <QString>

enum LEVEL { first=0, none=1, firstp=10, second=30, secondp=40, third=60, thirdp=70 };

class Window : public QWidget
{
    Q_OBJECT
public:
    explicit Window(QWidget *parent = 0);
    ~Window();

    QLabel *rm_OrgName;
    QLabel *rm_Email;
    QLabel *rm_ExtraContactInfo;
    QLabel *rm_ReportID;
    QLabel *rm_DateRangeBegin;
    QLabel *rm_DateRangeEnd;

    QLabel *pp_Domain;
    QLabel *pp_Adkim;
    QLabel *pp_Aspf;
    QLabel *pp_P;
    QLabel *pp_Sp;
    QLabel *pp_Pct;

    QLabel *re_SourceIP;
    QLabel *re_Count;
    QLabel *re_Disposition;
    QLabel *re_DKIM;
    QLabel *re_SPF;
    QLabel *re_HeaderFrom;
    QLabel *re_ARDKIMDomain;
    QLabel *re_ARDKIMResult;
    QLabel *re_ARSPFDomain;
    QLabel *re_ARSPFResult;
    
signals:

private:
    QLabel *createLabel(const QString &text = "", const LEVEL &level = none);
    QHBoxLayout *createHBox(const QString &text, const LEVEL &level, QLabel *lbl);
    void createDataLabels();

    QWidget *win;
    QVBoxLayout *layout;
};

#endif // WINDOW_H
