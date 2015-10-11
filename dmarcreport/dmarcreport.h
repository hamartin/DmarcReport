#ifndef DMARCREPORT_H
#define DMARCREPORT_H

#include <QAction>
#include <QFile>
#include <QFileDialog>
#include <QMainWindow>
#include <QMenu>
#include <QWidget>

#include "xmldmarcparser.h"
#include "window.h"

namespace Ui {
class DmarcReport;
}

class DmarcReport : public QMainWindow
{
    Q_OBJECT
    
public:
    explicit DmarcReport(QWidget *parent = 0);
    ~DmarcReport();

signals:
    void fileProcessed();

private slots:
    void openFile();
    void setWindowData();
    
private:
    void createActions();
    void createMenus();
    void createLayout();

    Ui::DmarcReport *ui;

    QMenu   *fileMenu;
    QAction *exitAct;
    QAction *openAct;
    QFile   *fp;

    XmlDmarcParser *xml;

    Window *win;        // setCentralWidget passes owner too, meaning we don't have to delete it.
};

#endif // DMARCREPORT_H
