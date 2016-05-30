# coding:utf-8
# 实现不规则窗体

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

"""
1 初始化鼠标与item中心的偏移量
self.dragPos = QPointF(0, 0)
2 得到鼠标当前的坐标与当前item的坐标偏移量
self.dragPos = event.scenePos() - self.scenePos()
3 修正偏移量
self.setPos(event.scenePos() - self.dragPos)
"""

class ShapeWidget(QWidget):
    def __init__(self):
        super(ShapeWidget, self).__init__()
        self.pix = QPixmap()
        self.pix.load("image/mario.png")
        self.pix = self.pix.scaled(600, 600)
        self.resize(self.pix.size())
        # 关键
        self.setMask(self.pix.mask())
        self.dragPosition = None

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pix)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

        if event.button() == Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.move(e.globalPos() - self.dragPosition)
            e.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ShapeWidget()
    widget.show()
    sys.exit(app.exec_())
