# coding:utf-8

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        layout = QVBoxLayout(self)
        hbox = QHBoxLayout()

        hbox.addWidget(QLabel("pen style:"))

        penstyle = QComboBox()
        penstyle.addItems(["SolidLine", "DashLine", "DotLine", "DashDotLine", "DashDotDotLine"])
        hbox.addWidget(penstyle)

        hbox.addWidget(QLabel("pen width:"))

        width = QSpinBox()
        width.setRange(1, 20)
        hbox.addWidget(width)

        self.colorbutton = QPushButton("color")
        self.colorbutton.setFlat(True)
        self.colorbutton.setAutoFillBackground(True)
        self.colorbutton.setPalette(QPalette(Qt.black))
        hbox.addWidget(self.colorbutton)

        clearbutton = QPushButton("clear")
        hbox.addWidget(clearbutton)

        hbox.addStretch()
        layout.addLayout(hbox)

        self.area = PaintArea()
        layout.addWidget(self.area)

        self.connect(penstyle, SIGNAL("activated(int)"), self.slotPenStyle)
        self.connect(width, SIGNAL("valueChanged(int)"), self.slotPenWidth)
        self.connect(self.colorbutton, SIGNAL("clicked()"), self.slotPenColor)
        self.connect(clearbutton, SIGNAL("clicked()"), self.slotClear)

    def slotPenStyle(self, style):
        self.area.pen.setStyle(style + 1)

    def slotPenWidth(self, width):
        self.area.pen.setWidth(width)

    def slotPenColor(self):
        color = QColorDialog.getColor()
        self.colorbutton.setPalette(QPalette(color))
        self.area.pen.setColor(color)

    def slotClear(self):
        self.area.pix.fill(Qt.white)
        self.colorbutton.setPalette(QPalette(Qt.white))
        self.area.update()


class PaintArea(QWidget):
    def __init__(self):
        super(PaintArea, self).__init__()
        self.setAutoFillBackground(True)
        self.setPalette(QPalette(Qt.white))
        self.setMinimumSize(500, 500)
        self.pen = QPen()
        self.startPos = None
        self.pix = QPixmap(self.size())
        self.pix.fill(Qt.white)

    def resizeEvent(self, e):
        newpix = QPixmap(e.size())
        newpix.fill()
        p = QPainter(newpix)
        p.drawPixmap(QPoint(0, 0), self.pix)
        self.pix = newpix

    def mousePressEvent(self, e):
        self.startPos = e.pos()

    def mouseMoveEvent(self, e):
        p = QPainter(self.pix)
        p.setPen(self.pen)
        p.drawLine(self.startPos, e.pos())
        self.startPos = e.pos()
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.drawPixmap(QPoint(0, 0), self.pix)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())
