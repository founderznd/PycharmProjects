# coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Informations as info


# enum of itemtype
class ItemType(object):
    EDGE = 0
    NEURON = 1


class NeuronIcon(QToolButton):
    def __init__(self, pixname):
        super(NeuronIcon, self).__init__()
        pix = QPixmap(pixname)
        icon = QIcon(pix)
        self.setFixedSize(100, 100)
        self.setIcon(icon)
        self.setIconSize(self.size())
        self.setAutoRaise(True)
        self.setCheckable(True)


class NeuralConnectionView(QWidget):
    def __init__(self):
        super(NeuralConnectionView, self).__init__()
        hbox = QHBoxLayout(self)
        vbox = QVBoxLayout()

        vbox.addSpacing(20)
        self.button1 = NeuronIcon("image/neural.png")
        vbox.addWidget(self.button1)
        self.button2 = NeuronIcon("image/neural2.png")
        vbox.addWidget(self.button2)
        vbox.addStretch()

        hbox.addLayout(vbox)
        view = QGraphicsView()
        hbox.addWidget(view)

        self.scene = MyScene()
        view.setScene(self.scene)
        # set DragMode to ScrollHandDrag
        view.setDragMode(QGraphicsView.ScrollHandDrag)

        self.connect(self.button1, SIGNAL("clicked()"), self.slotAddNeuron)
        self.connect(self.scene, SIGNAL("selectedItem(int)"), self.slotChangeStack)

    def slotAddNeuron(self):
        self.scene.isPrepared = self.button1.isChecked()

    def getItemData(self):
        return self.scene.item_data

    def slotChangeStack(self, i):
        self.scene.info_stack.setCurrentIndex(i)


class MyScene(QGraphicsScene):
    replot = pyqtSignal()
    selectedItem = pyqtSignal(int)

    def __init__(self):
        super(MyScene, self).__init__()
        self.setItemIndexMethod(QGraphicsScene.BspTreeIndex)
        self.setSceneRect(0, 0, 1920, 1080)
        self.item_data = {}
        self.source = None
        self.dest = None
        self.currentItem = None
        self.info_stack = QStackedWidget()
        self.isPrepared = False

    def addEdge(self, source, dest):
        if source is not dest:
            edge = Edge(source, dest)
            for e in self.items():
                if e.type == ItemType.EDGE and e.isSameTo(edge):
                    return
            self.addItem(edge)
            self.source = None
            self.dest = None
            self.update()

    def removeEdgesOf(self, item):
        for edge in self.items():
            if edge.type == ItemType.EDGE and edge.isConnectTo(item):
                self.removeItem(edge)
                self.update()

    def mouseMoveEvent(self, e):
        super(MyScene, self).mouseMoveEvent(e)
        if e.buttons() == Qt.LeftButton:
            for edge in self.items():
                if edge.type == ItemType.EDGE:
                    edge.update()
        self.update()

    def mousePressEvent(self, e):
        super(MyScene, self).mousePressEvent(e)
        self.currentItem = self.itemAt(e.scenePos())
        if self.currentItem and self.currentItem.type == ItemType.NEURON:
            # emit a signal with index of currentItem.info
            index = self.info_stack.indexOf(self.currentItem.info)
            self.selectedItem.emit(index)
            # show info of currentItem
            if e.button() == Qt.LeftButton:
                self.item_data = self.currentItem.info.data
                self.replot.emit()
            if e.button() == Qt.RightButton:
                self.source = self.currentItem
        if self.currentItem is None:
            if e.button() == Qt.LeftButton and self.isPrepared:
                item = Population()
                item.setPos(e.scenePos())
                self.addItem(item)
                self.info_stack.addWidget(item.info)
        self.update()

    def mouseReleaseEvent(self, e):
        super(MyScene, self).mouseReleaseEvent(e)
        if e.button() == Qt.RightButton and self.source:
            self.dest = self.itemAt(e.scenePos())
            if self.dest and self.dest.type == ItemType.NEURON:
                self.addEdge(self.source, self.dest)
                self.update()

    # delete currentItem when press "del" on keyboard
    def keyPressEvent(self, e):
        if self.currentItem and self.currentItem.type == ItemType.NEURON:
            if e.key() == Qt.Key_Delete:
                self.removeEdgesOf(self.currentItem)
                self.info_stack.removeWidget(self.currentItem.info)
                self.removeItem(self.currentItem)
                self.currentItem = None
                self.replot.emit()
                self.update()


class Edge(QGraphicsItem):
    def __init__(self, sourceNode, destNode):
        super(Edge, self).__init__()
        self.type = ItemType.EDGE
        self.setAcceptedMouseButtons(Qt.NoButton)

        self.source = sourceNode
        self.dest = destNode

        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()

    def isSameTo(self, edge):
        if (edge.source == self.source and edge.dest == self.dest) or (
                        edge.source == self.dest and edge.dest == self.source):
            return True
        else:
            return False

    def isConnectTo(self, item):
        if self.source == item or self.dest == item:
            return True
        else:
            return False

    def update(self):
        super(Edge, self).update()
        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()

    def boundingRect(self):
        return QRectF(self.sourcePoint, self.destPoint)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        pen = QPen()
        pen.setWidth(2)
        pen.setStyle(Qt.DotLine)
        QPainter.setPen(pen)
        QPainter.drawLine(self.sourcePoint, self.destPoint)


class Population(QGraphicsItem):
    def __init__(self):
        super(Population, self).__init__()
        self.type = ItemType.NEURON
        self.pix = QPixmap("image/neural.png")
        self.setScale(0.2)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.dragPos = QPointF(0, 0)
        # make sure items alway above edges
        self.setZValue(1)
        self.info = info.ParameterStack()

    def boundingRect(self):
        return QRectF(-self.pix.width() / 2, -self.pix.height() / 2, self.pix.width(), self.pix.height())

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)
