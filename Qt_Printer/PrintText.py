# coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class PrintText(QMainWindow):
    def __init__(self):
        super(PrintText, self).__init__()
        self.setWindowTitle("printer")
        self.resize(800, 600)

        self.textedit = QTextEdit()
        self.setCentralWidget(self.textedit)
        menubar = QMenuBar()
        print_action = menubar.addAction("print")
        self.setMenuBar(menubar)

        file = QFile("readme.txt")
        if file.open(QIODevice.ReadOnly | QIODevice.Text):
            textstream = QTextStream(file)
            while not textstream.atEnd():
                self.textedit.append(textstream.readLine())
            file.close()

        self.connect(print_action, SIGNAL("triggered()"), self.slotPrint)

    def slotPrint(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_():
            doc = self.textedit.document()
            doc.print_(printer)


import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PrintText()
    window.show()
    sys.exit(app.exec_())
