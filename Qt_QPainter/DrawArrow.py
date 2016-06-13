# coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setFixedSize(600, 600)
        self.lo = QGridLayout(self)

        self.view = QGraphicsView()
        self.view.setSceneRect(0, 0, 500, 500)
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.scene.addItem(MyArrow())

        self.lo.addWidget(self.view)




class MyArrow(QGraphicsLineItem):
    def __init__(self):
        super(MyArrow, self).__init__()
        self.source = QPointF(0, 0)
        self.dest = QPointF(250, 250)
        self.line = QLineF(self.source, self.dest)
        self.line.setLength(self.line.length() + 10)
        self.setLine(self.line)
        pen = QPen()
        pen.setWidth(5)
        self.setPen(pen)

    def update(self, *__args):
        super(MyArrow, self).update()
        self.line = QLineF(self.source, self.dest)
        self.setLine(self.line)

    def mousePressEvent(self, e):
        super(MyArrow, self).mousePressEvent(e)
        self.dest = e.scenePos()
        self.update()
        print "clicked"

    def mouseMoveEvent(self, e):
        super(MyArrow, self).mouseMoveEvent(e)
        if e.buttons() == Qt.LeftButton:
            print "mv"

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        super(MyArrow, self).paint(QPainter, QStyleOptionGraphicsItem, None)
        v = self.line.unitVector()
        v.setLength(10)
        v.translate(self.line.p2())
        p1 = v.p2()

        n = v.normalVector()
        n.setLength(n.length() * 0.5)
        p2 = n.p2()
        n2 = n.normalVector().normalVector()
        p3 = n2.p2()

        path = QPainterPath()
        arrow = QPolygonF([p1, p2, p3, p1])
        path.addPolygon(arrow)
        path.setFillRule(Qt.OddEvenFill)

        brush = QBrush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        QPainter.setBrush(brush)

        pen = QPen()
        pen.setWidth(3)
        QPainter.setPen(pen)

        QPainter.drawPath(path)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())