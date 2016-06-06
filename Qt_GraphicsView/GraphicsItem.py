# coding:utf-8

import numpy as np

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        cwidget = QWidget()
        self.setCentralWidget(cwidget)

        self.createMenubar()

        layout = QHBoxLayout(cwidget)

        self.view = QGraphicsView()
        layout.addWidget(self.view)

        self.scene = QGraphicsScene()

        self.view.setScene(self.scene)
        self.view.setMinimumSize(400, 400)

        ctrlwidget = QWidget()
        rlayout = QVBoxLayout(ctrlwidget)

        rotategroup = QGroupBox("Rotate")
        rl = QVBoxLayout(rotategroup)
        rotate = QSlider()
        rotate.setOrientation(Qt.Horizontal)
        rotate.setRange(0, 360)
        rl.addWidget(rotate)
        self.connect(rotate, SIGNAL("valueChanged(int)"), self.slotRotate)

        scalegroup = QGroupBox("Scale")
        rl = QVBoxLayout(scalegroup)
        scale = QSlider()
        scale.setOrientation(Qt.Horizontal)
        scale.setRange(0, 100)
        scale.setValue(50)
        rl.addWidget(scale)
        self.connect(scale, SIGNAL("valueChanged(int)"), self.slotScale)

        sheargroup = QGroupBox("Shear")
        rl = QVBoxLayout(sheargroup)
        shear = QSlider()
        shear.setOrientation(Qt.Horizontal)
        shear.setRange(0, 10)
        rl.addWidget(shear)
        self.connect(shear, SIGNAL("valueChanged(int)"), self.slotShear)

        translategroup = QGroupBox("Translate")
        rl = QVBoxLayout(translategroup)
        tr_H = QSlider()
        tr_H.setOrientation(Qt.Horizontal)
        tr_H.setRange(0, 100)
        tr_H.setValue(50)
        rl.addWidget(tr_H)
        self.connect(tr_H, SIGNAL("valueChanged(int)"), self.slotTranslate)

        rlayout.addWidget(rotategroup)
        rlayout.addWidget(scalegroup)
        rlayout.addWidget(sheargroup)
        rlayout.addWidget(translategroup)
        rlayout.addStretch()

        layout.addWidget(ctrlwidget)
        layout.setStretch(0, 8)
        layout.setStretch(1, 2)

    def createMenubar(self):
        menubar = QMenuBar()
        self.setMenuBar(menubar)

        fileMenu = menubar.addMenu("File")
        exitAct = fileMenu.addAction("Exit")
        self.connect(exitAct, SIGNAL("triggered()"), self.close)
        fileMenu.addSeparator()
        staritem = fileMenu.addAction("Add Star")
        self.connect(staritem, SIGNAL("triggered()"), self.slotAddStarItem)
        rectitem = fileMenu.addAction("Add Rect")
        self.connect(rectitem, SIGNAL("triggered()"), self.slotAddRect)
        pixitem = fileMenu.addAction("Add Pix")
        self.connect(pixitem, SIGNAL("triggered()"), self.slotAddPixItem)

    def slotRotate(self, d):
        self.pixitem.rotate = d
        self.pixitem.setRotation(d)

    def slotScale(self, s):
        self.pixitem.scale = s
        self.pixitem.setScale(s / 100.0)

    # 扭曲效果(横向)
    def slotShear(self, n):
        self.pixitem.transform.shear((n / 10.0 - self.pixitem.transform.m21()), 0.0)
        self.pixitem.setTransform(self.pixitem.transform)

    def slotTranslate(self, pos):
        self.pixitem.transform.translate(pos - self.pixitem.transform.m31(), 0.0)
        self.pixitem.setTransform(self.pixitem.transform)

    def slotAddRect(self):
        item = QGraphicsRectItem(QRectF(0, 0, 60, 60))
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(Qt.blue)
        item.setPen(pen)
        item.setBrush(Qt.yellow)
        item.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(item)
        item.setPos((qrand() % int(self.scene.sceneRect().width())) - 200,
                    (qrand() % int(self.scene.sceneRect().height())) - 200)

    def slotAddStarItem(self):
        """这里指定父类很重要！！！！！"""
        anim = QGraphicsItemAnimation(self)

        star = StarItem()
        star.setFlag(QGraphicsItem.ItemIsMovable)
        anim.setItem(star)

        timeline = QTimeLine(2000)
        timeline.setCurveShape(QTimeLine.LinearCurve)
        timeline.setLoopCount(0)
        anim.setTimeLine(timeline)

        r = 150
        for i in range(360):
            anim.setPosAt(i / 360.0, QPointF(r * np.cos(i / 180.0 * np.pi), r * np.sin(i / 180.0 * np.pi)))

        self.scene.addItem(star)

        timeline.start()

    def slotAddPixItem(self):
        pixname = QFileDialog().getOpenFileName(None, "Get Picture", QDir.currentPath(), "*.*")
        self.pixitem = PixItem(QPixmap(pixname))
        self.scene.addItem(self.pixitem)


class StarItem(QGraphicsItem):
    def __init__(self):
        super(StarItem, self).__init__()
        self.pix = QPixmap("image/mario.png").scaled(200, 200)

    def boundingRect(self):
        return QRectF(-self.pix.width() / 2, -self.pix.height() / 2, self.pix.width(), self.pix.height())

    def paint(self, painter, item, widget=None):
        painter.drawPixmap(self.boundingRect().topLeft(), self.pix)


class PixItem(QGraphicsItem):
    def __init__(self, pix):
        super(PixItem, self).__init__()
        self.pix = pix
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.rotate = 0
        self.scale = 0.5
        self.setRotation(self.rotate)
        self.setScale(self.scale)
        self.transform = QTransform()
        self.setTransform(self.transform)

    def boundingRect(self):
        return QRectF(-2 - self.pix.width() / 2, -2 - self.pix.height() / 2, self.pix.width() + 4,
                      self.pix.height() + 4)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
