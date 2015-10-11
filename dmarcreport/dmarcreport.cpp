#include "dmarcreport.h"
#include "ui_dmarcreport.h"

DmarcReport::DmarcReport(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::DmarcReport)
{
    ui->setupUi(this);

    fp = NULL;                  // In case we never open a file before closing and deleting the pointer.
    xml = NULL;

    createActions();
    createMenus();
    createLayout();

    connect(this, SIGNAL(fileProcessed()), this, SLOT(setWindowData()));
}

DmarcReport::~DmarcReport()
{
    if (exitAct)
        delete exitAct;
    if (fileMenu)
        delete fileMenu;
    if (fp)
        delete fp;
    if (openAct)
        delete openAct;
    if (xml)
        delete xml;
    if (ui)
        delete ui;
}

void DmarcReport::createActions()
{
    openAct = new QAction(tr("&Open..."), this);
    openAct->setShortcuts(QKeySequence::Open);
    openAct->setStatusTip(tr("Open an existing file"));
    connect(openAct, SIGNAL(triggered()), this, SLOT(openFile()));

    exitAct = new QAction(tr("E&xit..."), this);
    exitAct->setShortcuts(QKeySequence::Quit);
    exitAct->setStatusTip(tr("Closes the application"));
    connect(exitAct, SIGNAL(triggered()), qApp, SLOT(closeAllWindows()));
}

void DmarcReport::createMenus()
{
    fileMenu = menuBar()->addMenu(tr("&File"));
    fileMenu->addAction(openAct);
    fileMenu->addSeparator();
    fileMenu->addAction(exitAct);
}

void DmarcReport::createLayout()
{
    Window *win = new Window;
    setWindowTitle(tr("DmarcReport"));
    setCentralWidget(win);
}

void DmarcReport::openFile()
{
    QString fileName = QFileDialog::getOpenFileName(this,
                                                    tr("Open report"),
                                                    "",
                                                    tr("XML reports (*.xml *.XML);;Zipped reports (*.zip *.ZIP)"));
    if (!fileName.isEmpty()) {
        fp = new QFile(fileName);
        fp->open(QIODevice::ReadOnly);
        xml = new XmlDmarcParser(fp);
        xml->read();

        emit fileProcessed();
    }
}

void DmarcReport::setWindowData()
{
    win->rm_Email->setText(xml->rep->email);
}
