# coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Informations as info


class NeuralButton(QToolButton):
    def __init__(self, pixname):
        super(NeuralButton, self).__init__()
        pix = QPixmap(pixname)
        icon = QIcon(pix)
        self.setFixedSize(100, 100)
        self.setIcon(icon)
        self.setIconSize(self.size())
        self.setAutoRaise(True)


# class ItemInfoView(QGroupBox):
#     def __init__(self):
#         super(ItemInfoView, self).__init__()
#         self.setTitle("Informations:")
#
#         self.layout = QFormLayout(self)
#
#         self.functionName = QLabel()
#
#     def setupInfo(self, d):
#         for item in d.items():
#             key = QLabel(str(item[0]))
#             value = QLabel(str(item[1]))
#             self.layout.addRow(key, value)


class NeuralConnectionView(QWidget):
    def __init__(self):
        super(NeuralConnectionView, self).__init__()
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
        hbox.addWidget(view)

        self.scene = MyScene()
        view.setScene(self.scene)
        # set DragMode to ScrollHandDrag
        view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.connect(self.button1, SIGNAL("clicked()"), self.slotAddNeural1)

        self.connect(self.scene, SIGNAL("activated(int)"), self.slot_test)

    def slotAddNeural1(self):
        item = ItemOne()
        self.scene.addItem(item)
        self.scene.info_stack.addWidget(item.info)

    def getItemData(self):
        return self.scene.item_data

    def slot_test(self, i):
        # print self.scene.currentItem
        # print "index = ", len(self.scene.items()) - i - 1 - len(self.scene.edgelist)
        # if self.scene.currentItem:
        #     print self.scene.info_stack.indexOf(self.scene.currentItem.info)
        # else:
        #     print None
        self.scene.info_stack.setCurrentIndex(len(self.scene.items()) - i - 1 - len(self.scene.edgelist))


class MyScene(QGraphicsScene):
    repaintSignal = pyqtSignal()
    activated = pyqtSignal(int)

    def __init__(self):
        super(MyScene, self).__init__()
        self.item_data = {}
        self.edgelist = []
        self.source = None
        self.dest = None
        self.currentItem = None
        self.info_stack = QStackedWidget()

    def getCurrentIndex(self):
        index = 0
        for item in self.items():
            if self.currentItem == item:
                return index
            else:
                index += 1
        return index

    def addEdge(self):
        if self.source and self.dest:
            edge = Edge(self.source, self.dest)
            for e in self.edgelist:
                if e.isSameTo(edge):
                    return
            self.edgelist.append(edge)
            self.addItem(edge)
            self.source = None
            self.dest = None

    def removeEdgesOf(self, item):
        l = []
        for edge in self.edgelist:
            if edge.isConnectTo(item):
                l.append(edge)
        for edge in l:
            self.removeItem(edge)
            self.edgelist.remove(edge)

    def mouseMoveEvent(self, e):
        self.update()
        super(MyScene, self).mouseMoveEvent(e)
        for edge in self.edgelist:
            edge.update()

    def mousePressEvent(self, e):
        self.update()
        super(MyScene, self).mousePressEvent(e)
        self.currentItem = self.itemAt(e.scenePos())
        if self.currentItem:
            # emit a Signal with the index of currentItem
            index = self.getCurrentIndex()
            if index != -1:
                self.activated.emit(index)
            # show info on right
            if e.button() == Qt.LeftButton and self.currentItem.type() == 1:
                self.item_data = self.currentItem.info.data
                self.repaintSignal.emit()
            if e.button() == Qt.RightButton:
                self.source = self.currentItem

    def mouseReleaseEvent(self, e):
        self.update()
        super(MyScene, self).mouseReleaseEvent(e)
        if e.button() == Qt.RightButton:
            self.dest = self.itemAt(e.scenePos())
            if self.source is not self.dest:
                self.addEdge()

    # delete item when press "del" on keyboard
    def keyPressEvent(self, e):
        self.update()
        if e.key() == Qt.Key_Delete and self.currentItem:
            if self.currentItem.type() == 1:
                self.removeEdgesOf(self.currentItem)
                self.info_stack.removeWidget(self.currentItem.info)
                self.removeItem(self.currentItem)
                self.currentItem = None
                self.repaintSignal.emit()


class Edge(QGraphicsItem):
    def __init__(self, sourceNode, destNode):
        super(Edge, self).__init__()
        self.setAcceptedMouseButtons(Qt.NoButton)

        self.source = sourceNode
        self.dest = destNode

        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()

    def type(self):
        return 0

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
        pen.setWidth(4)
        pen.setStyle(Qt.DotLine)
        QPainter.setPen(pen)
        QPainter.drawLine(self.sourcePoint, self.destPoint)


class ItemOne(QGraphicsItem):
    def __init__(self):
        super(ItemOne, self).__init__()
        self.pix = QPixmap("image/neural.png")
        self.setScale(0.2)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.dragPos = QPointF(0, 0)
        # make sure items alway above edges
        self.setZValue(1)

        self.info = info.Parameters()

    def type(self):
        return 1

    def boundingRect(self):
        return QRectF(-self.pix.width() / 2, -self.pix.height() / 2, self.pix.width(), self.pix.height())

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)

    # setup parameters in a QDialog and return them to info.parameterDict
    def mouseDoubleClickEvent(self, e):
        super(ItemOne, self).mouseDoubleClickEvent(e)
        if e.button() == Qt.LeftButton:
            self.info.show()
