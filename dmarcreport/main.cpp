#include <QApplication>
#include "dmarcreport.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    DmarcReport w;
    w.show();
    
    return a.exec();
}
