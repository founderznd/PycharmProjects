# coding:utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class DragIcon(QLabel):
    def __init__(self,pix):
        super(DragIcon, self).__init__()
        self.setScaledContents(True)
        self.setPixmap(pix)
        self.startPos = QPoint()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.startPos = e.pos()

    def mouseMoveEvent(self, e):
        pass
