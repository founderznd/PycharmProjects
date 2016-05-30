# coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class NeuralButton(QToolButton):
    def __init__(self, pixname):
        super(NeuralButton, self).__init__()
        pix = QPixmap(pixname)
        icon = QIcon(pix)
        self.setFixedSize(100, 100)
        self.setIcon(icon)
        self.setIconSize(self.size())
        self.setAutoRaise(True)


class NeuronnenConnection(QWidget):
    def __init__(self):
        super(NeuronnenConnection, self).__init__()
        hbox = QHBoxLayout(self)
        vbox = QVBoxLayout()

        vbox.addSpacing(20)
        self.button1 = NeuralButton("image/neural.png")
        vbox.addWidget(self.button1)
        self.button2 = NeuralButton("image/neural2.png")
        vbox.addWidget(self.button2)
        vbox.addStretch()

        hbox.addLayout(vbox)
        view = QGraphicsView()
        view.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        hbox.addWidget(view)

        self.scene = QGraphicsScene()
        view.setScene(self.scene)
        # set DragMode to ScrollHandDrag
        view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.connect(self.button1, SIGNAL("clicked()"), self.slotAddNeural1)

    def slotAddNeural1(self):
        item = ItemOne()
        item.setPos(0,0)
        self.scene.addItem(item)


class ItemOne(QGraphicsItem):
    def __init__(self):
        super(ItemOne, self).__init__()
        self.pix = QPixmap("image/neural.png")
        self.setScale(0.2)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.dragPos = QPointF(0, 0)

    def boundingRect(self):
        return QRectF(-self.pix.width() / 2 - 2, -self.pix.height() / 2 - 2, self.pix.width() + 4,
                      self.pix.height() + 4)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.scenePos() - self.scenePos()

        if event.button() == Qt.RightButton:
            self.setFocus()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.setPos(event.scenePos() - self.dragPos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setPos(event.scenePos() - self.dragPos)

        if event.button() == Qt.RightButton:
            pass

