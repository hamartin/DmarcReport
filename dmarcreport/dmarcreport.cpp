#include "dmarcreport.h"
#include "ui_dmarcreport.h"

DmarcReport::DmarcReport(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::DmarcReport)
{
    ui->setupUi(this);

    this->fp = NULL;                  // In case we never open a file before closing and deleting the pointer.
    this->xml = NULL;
    this->rep = NULL;
    this->rec = NULL;
    this->pol = NULL;

    createActions();
    createMenus();
    createLayout();

    connect(this, SIGNAL(fileProcessed()), this, SLOT(setWindowData()));
}

DmarcReport::~DmarcReport()
{
    if (this->exitAct)
        delete this->exitAct;
    if (this->fileMenu)
        delete this->fileMenu;
    if (this->fp)
        delete this->fp;
    if (this->openAct)
        delete this->openAct;
    if (this->xml)
        delete this->xml;
    if (this->ui)
        delete this->ui;
}

void DmarcReport::createActions()
{
    this->openAct = new QAction(tr("&Open..."), this);
    this->openAct->setShortcuts(QKeySequence::Open);
    this->openAct->setStatusTip(tr("Open an existing file"));
    connect(this->openAct, SIGNAL(triggered()), this, SLOT(openFile()));

    this->exitAct = new QAction(tr("E&xit..."), this);
    this->exitAct->setShortcuts(QKeySequence::Quit);
    this->exitAct->setStatusTip(tr("Closes the application"));
    connect(this->exitAct, SIGNAL(triggered()), qApp, SLOT(closeAllWindows()));
}

void DmarcReport::createMenus()
{
    this->fileMenu = menuBar()->addMenu(tr("&File"));
    this->fileMenu->addAction(this->openAct);
    this->fileMenu->addSeparator();
    this->fileMenu->addAction(exitAct);
}

void DmarcReport::createLayout()
{
    Window *win = new Window;
    setWindowTitle("DmarcReport");
    setCentralWidget(win);
}

void DmarcReport::openFile()
{
    QString fileName = QFileDialog::getOpenFileName(this,
                                                    tr("Open report"),
                                                    "",
                                                    tr("XML reports (*.xml *.XML);;Zipped reports (*.zip *.ZIP)"));
    if (!fileName.isEmpty()) {
        this->fp = new QFile(fileName);
        this->fp->open(QIODevice::ReadOnly);
        this->xml = new XmlDmarcParser(fp);
        this->xml->read();

        this->rec = this->xml->rec;
        this->rep = this->xml->rep;
        this->pol = this->xml->pol;

        emit fileProcessed();
    }
}

void DmarcReport::setWindowData()
{
    this->win->rmOrgName->setText(&this->rep->orgName);
}
