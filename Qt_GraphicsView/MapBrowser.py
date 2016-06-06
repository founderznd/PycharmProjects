#  coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MapWidget(QGraphicsView):
    def __init__(self):
        super(MapWidget, self).__init__()
        self.map = QPixmap("image/worldmap.png")

        scene = QGraphicsScene(self)

        self.setScene(scene)
        self.setWindowTitle(u"地图浏览器")
        self.setMinimumSize(600, 400)

        slider = QSlider()
        slider.setOrientation(Qt.Vertical)
        slider.setRange(1, 100)
        self.zoom = 50
        slider.setValue(50)
        self.connect(slider, SIGNAL("valueChanged(int)"), self.slotZoom)

        layout = QHBoxLayout(self)
        layout.addWidget(slider)
        layout.addStretch()

    def drawBackground(self, painter, rect):
        painter.drawPixmap(rect.topLeft(), self.map)

    def slotZoom(self, value):
        if 1 < value < 100:
            if value > self.zoom:
                self.scale(1.01, 1.01)
            else:
                self.scale(0.99, 0.99)
        self.zoom = value

    def wheelEvent(self, e):
        if e.delta() > 0:
            self.scale(1.05, 1.05)
        else:
            self.scale(1 / 1.05, 1 / 1.05)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainwindow = MapWidget()
    mainwindow.show()
    sys.exit(app.exec_())
