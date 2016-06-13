# coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Informations as info


# enum of itemtype
class ItemType(object):
    EDGE = 0
    NEURON = 1


class PopulationButton(QToolButton):
    def __init__(self, iconpath):
        super(PopulationButton, self).__init__()
        self.setFixedSize(50, 50)
        # these two code solve the warning below
        # libpng warning: iCCP: known incorrect sRGB profile
        self.image = QImage(iconpath)
        self.image.save(iconpath, "PNG")
        self.pix = QPixmap(iconpath)
        self.setIconSize(self.size())
        self.setIcon(QIcon(self.pix))
        self.setCheckable(True)
        self.setAutoRaise(True)


class NeuralConnectionView(QGraphicsView):
    def __init__(self, parent):
        super(NeuralConnectionView, self).__init__(parent)
        self.scene = MyScene()
        self.setScene(self.scene)

        self.layout = QGridLayout(self)
        self.poplutaion_button = PopulationButton("image/neuron.png")
        self.poplutaion_button.setToolTip("click to add a Population to scene")

        self.center_button = PopulationButton("image/centerOn.png")
        self.center_button.setToolTip("focus on the selected Population")
        self.center_button.setCheckable(False)

        self.layout.addWidget(self.poplutaion_button, 0, 0)
        self.layout.addWidget(self.center_button, 1, 0)
        self.layout.setRowStretch(self.layout.rowCount(), 1)
        self.layout.setColumnStretch(self.layout.columnCount(), 1)

        self.connect(self.center_button, SIGNAL("clicked()"), self.slot_centerOn)

    def slot_centerOn(self):
        if self.scene.currentItem:
            self.centerOn(self.scene.currentItem)


class MyScene(QGraphicsScene):
    replot = pyqtSignal()

    def __init__(self):
        super(MyScene, self).__init__()
        self.setItemIndexMethod(QGraphicsScene.BspTreeIndex)
        self.setSceneRect(0, 0, 1920, 1080)
        self.item_data = {}
        self.source = None
        self.dest = None
        self.currentItem = None
        self.isPrepared = False
        self.info_stack = info.QStackedWidget()

    def update(self, *__args):
        super(MyScene, self).update()
        rect = self.itemsBoundingRect()
        rect = rect.united(self.sceneRect())
        self.setSceneRect(rect)

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
            if edge.type == ItemType.EDGE and edge.contains(item.pos()):
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
            self.info_stack.setCurrentIndex(index)
            # show info of currentItem
            if e.button() == Qt.LeftButton:
                self.item_data = self.currentItem.info.data
                self.replot.emit()
            if e.button() == Qt.RightButton:
                self.source = self.currentItem

        # here edit the selected line if necessary
        # if self.currentItem and self.currentItem.type == ItemType.EDGE:
        #     print self.currentItem.line()

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

    def mouseDoubleClickEvent(self, e):
        if self.currentItem and self.currentItem.type == ItemType.NEURON:
            if e.button() == Qt.LeftButton:
                index = self.currentItem.info.ui.neuron_type.currentIndex()
                self.currentItem.info.open_Dialog(index)


class Edge(QGraphicsLineItem):
    def __init__(self, sourceNode, destNode):
        super(Edge, self).__init__()
        self.type = ItemType.EDGE
        self.setAcceptedMouseButtons(Qt.NoButton)

        self.source = sourceNode
        self.dest = destNode

        self.pen = QPen()
        self.pen.setWidth(2)
        self.pen.setStyle(Qt.DashLine)
        self.setPen(self.pen)

        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()
        self.setLine(QLineF(self.sourcePoint, self.destPoint))

    def isSameTo(self, edge):
        if (edge.source == self.source and edge.dest == self.dest) or (
                        edge.source == self.dest and edge.dest == self.source):
            return True
        else:
            return False

    # def isConnectTo(self, item):
    #     if self.contains(item.pos()):
    #         return True
    #     else:
    #         return False

    def update(self):
        super(Edge, self).update()
        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()
        self.setLine(QLineF(self.sourcePoint, self.destPoint))


class Population(QGraphicsItem):
    def __init__(self):
        super(Population, self).__init__()
        self.type = ItemType.NEURON
        self.pix = QPixmap("image/neuron.png").scaled(80, 80)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        # make sure items alway above edges
        self.setZValue(1)
        self.info = info.InfoWidget()

    def boundingRect(self):
        return QRectF(-self.pix.width() / 2, -self.pix.height() / 2, self.pix.width(), self.pix.height())

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget = None):
        QPainter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)
