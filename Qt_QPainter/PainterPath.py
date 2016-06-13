# coding:utf-8

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import sqrt


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        layout = QHBoxLayout(self)

        self.area = PaintArea()
        ctrl_widget = QWidget()
        ctrl_layout = QGridLayout(ctrl_widget)

        ctrl_layout.addWidget(QLabel(u"填充规则："), 0, 0)
        fillrule = QComboBox()
        fillrule.addItems(["OddEvenFill", "WindingFill"])
        ctrl_layout.addWidget(fillrule, 0, 1)

        ctrl_layout.addWidget(QLabel(u"画笔宽度："), 1, 0)
        penwidth = QSpinBox()
        penwidth.setRange(1, 20)
        ctrl_layout.addWidget(penwidth, 1, 1)

        ctrl_layout.addWidget(QLabel(u"画笔颜色："), 2, 0)
        self.pencolorframe = QFrame()
        self.pencolorframe.setAutoFillBackground(True)
        self.pencolorframe.setPalette(QPalette(Qt.blue))
        pencolorbutton = QPushButton("Change")
        ctrl_layout.addWidget(self.pencolorframe, 2, 1)
        ctrl_layout.addWidget(pencolorbutton, 2, 2)

        ctrl_layout.addWidget(QLabel(u"画刷颜色："), 3, 0)
        self.brushcolorframe = QFrame()
        self.brushcolorframe.setAutoFillBackground(True)
        self.brushcolorframe.setPalette(QPalette(Qt.darkCyan))
        brushcolorbutton = QPushButton("Change")
        ctrl_layout.addWidget(self.brushcolorframe, 3, 1)
        ctrl_layout.addWidget(brushcolorbutton, 3, 2)

        ctrl_layout.setRowStretch(ctrl_layout.rowCount() + 1, 1)

        layout.addWidget(self.area)
        layout.addWidget(ctrl_widget)
        layout.setStretch(0, 1)

        self.connect(fillrule, SIGNAL("activated(int)"), self.slotFillRule)
        self.connect(penwidth, SIGNAL("valueChanged(int)"), self.slotPenWidth)
        self.connect(pencolorbutton, SIGNAL("clicked()"), self.slotPenColor)
        self.connect(brushcolorbutton, SIGNAL("clicked()"), self.slotBrushColor)

    def slotFillRule(self, rule):
        self.area.path.setFillRule(rule)
        self.area.update()

    def slotPenWidth(self, penwidth):
        self.area.pen.setWidth(penwidth)
        self.area.update()

    def slotPenColor(self):
        color = QColorDialog.getColor()
        self.pencolorframe.setPalette(QPalette(color))
        self.area.pen.setColor(color)
        self.area.update()

    def slotBrushColor(self):
        color = QColorDialog.getColor()
        self.brushcolorframe.setPalette(QPalette(color))
        self.area.brush.setColor(color)
        self.area.update()


class PaintArea(QWidget):
    def __init__(self):
        super(PaintArea, self).__init__()
        self.setAutoFillBackground(True)
        self.setPalette(QPalette(Qt.white))
        self.setMinimumSize(400, 400)
        self.pen = QPen()
        self.pen.setColor(Qt.blue)
        self.brush = QBrush()
        self.brush.setColor(Qt.darkCyan)

        self.path = QPainterPath()
        self.path.addEllipse(QRectF(150, 150, 100, 100))
        self.path.moveTo(100, 100)
        self.path.cubicTo(300, 100, 200, 200, 300, 300)
        self.path.cubicTo(100, 300, 200, 200, 100, 100)
        self.path.moveTo(100, 300)
        self.path.cubicTo(100, 100, 200, 200, 300, 100)
        self.path.cubicTo(300, 300, 200, 200, 100, 300)
        self.path.moveTo(100, 100)
        self.path.addEllipse(QPointF(200, 200), 100 * sqrt(2), 100 * sqrt(2))

    def paintEvent(self, e):
        p = QPainter(self)
        p.setPen(self.pen)
        p.setBrush(self.brush)
        self.brush.setStyle(Qt.SolidPattern)

        p.drawPath(self.path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())