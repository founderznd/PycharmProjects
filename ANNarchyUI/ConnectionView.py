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
        if self.scene.currentItem and e.key() == Qt.Key_Delete:
            if self.scene.currentItem.type == ItemType.POPULATION:
                self.scene.removeProjectionsOf(self.scene.currentItem)
            self.scene.removeItem(self.scene.currentItem)
            self.scene.info_stack.removeWidget(self.scene.currentItem.info)
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
        self.neurondict = dict()
        self.neuronlist = [
            QString("Define Own..."),
            QString("LeakyIntegratorNeuron"),
            QString("Izhikevich"),
        ]
        # neurondict initialization
        self.neurondict.update({
            "LeakyIntegratorNeuron": {
                "name"       : "LeakyIntegratorNeuron",

                "parameters" : "tau = 10.0\n"
                               "baseline = -0.2",

                "equations"  : "tau * dmp/dt + mp = baseline + sum(exc)\n"
                               "r = pos(mp)",

                "functions"  : "sigmoid(x) = 1.0 / (1.0 + exp(-x))",

                "spike"      : "",
                "reset"      : "",
                "refractory" : 0,
                "description": ""
            }
        })
        self.neurondict.update({
            "Izhikevich": {
                "name"       : "Izhikevich",

                "description": "This script reproduces the simple pulse-coupled network proposed by Eugene Izhikevich "
                               "in the article:Izhikevich, E.M. (2003). Simple Model of Spiking Neurons, "
                               "IEEE Transaction on Neural Networks, 14:6.",

                "parameters" : "noise = 5.0 : population\n"
                               "a = 0.02\n"
                               "b = 0.2\n"
                               "c = -65.0\n"
                               "d = 2.0\n"
                               "v_thresh = 30.0",

                "equations"  : "I = g_exc - g_inh + noise * Normal(0.0, 1.0)\n"
                               "dv/dt = 0.04 * v^2 + 5.0 * v + 140.0-u + I\n"
                               "du/dt = a * (b*v - u)",

                "functions"  : "",

                "spike"      : "v >= v_thresh",

                "reset"      : "v = c\n"
                               "u += d",

                "refractory" : 0
            }
        })
        self.synapsedict = dict()
        self.synapselist = [
            QString("Define Own..."),
            QString("Oja"),
            QString("Spiking synapse")
        ]
        self.synapsedict.update({
            "Oja": {
                "parameters" : "tau = 5000\n"
                               "alpha = 8.0",
                "equations"  : "tau * dw / dt = pre.r * post.r - alpha * post.r^2 * w",
                "psp"        : "",
                "pre_spike"  : "",
                "post_spike" : "",
                "functions"  : "product(x,y) = x * y",
                "name"       : "Oja",
                "description": ""
            }
        })
        self.synapsedict.update({
            "Spiking synapse": {
                "parameters" : "",
                "equations"  : "",
                "psp"        : "",
                "pre_spike"  : "",
                "post_spike" : "",
                "functions"  : "",
                "name"       : "Spiking synapse",
                "description": ""
            }
        })
        # self.connectorlist = list()
        self.source = None
        self.dest = None
        self.currentItem = None
        self.isPrepared = False
        self.info_stack = QStackedWidget()

    def setPrepared(self, isPrepared):
        self.isPrepared = isPrepared

    def update(self, *__args):
        super(MyScene, self).update()
        rect = self.itemsBoundingRect()
        rect = rect.united(self.sceneRect())
        self.setSceneRect(rect)
        if self.currentItem:
            self.currentItem.info.update()

    # synchronize neuron types to all Populations
    def updateNeurondict(self, nd, nl):
        self.neurondict.update(nd)
        self.neuronlist = nl
        for item in self.items():
            if item.type == ItemType.POPULATION:
                item.info.synchronizeDict(self.neurondict, self.neuronlist)

    # synchronize synapse types to all Projections
    def updateSynapsedict(self, sd, sl):
        self.synapsedict.update(sd)
        self.synapselist = sl
        for item in self.items():
            if item.type == ItemType.PROJECTION:
                item.info.synchronizeDict(self.synapsedict, self.synapselist)

    # def updateConnectorlist(self, cl):
    #     self.connectorlist = cl
    #     for item in self.items():
    #         if item.type == ItemType.PROJECTION:
    #             item.info.sychronizeConnector(self.connectorlist)

    def addProjection(self, source, dest):
        if source is not dest:
            # edge = Projection(source, dest, self.synapsedict, self.synapselist, self.connectorlist)
            projection = Projection(source, dest, self.synapsedict, self.synapselist, None)
            for e in self.items():
                if e.type == ItemType.PROJECTION and e.isSameTo(projection):
                    return
            self.addItem(projection)
            self.info_stack.addWidget(projection.info)
            projection.info.sig_synapse.connect(self.updateSynapsedict)
            # edge.info.sig_connector.connect(self.updateConnectorlist)
            self.source = None
            self.dest = None
            return projection.info

    def addPopulation(self, p):
        item = Population(self.neurondict, self.neuronlist)
        item.setPos(p)
        self.addItem(item)
        self.info_stack.addWidget(item.info)
        item.info.sig_neuron.connect(self.updateNeurondict)
        return item.info

    def removeProjectionsOf(self, item):
        for proj in self.items():
            if proj.type == ItemType.PROJECTION and proj.contains(item.pos()):
                self.info_stack.removeWidget(proj.info)
                self.removeItem(proj)
                self.update()

    def mouseMoveEvent(self, e):
        super(MyScene, self).mouseMoveEvent(e)
        if e.buttons() == Qt.LeftButton:
            for proj in self.items():
                if proj.type == ItemType.PROJECTION:
                    proj.update()
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
                self.currentItem.info.openNeuronDefinition(self.currentItem.info.currentData.get("neuron"))
            if self.currentItem.type == ItemType.PROJECTION:
                self.currentItem.info.openSynapseDefinition(self.currentItem.info.currentData.get("synapse"))


class Projection(QGraphicsLineItem):
    OffSet = 40
    SelectRange = 30
    ArrowSize = 10
    LineWidth = 3

    def __init__(self, sourceNode, destNode, synapsedict=None, synapselist=None, connectorlist=None):
        super(Projection, self).__init__()

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.type = ItemType.PROJECTION
        self.source = sourceNode
        self.dest = destNode

        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()

        l = QLineF(self.sourcePoint, self.destPoint)
        l.setLength(l.length() - Projection.OffSet * math.sqrt(2) - Projection.ArrowSize)
        self.endPoint = l.p2()
        l.setLength(Projection.OffSet * math.sqrt(2))
        self.beginPoint = l.p2()

        # this is actually setup the range of selection
        pen = QPen()
        pen.setWidth(Projection.SelectRange)
        self.setPen(pen)
        self.setLine(QLineF(self.sourcePoint, self.destPoint))

        # if type(synapsedict) == dict or type(synapselist) == list or type(connectorlist):
        if type(synapsedict) == dict and type(synapselist) == list:
            self.info = Informations.ProjectionInfo(self.source, self.dest, synapsedict, synapselist, connectorlist)
        else:
            self.info = Informations.ProjectionInfo(self.source, self.dest)

    def isSameTo(self, projection):
        if (projection.source == self.source and projection.dest == self.dest) or (
                        projection.source == self.dest and projection.dest == self.source):
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

        l = QLineF(self.sourcePoint, self.destPoint)
        l.setLength(l.length() - Projection.OffSet * math.sqrt(2) - Projection.ArrowSize)
        self.endPoint = l.p2()
        l.setLength(Projection.OffSet * math.sqrt(2))
        self.beginPoint = l.p2()
        self.setLine(QLineF(self.sourcePoint, self.destPoint))

        self.info.update()

    def boundingRect(self):
        return QRectF(self.sourcePoint.x(), self.sourcePoint.y(), self.destPoint.x() - self.sourcePoint.x(),
                      self.destPoint.y() - self.sourcePoint.y())

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        pen = QPen()
        pen.setWidth(Projection.LineWidth)
        pen.setJoinStyle(Qt.MiterJoin)
        # pen.setStyle(Qt.DotLine)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)

        if self.isSelected():
            pen.setColor(Qt.red)
            brush.setColor(Qt.red)

        QPainter.setPen(pen)
        QPainter.setBrush(brush)

        # begin draw Arrow
        l = QLineF(self.beginPoint, self.endPoint)
        v1 = l.unitVector()
        l.setLength(l.length() - Projection.OffSet * math.sqrt(2))
        v1.setLength(Projection.ArrowSize)
        # this is very important
        v1.translate(self.endPoint - self.beginPoint)

        v2 = v1.normalVector()
        v2.setLength(v1.length() * 0.4)
        v3 = v2.normalVector().normalVector()

        p1 = v1.p2()
        p2 = v2.p2()
        p3 = v3.p2()

        dist = QLineF(self.sourcePoint, self.destPoint)
        if dist.length() > Population.SIZE * math.sqrt(2) + Projection.ArrowSize:
            QPainter.drawLine(QLineF(self.beginPoint, self.endPoint))
            QPainter.drawPolygon(p1, p2, p3)


class Population(QGraphicsItem):
    SIZE = 80

    def __init__(self, neurondict=None, neuronlist=None):
        super(Population, self).__init__()
        self.type = ItemType.POPULATION
        self.pix = QPixmap("image/neuron.png").scaled(Population.SIZE, Population.SIZE)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        # make sure items alway above edges
        self.setZValue(1)

        if isinstance(neurondict, dict) and isinstance(neuronlist, list):
            self.info = Informations.PopulationInfo(neurondict, neuronlist)
        else:
            self.info = Informations.PopulationInfo()

    def boundingRect(self):
        return QRectF(-self.pix.width() / 2, -self.pix.height() / 2, self.pix.width(), self.pix.height())

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)
        if self.isSelected():
            QPainter.drawRoundRect(self.boundingRect())
