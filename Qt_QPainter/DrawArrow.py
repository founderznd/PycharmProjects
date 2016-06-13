# coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyWidget(QGraphicsView):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setFixedSize(300, 300)
        self.setSceneRect(0, 0, 250, 250)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.scene.addItem(MyArrow())


class MyArrow(QGraphicsLineItem):
    def __init__(self):
        super(MyArrow, self).__init__()
        self.source = QPointF(0, 250)
        self.dest = QPointF(120, 120)
        self.line = QLineF(self.source, self.dest)
        self.line.setLength(self.line.length() - 10)
        self.setLine(self.line)
        pen = QPen()
        pen.setWidth(5)
        self.setPen(pen)

    def update(self, *__args):
        super(MyArrow, self).update()
        self.line = QLineF(self.source, self.dest)
        self.setLine(self.line)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        super(MyArrow, self).paint(QPainter, QStyleOptionGraphicsItem, None)
        v = self.line.unitVector()
        v.setLength(20)
        v.translate(QPointF(self.line.dx(), self.line.dy()))

        n = v.normalVector()
        n.setLength(n.length() * 0.5)
        n2 = n.normalVector().normalVector()
        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()
        arrow = QPolygonF([p1, p2, p3, p1])

        path = QPainterPath()
        path.addPolygon(arrow)

        path.setFillRule(Qt.OddEvenFill)
        brush = QBrush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        QPainter.setBrush(brush)

        pen = QPen()
        pen.setWidth(5)
        pen.setJoinStyle(Qt.MiterJoin)
        QPainter.setPen(pen)

        QPainter.drawPath(path)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
