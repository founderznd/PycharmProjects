# coding:utf-8

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        text = QTextEdit()
        self.setCentralWidget(text)
        self.resize(800, 600)
        self.createMenus()
        self.createToolBars()

    def createMenus(self):
        menubar = QMenuBar()
        menubar.addMenu("File")
        menubar.addMenu("Edit")
        menubar.addMenu("Help")

        self.setMenuBar(menubar)

    def createToolBars(self):
        toolbar = QToolBar()
        toolbar.addAction(QAction(QIcon(self.getPix(0, 0, 4, 5)), "Open", self))
        self.addToolBar(toolbar)

    def getPix(self, row, col, rowMax, colMax):
        pixmap = QPixmap("image/toolbar.png")
        width = pixmap.width() / colMax
        height = pixmap.height() / rowMax
        print pixmap.width(), pixmap.height()
        print width, height
        print width * row, height * col, (row + 1) * width, (col + 1) * height
        rect = QRect(width * row, height * col, width, height)
        pix = pixmap.copy(rect)
        return pix


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
