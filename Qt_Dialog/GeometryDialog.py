# -*- coding: utf-8 -*-
# 显示位置信息
import sys
from PyQt4.QtGui import *


class PositionDialog(QMainWindow):
    def __init__(self):
        super(PositionDialog, self).__init__()
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.layout = QGridLayout(self.centralwidget)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.xlabel = QLabel("x():")
        self.ylabel = QLabel("y():")
        self.frameGeometrylabel = QLabel("frameGeometry():")
        self.poslabel = QLabel("pos():")
        self.geometrylabel = QLabel("geometry():")
        self.widthlabel = QLabel("width():")
        self.heightlabel = QLabel("height():")
        self.rectlabel = QLabel("rect():")
        self.sizelabel = QLabel("size():")
        self.xnum = QLabel()
        self.ynum = QLabel()
        self.frameGeometrynum = QLabel()
        self.posnum = QLabel()
        self.geometrynum = QLabel()
        self.widthnum = QLabel()
        self.heightnum = QLabel()
        self.rectnum = QLabel()
        self.sizenum = QLabel()
        self.setupUI()
        self.show()

    def setupUI(self):
        # 初始化窗口時最好不要用setGeometry函數，会导致闪烁
        # self.setGeometry(0, 0, 400, 400)
        self.resize(400, 400)
        self.move(400, 400)
        self.setWindowTitle("Geometry")
        self.layout.addWidget(self.xlabel, 0, 0)
        self.layout.addWidget(self.ylabel, 1, 0)
        self.layout.addWidget(self.frameGeometrylabel, 2, 0)
        self.layout.addWidget(self.poslabel, 3, 0)
        self.layout.addWidget(self.geometrylabel, 4, 0)
        self.layout.addWidget(self.widthlabel, 5, 0)
        self.layout.addWidget(self.heightlabel, 6, 0)
        self.layout.addWidget(self.rectlabel, 7, 0)
        self.layout.addWidget(self.sizelabel, 8, 0)
        self.layout.addWidget(self.xnum, 0, 1)
        self.layout.addWidget(self.ynum, 1, 1)
        self.layout.addWidget(self.frameGeometrynum, 2, 1)
        self.layout.addWidget(self.posnum, 3, 1)
        self.layout.addWidget(self.geometrynum, 4, 1)
        self.layout.addWidget(self.widthnum, 5, 1)
        self.layout.addWidget(self.heightnum, 6, 1)
        self.layout.addWidget(self.rectnum, 7, 1)
        self.layout.addWidget(self.sizenum, 8, 1)

    def updateInfo(self):
        self.xnum.setText(str(self.pos().x()))
        self.ynum.setText(str(self.pos().y()))
        self.frameGeometrynum.setText(
            str(self.frameGeometry().x()) + ", " +
            str(self.frameGeometry().y()) + ", " +
            str(self.frameGeometry().width()) + ", " +
            str(self.frameGeometry().height()))
        self.posnum.setText(str(self.pos().x()) + ", " + str(self.pos().y()))
        self.geometrynum.setText(
            str(self.geometry().x()) + ", " +
            str(self.geometry().y()) + ", " +
            str(self.geometry().width()) + ", " +
            str(self.geometry().height()))
        self.widthnum.setText(str(self.width()))
        self.heightnum.setText(str(self.height()))
        self.rectnum.setText(
            str(self.rect().x()) + ", " +
            str(self.rect().y()) + ", " +
            str(self.rect().width()) + ", " +
            str(self.rect().height()))
        self.sizenum.setText(str(self.size().width()) + ", " + str(self.size().height()))

    def moveEvent(self, event):
        self.updateInfo()

    def resizeEvent(self, event):
        self.updateInfo()


app = QApplication(sys.argv)
widget = PositionDialog()
sys.exit(app.exec_())
