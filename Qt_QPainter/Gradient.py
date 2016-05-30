# coding:utf-8

import math
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        layout = QVBoxLayout(self)

        self.area = PaintArea(self)
        layout.addWidget(self.area)

        hbox = QHBoxLayout()
        layout.addLayout(hbox)

        self.startColor = QPushButton("start")
        self.startColor.setAutoFillBackground(True)
        self.startColor.setPalette(QPalette(Qt.darkBlue))
        self.startColor.setFlat(True)
        self.color1 = QColor(Qt.darkBlue)
        self.connect(self.startColor, SIGNAL("clicked()"), self.slotStartColor)

        self.endColor = QPushButton("end")
        self.endColor.setAutoFillBackground(True)
        self.endColor.setPalette(QPalette(Qt.darkCyan))
        self.endColor.setFlat(True)
        self.color2 = QColor(Qt.darkCyan)
        self.connect(self.endColor, SIGNAL("clicked()"), self.slotEndColor)

        gradient = QComboBox()
        spread = QComboBox()
        hbox.addWidget(self.startColor)
        hbox.addWidget(gradient)
        hbox.addWidget(spread)
        hbox.addWidget(self.endColor)

        self.style = QGradient.LinearGradient
        self.spread = QGradient.PadSpread

        gradient.addItems(["Linear", "Radial", "Conical"])
        self.connect(gradient, SIGNAL("activated(int)"), self.slotGradient)

        spread.addItems(["PadSpread", "ReflectSpread", "RepeatSpread"])
        self.connect(spread, SIGNAL("activated(int)"), self.slotSpread)

    def slotStartColor(self):
        self.color1 = QColorDialog.getColor()
        self.startColor.setPalette(QPalette(self.color1))
        self.area.update()

    def slotEndColor(self):
        self.color2 = QColorDialog.getColor()
        self.endColor.setPalette(QPalette(self.color2))
        self.area.update()

    def slotGradient(self, gradient):
        self.style = gradient
        self.area.update()

    def slotSpread(self, spread):
        self.spread = spread
        self.area.update()


class PaintArea(QWidget):
    def __init__(self, parent):
        super(PaintArea, self).__init__(parent)
        self.setPalette(QPalette(Qt.white))
        self.setAutoFillBackground(True)
        self.setMinimumSize(400, 400)
        self.mainwidget = parent
        self.startPoint = QPoint(0, 0)
        self.endPoint = QPoint(400, 400)

    def mousePressEvent(self, e):
        self.startPoint = e.pos()

    def mouseReleaseEvent(self, e):
        self.endPoint = e.pos()
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        rect = self.rect()
        if self.mainwidget.style == QGradient.LinearGradient:
            gradient = QLinearGradient(self.startPoint, self.endPoint)
            gradient.setColorAt(0, self.mainwidget.color1)
            gradient.setColorAt(1, self.mainwidget.color2)
            gradient.setSpread(self.mainwidget.spread)
        elif self.mainwidget.style == QGradient.RadialGradient:
            r = math.sqrt(
                (self.endPoint.x() - self.startPoint.x()) ** 2 + (self.endPoint.y() - self.startPoint.y()) ** 2)
            gradient = QRadialGradient(self.startPoint, r, self.startPoint)
            gradient.setColorAt(0, self.mainwidget.color1)
            gradient.setColorAt(1, self.mainwidget.color2)
            gradient.setSpread(self.mainwidget.spread)
        else:
            angle = math.atan2(self.endPoint.y() - self.startPoint.y(), self.endPoint.x() - self.startPoint.x())
            gradient = QConicalGradient(self.startPoint, -(180 * angle) / math.pi)
            gradient.setColorAt(0, self.mainwidget.color1)
            gradient.setColorAt(1, self.mainwidget.color2)

        p.setBrush(gradient)
        p.drawRect(rect)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())
