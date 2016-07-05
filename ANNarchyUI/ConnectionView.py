# coding:utf-8
import math

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Informations


# enum of itemtype
class ItemType(object):
    PROJECTION = 0
    POPULATION = 1


class PopulationButton(QToolButton):
    SIZE = 50

    def __init__(self, iconpath):
        super(PopulationButton, self).__init__()
        self.setFixedSize(PopulationButton.SIZE, PopulationButton.SIZE)

        # these two lines codes below solved the warning
        # libpng warning: iCCP: known incorrect sRGB profile
        # uncomment them if necessary
        # self.image = QImage(iconpath)
        # self.image.save(iconpath, "PNG")

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
        self.population_button = PopulationButton("image/neuron.png")
        self.population_button.setToolTip("click to add a Population to scene")

        self.center_button = PopulationButton("image/centerOn.png")
        self.center_button.setToolTip("focus on the selected Population")
        self.center_button.setCheckable(False)

        self.layout.addWidget(self.population_button, 0, 0)
        self.layout.addWidget(self.center_button, 1, 0)
        self.layout.setRowStretch(self.layout.rowCount(), 1)
        self.layout.setColumnStretch(self.layout.columnCount(), 1)

        self.connect(self.center_button, SIGNAL("clicked()"), self.slot_centerOn)

    def slot_centerOn(self):
        if self.scene.currentItem:
            self.centerOn(self.scene.currentItem)

    # delete currentItem when press "del" on keyboard
    def keyPressEvent(self, e):
        if self.scene.currentItem and self.scene.currentItem.type == ItemType.POPULATION:
            if e.key() == Qt.Key_Delete:
                self.scene.removeProjectionsOf(self.scene.currentItem)
                self.scene.info_stack.removeWidget(self.scene.currentItem.info)
                self.scene.removeItem(self.scene.currentItem)
                self.scene.currentItem = None
                self.scene.sig_replot.emit()
        if e.key() == Qt.Key_Escape:
            self.population_button.setChecked(False)
            self.scene.isPrepared = False
        self.scene.update()


class MyScene(QGraphicsScene):
    sig_replot = pyqtSignal()

    def __init__(self):
        super(MyScene, self).__init__()
        self.setItemIndexMethod(QGraphicsScene.BspTreeIndex)
        self.setSceneRect(0, 0, 1920, 1080)
        self.item_data = dict()
        self.neuronsdict = dict()
        self.synapsedict = dict()
        self.source = None
        self.dest = None
        self.currentItem = None
        self.isPrepared = False
        self.info_stack = QStackedWidget()

    def update(self, *__args):
        super(MyScene, self).update()
        rect = self.itemsBoundingRect()
        rect = rect.united(self.sceneRect())
        self.setSceneRect(rect)
        if self.currentItem:
            self.currentItem.info.update()

    # synchronize neuron types to all Populations
    def updateNeurondict(self, nd):
        self.neuronsdict.update(nd)
        for item in self.items():
            if item.type == ItemType.POPULATION:
                item.info.synchronizeDict(self.neuronsdict)

    # synchronize synapse types to all Projections
    def updateSynapsedict(self, sd):
        self.synapsedict.update(sd)
        for item in self.items():
            if item.type == ItemType.PROJECTION:
                item.info.synchronizeDict(self.synapsedict)

    def addProjection(self, source, dest):
        if source is not dest:
            edge = Projection(source, dest, self.synapsedict)
            for e in self.items():
                if e.type == ItemType.PROJECTION and e.isSameTo(edge):
                    return
            self.addItem(edge)
            self.info_stack.addWidget(edge.info)
            edge.info.sig_synapse.connect(self.updateSynapsedict)
            self.source = None
            self.dest = None

    def addPopulation(self, p):
        item = Population(self.neuronsdict)
        item.setPos(p)
        self.addItem(item)
        self.info_stack.addWidget(item.info)
        item.info.sig_neuron.connect(self.updateNeurondict)

    def removeProjectionsOf(self, item):
        for edge in self.items():
            if edge.type == ItemType.PROJECTION and edge.contains(item.pos()):
                self.removeItem(edge)
                self.info_stack.removeWidget(edge.info)
                self.update()

    def mouseMoveEvent(self, e):
        super(MyScene, self).mouseMoveEvent(e)
        if e.buttons() == Qt.LeftButton:
            for edge in self.items():
                if edge.type == ItemType.PROJECTION:
                    edge.update()
        self.update()

    def mousePressEvent(self, e):
        super(MyScene, self).mousePressEvent(e)
        self.currentItem = self.itemAt(e.scenePos())
        if self.currentItem and self.currentItem.type == ItemType.POPULATION:
            # show info of currentItem
            index = self.info_stack.indexOf(self.currentItem.info)
            self.info_stack.setCurrentIndex(index)
            if e.button() == Qt.LeftButton:
                self.item_data = self.currentItem.info.currentData
                self.sig_replot.emit()
            if e.button() == Qt.RightButton:
                self.source = self.currentItem

        if self.currentItem and self.currentItem.type == ItemType.PROJECTION:
            # show info of currentItem
            index = self.info_stack.indexOf(self.currentItem.info)
            self.info_stack.setCurrentIndex(index)
            if e.button() == Qt.LeftButton:
                self.item_data = self.currentItem.info.currentData

        if self.currentItem is None:
            if e.button() == Qt.LeftButton and self.isPrepared:
                self.addPopulation(e.scenePos())

        self.update()

    def mouseReleaseEvent(self, e):
        super(MyScene, self).mouseReleaseEvent(e)
        if e.button() == Qt.RightButton and self.source:
            self.dest = self.itemAt(e.scenePos())
            if self.dest and self.dest.type == ItemType.POPULATION:
                self.addProjection(self.source, self.dest)
                self.update()

    def mouseDoubleClickEvent(self, e):
        if self.currentItem and e.button() == Qt.LeftButton:
            if self.currentItem.type == ItemType.POPULATION:
                self.currentItem.info.openDialog(self.currentItem.info.currentData.get("neuron"))
            if self.currentItem.type == ItemType.PROJECTION:
                self.currentItem.info.openDialog(self.currentItem.info.currentData.get("synapse"))


class Projection(QGraphicsLineItem):
    OffSet = 40
    ArrowSize = 15

    def __init__(self, sourceNode, destNode, synapsedict=None):
        super(Projection, self).__init__()

        self.type = ItemType.PROJECTION
        self.source = sourceNode
        self.dest = destNode

        self.pen = QPen()
        self.pen.setWidth(5)
        # self.pen.setStyle(Qt.DotLine)
        self.setPen(self.pen)

        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()
        self.l = QLineF(self.sourcePoint, self.destPoint)
        self.l.setLength(self.l.length() - Projection.OffSet * math.sqrt(2))
        self.setLine(self.l)

        if type(synapsedict) == dict:
            self.info = Informations.ProjectionInfo(self.source, self.dest, synapsedict)
        else:
            self.info = Informations.ProjectionInfo(self.source, self.dest)

    def isSameTo(self, edge):
        if (edge.source == self.source and edge.dest == self.dest) or (
                        edge.source == self.dest and edge.dest == self.source):
            return True
        else:
            return False

    def contains(self, p):
        if p == self.sourcePoint or p == self.destPoint:
            return True
        else:
            return super(Projection, self).contains(p)

    def update(self):
        super(Projection, self).update()
        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()
        self.l = QLineF(self.sourcePoint, self.destPoint)
        if self.l.length() > Projection.OffSet * math.sqrt(2):
            self.l.setLength(self.l.length() - Projection.OffSet * math.sqrt(2))
        else:
            self.l.setLength(0)
        self.setLine(self.l)
        self.info.update()

    def boundingRect(self):
        return QRectF(self.sourcePoint.x(), self.sourcePoint.y(), self.destPoint.x() - self.sourcePoint.x(),
                      self.destPoint.y() - self.sourcePoint.y())

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        super(Projection, self).paint(QPainter, QStyleOptionGraphicsItem, None)
        # begin draw Arrow
        v1 = self.l.unitVector()
        v1.setLength(Projection.ArrowSize)
        # this is very important
        v1.translate(QPointF(self.l.dx(), self.l.dy()))

        p1 = v1.p2()
        v2 = v1.normalVector()
        v2.setLength(v1.length() * 0.4)
        p2 = v2.p2()
        v3 = v2.normalVector().normalVector()
        p3 = v3.p2()

        arrow = QPolygonF([p1, p2, p3, p1])

        path = QPainterPath()
        path.addPolygon(arrow)
        pen = QPen()
        pen.setJoinStyle(Qt.MiterJoin)
        QPainter.setPen(pen)
        brush = QBrush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        QPainter.setBrush(brush)

        QPainter.drawPath(path)


class Population(QGraphicsItem):
    SIZE = 80

    def __init__(self, neurondict=None):
        super(Population, self).__init__()
        self.type = ItemType.POPULATION
        self.pix = QPixmap("image/neuron.png").scaled(Population.SIZE, Population.SIZE)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        # make sure items alway above edges
        self.setZValue(1)

        if neurondict:
            self.info = Informations.PopulationInfo(neurondict)
        else:
            self.info = Informations.PopulationInfo()

    def boundingRect(self):
        return QRectF(-self.pix.width() / 2, -self.pix.height() / 2, self.pix.width(), self.pix.height())

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)
        if self.isSelected():
            QPainter.drawRoundRect(self.boundingRect())