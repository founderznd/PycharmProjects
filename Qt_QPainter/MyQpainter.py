# coding:utf-8

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyQpainter(QWidget):
    def __init__(self):
        super(MyQpainter, self).__init__()
        self.layout = QHBoxLayout(self)
        self.area = self.init_left()
        self.right = self.init_right()
        self.layout.addWidget(self.area)
        self.layout.addWidget(self.right)

    def init_left(self):
        area = PaintArea()
        return area

    def init_right(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        self.pen = QPen()
        self.brush = QBrush()

        shape = QComboBox()
        shape.addItems(
            ["Line", "Rectangle", "RoundRect", "Ellipse", "Polygon", "Polyline", "Points", "Arc", "Path", "Text",
             "Pixmap"])
        layout.addWidget(QLabel("shape:"), 0, 0)
        layout.addWidget(shape, 0, 1)
        self.connect(shape, SIGNAL("activated(QString)"), self.slotShape)

        width = QSpinBox()
        width.setRange(0, 20)
        layout.addWidget(QLabel("pen width:"), 1, 0)
        layout.addWidget(width, 1, 1)
        self.connect(width, SIGNAL("valueChanged(int)"), self.slotPenWidth)

        self.colorframe = QFrame()
        self.colorframe.setAutoFillBackground(True)
        self.colorframe.setPalette(QPalette(Qt.black))
        colorbutton = QPushButton(self.tr("Change"))
        layout.addWidget(QLabel("pen color:"), 2, 0)
        layout.addWidget(self.colorframe, 2, 1)
        layout.addWidget(colorbutton, 2, 2)
        self.connect(colorbutton, SIGNAL("clicked()"), self.slotPenColor)

        penstyle = QComboBox()
        penstyle.addItems(["NoPen", "SolidLine", "DashLine", "DotLine", "DashDotLine", "DashDotDotLine"])
        layout.addWidget(QLabel("pen style:"), 3, 0)
        layout.addWidget(penstyle, 3, 1)
        self.connect(penstyle, SIGNAL("activated(int)"), self.slotPenStyle)

        pencap = QComboBox()
        pencap.addItems(["SquareCap", "FlatCap", "RoundCap"])
        layout.addWidget(QLabel("pen cap:"), 4, 0)
        layout.addWidget(pencap, 4, 1)
        self.connect(pencap, SIGNAL("activated(int)"), self.slotPenCap)

        penjoin = QComboBox()
        penjoin.addItems(["MiterJoin", "BevelJoin", "RoundJoin"])
        layout.addWidget(QLabel("pen join:"), 5, 0)
        layout.addWidget(penjoin, 5, 1)
        self.connect(penjoin, SIGNAL("activated(int)"), self.slotPenJoin)

        brushstyle = QComboBox()
        brushstyle.addItems(
            ["NoBrush", "SolidPattern", "Dense1Pattern", "Dense2Pattern", "Dense3Pattern", "Dense4Pattern",
             "Dense5Pattern", "Dense6Pattern", "Dense7Pattern", "HorPattern", "VerPattern", "CrossPattern",
             "BDiagPattern", "FDiagPattern", "DiagCrossPattern"])
        layout.addWidget(QLabel("Brush Style:"), 6, 0)
        layout.addWidget(brushstyle, 6, 1)
        self.connect(brushstyle, SIGNAL("activated(int)"), self.slotBrushStyle)

        self.brushframe = QFrame()
        self.brushframe.setAutoFillBackground(True)
        self.brushframe.setPalette(QPalette(Qt.black))
        brushcolorbutton = QPushButton("Change")
        layout.addWidget(QLabel("Brush Color"), 7, 0)
        layout.addWidget(self.brushframe, 7, 1)
        layout.addWidget(brushcolorbutton, 7, 2)
        self.connect(brushcolorbutton, SIGNAL("clicked()"), self.slotBrushColor)

        return widget

    def slotShape(self, shape):
        self.area.setShape(shape)

    def slotPenWidth(self, width):
        self.pen.setWidth(width)
        self.area.setPen(self.pen)

    def slotPenColor(self):
        color = QColorDialog.getColor()
        self.colorframe.setPalette(QPalette(color))
        self.pen.setColor(color)
        self.area.setPen(self.pen)

    def slotPenStyle(self, penstyle):
        self.pen.setStyle(penstyle)
        self.area.setPen(self.pen)

    def slotPenCap(self, pencap):
        self.pen.setCapStyle(pencap * 10)
        self.area.setPen(self.pen)

    def slotPenJoin(self, penjoin):
        self.pen.setJoinStyle(penjoin * 40)
        self.area.setPen(self.pen)

    def slotBrushStyle(self, brushstyle):
        self.brush.setStyle(brushstyle)
        self.area.setBrush(self.brush)

    def slotBrushColor(self):
        color = QColorDialog().getColor()
        self.brushframe.setPalette(QPalette(color))
        self.brush.setColor(color)
        self.area.setBrush(self.brush)


class PaintArea(QWidget):
    def __init__(self):
        super(PaintArea, self).__init__()
        self.setPalette(QPalette(Qt.white))
        self.setAutoFillBackground(True)
        self.setMinimumSize(400, 400)
        self.shape = ""
        self.pen = QPen()
        self.brush = QBrush()

    def setShape(self, shape):
        self.shape = shape
        self.update()

    def setPen(self, pen):
        self.pen = QPen(pen)
        self.update()

    def setBrush(self, brush):
        self.brush = QBrush(brush)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        """for drawRect,drawRoundRect,drawEllipse"""
        rect = QRect(50, 100, 300, 200)

        """for drawPolygon,drawline,drawPoints"""
        points = QPolygon([QPoint(150, 100), QPoint(300, 150), QPoint(350, 250), QPoint(100, 300)])

        """for drawArc"""
        startAngle = 30 * 16
        spanAngle = 120 * 16

        """for drawPath"""
        path = QPainterPath()
        path.addRect(150, 150, 100, 100)
        path.moveTo(100, 100)
        path.cubicTo(300, 100, 200, 200, 300, 300)
        path.cubicTo(100, 300, 200, 200, 100, 100)

        if self.shape == "Line":
            painter.drawLine(rect.topLeft(), rect.bottomRight())
        elif self.shape == "Rectangle":
            painter.drawRect(rect)
        elif self.shape == "RoundRect":
            painter.drawRoundRect(rect)
        elif self.shape == "Ellipse":
            painter.drawEllipse(rect)
        elif self.shape == "Polygon":
            painter.drawPolygon(points)
        elif self.shape == "Polyline":
            painter.drawPolyline(points)
        elif self.shape == "Points":
            painter.drawPoints(points)
        elif self.shape == "Arc":
            painter.drawArc(rect, startAngle, spanAngle)
        elif self.shape == "Path":
            painter.drawPath(path)
        elif self.shape == "Text":
            painter.drawText(rect, Qt.AlignCenter, self.tr("Hello Qt!"))
        elif self.shape == "Pixmap":
            painter.drawPixmap(150, 150, QPixmap("image/mario.png"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyQpainter()
    widget.show()
    sys.exit(app.exec_())
