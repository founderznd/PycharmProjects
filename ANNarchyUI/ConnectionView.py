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
        # uncomment them if you occur this problem
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

        self.dragdrop_button = PopulationButton("image/Drag_Drop.png")
        self.dragdrop_button.setToolTip("swith drag mode")
        self.dragdrop_button.setCheckable(True)

        self.layout.addWidget(self.population_button, 0, 0)
        self.layout.addWidget(self.center_button, 0, 1)
        self.layout.addWidget(self.dragdrop_button, 1, 0)
        self.layout.setRowStretch(self.layout.rowCount(), 1)
        self.layout.setColumnStretch(self.layout.columnCount(), 1)

        self.connect(self.center_button, SIGNAL("clicked()"), self.slot_centerOn)
        self.connect(self.dragdrop_button, SIGNAL("clicked()"), self.slot_swith_dragMode)
        self.connect(self.population_button, SIGNAL("clicked(bool)"), self.scene.setPrepared)

    def slot_centerOn(self):
        if self.scene.currentItem:
            self.centerOn(self.scene.currentItem)

    def slot_swith_dragMode(self):
        if self.dragdrop_button.isChecked():
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QGraphicsView.NoDrag)

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
            self.scene.setPrepared(False)
            self.dragdrop_button.setChecked(False)
            self.slot_swith_dragMode()
        self.scene.update()


class MyScene(QGraphicsScene):
    sig_replot = pyqtSignal()

    def __init__(self):
        super(MyScene, self).__init__()
        self.setItemIndexMethod(QGraphicsScene.BspTreeIndex)
        self.setSceneRect(0, 0, 1920, 1080)
        self.isReadyToProjection = False
        self.pop_menu = QMenu()
        self.pop_menu.addAction(QIcon("image/proj_to_other.png"), "project to other", self.slot_projection)
        self.pop_menu.addAction(QIcon("image/setup.png"), "setting neuron", self.slot_set_neuron)
        self.pop_menu.addAction(QIcon("image/monitor.png"), "Monitor", self.slot_monitor)
        self.proj_menu = QMenu()
        self.proj_menu.addAction(QIcon("image/setup.png"), "setting synapse", self.slot_set_synapse)
        self.proj_menu.addAction(QIcon("image/setup.png"), "setting connector", self.slot_set_connector)

        self.neuronlist = [
            QString("Define Own..."),
            QString("PoissonNeuron"),
            QString("LeakyIntegratorNeuron"),
            QString("Izhikevich")
        ]
        # neurondict initialization
        self.neurondict = dict()
        self.neurondict.update({
            "LeakyIntegratorNeuron": {
                "name"      : "LeakyIntegratorNeuron",

                "parameters": "tau = 10.0\n"
                              "baseline = -0.2",

                "equations" : "tau * dmp/dt + mp = baseline + sum(exc)\n"
                              "r = pos(mp)",

                "functions" : "sigmoid(x) = 1.0 / (1.0 + exp(-x))",

                "refractory": 0,
            },
            "Izhikevich"           : {
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

                "spike"      : "v >= v_thresh",

                "reset"      : "v = c\n"
                               "u += d",

                "refractory" : 0
            },
            "PoissonNeuron"        : {
                "name"      : "PoissonNeuron",

                "parameters": "amp = 100.0\n"
                              "frequency = 1.0",

                "equations" : "rates = amp * (1.0 + sin(2*pi*frequency*t/1000.0) )/2.0\n"
                              "p = Uniform(0.0, 1.0) * 1000.0 / dt",

                "spike"     : "p < rates"
            }
        })

        self.synapsedict = dict()
        self.synapselist = [
            QString("Define Own..."),
            QString("None"),
            QString("Oja"),
            QString("Spiking synapse")
        ]
        self.synapsedict.update({
            "None": {},
            "Oja" : {
                "parameters": "tau = 5000\n"
                              "alpha = 8.0",
                "equations" : "tau * dw / dt = pre.r * post.r - alpha * post.r^2 * w",
                "functions" : "product(x,y) = x * y",
                "name"      : "Oja",
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

    def setCursor(self, cursor=(int, QCursor)):
        for view in self.views():
            view.setCursor(cursor)

    def slot_projection(self):
        """
        draw Projection from a pop to another
        :return:
        :rtype:
        """
        self.isReadyToProjection = True
        self.setCursor(Qt.PointingHandCursor)
        self.source = self.currentItem

    def slot_monitor(self):
        if isinstance(self.currentItem, Population):
            self.currentItem.info.slot_monitor()

    def slot_set_neuron(self):
        if isinstance(self.currentItem, Population):
            self.currentItem.info.openNeuronDefinition(self.currentItem.info.currentData.get("neuron"))

    def slot_set_synapse(self):
        if isinstance(self.currentItem, Projection):
            self.currentItem.info.openSynapseDefinition(self.currentItem.info.currentData.get("synapse"))

    def slot_set_connector(self):
        if isinstance(self.currentItem, Projection):
            self.currentItem.info.openConnectorDefinition(self.currentItem.info.currentData.get("connector"))

    def setPrepared(self, isPrepared):
        if isPrepared:
            pix = QPixmap("image/neuron.png")
            pix = pix.scaled(Population.SIZE, Population.SIZE)
            cursor = QCursor(pix)
            self.setCursor(cursor)
        else:
            self.setCursor(Qt.ArrowCursor)
            for view in self.views():
                view.population_button.setChecked(False)
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
        projection = Projection(source, dest, self.synapsedict, self.synapselist, None)
        for e in self.items():
            if e.type == ItemType.PROJECTION and e.isSameTo(projection):
                return
        self.addItem(projection)
        self.info_stack.addWidget(projection.info)
        projection.info.sig_synapse.connect(self.updateSynapsedict)
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
            if isinstance(proj, Projection) and proj.contains(item.pos()):
                self.info_stack.removeWidget(proj.info)
                self.removeItem(proj)
                self.update()

    def mouseMoveEvent(self, e):
        super(MyScene, self).mouseMoveEvent(e)
        if e.buttons() == Qt.LeftButton:
            for proj in self.items():
                if isinstance(proj, Projection):
                    proj.update()
                    self.update()

    # def mouseReleaseEvent(self, e):
    #     super(MyScene, self).mouseReleaseEvent(e)
    #     if e.button() == Qt.LeftButton and self.isReadyToProjection is True:
    #         print "begin"
    #         self.tmp = QLineF(self.source.scenePos(), e.scenePos())
    #         self.addLine(self.tmp)

    def mousePressEvent(self, e):
        super(MyScene, self).mousePressEvent(e)
        self.currentItem = self.itemAt(e.scenePos())
        if self.currentItem and len(self.selectedItems()) == 0:
            self.currentItem.setSelected(True)

        if e.button() == Qt.LeftButton:
            """add a new Population"""
            if self.currentItem is None and self.isPrepared:
                # self.setCursor(Qt.ArrowCursor)
                self.isReadyToProjection = False
                self.addPopulation(e.scenePos())
            """show info of Item"""
            if self.currentItem:
                index = self.info_stack.indexOf(self.currentItem.info)
                self.info_stack.setCurrentIndex(index)
            """add a new Projection"""
            if self.isReadyToProjection is True and isinstance(self.currentItem, Population):
                self.dest = self.currentItem
                self.addProjection(self.source, self.dest)
                self.setCursor(Qt.ArrowCursor)
                self.isReadyToProjection = False

        if e.button() == Qt.RightButton:
            if self.currentItem is None:
                self.setPrepared(False)
            if isinstance(self.currentItem, Population):
                self.pop_menu.exec_(e.screenPos())
            if isinstance(self.currentItem, Projection):
                self.proj_menu.exec_(e.screenPos())

        self.update()

    def mouseDoubleClickEvent(self, e):
        if self.currentItem and e.button() == Qt.LeftButton:
            if self.currentItem.type == ItemType.POPULATION:
                self.currentItem.info.openNeuronDefinition(self.currentItem.info.currentData.get("neuron"))
            if self.currentItem.type == ItemType.PROJECTION:
                self.currentItem.info.openSynapseDefinition(self.currentItem.info.currentData.get("synapse"))


class Projection(QGraphicsPathItem):
    OffSet = 40
    ArrowSize = 14
    LineWidth = 6

    def __init__(self, sourceNode, destNode, synapsedict=None, synapselist=None, connectorlist=None):
        super(Projection, self).__init__()

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.type = ItemType.PROJECTION
        self.source = sourceNode
        self.dest = destNode

        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()

        self.setPath(self.currentPath())

        if type(synapsedict) == dict and type(synapselist) == list:
            self.info = Informations.ProjectionInfo(self.source, self.dest, synapsedict, synapselist, connectorlist)
        else:
            self.info = Informations.ProjectionInfo(self.source, self.dest)

    def isSameTo(self, projection):
        if projection.source == self.source and projection.dest == self.dest:
            return True
        else:
            return False

    def contains(self, p):
        if p == self.sourcePoint or p == self.destPoint:
            return True
        else:
            return super(Projection, self).contains(p)

    def currentPath(self, color=None):
        qpath = QPainterPath()
        pen = QPen()
        pen.setWidth(Projection.LineWidth)
        pen.setJoinStyle(Qt.MiterJoin)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)

        if isinstance(color, QColor):
            pen.setColor(color)
            brush.setColor(color)

        self.setPen(pen)
        # self.setBrush(brush)

        if self.sourcePoint != self.destPoint:

            l = QLineF(self.sourcePoint, self.destPoint)
            l.setLength(l.length() - Projection.OffSet * math.sqrt(2) - Projection.ArrowSize)
            self.endPoint = l.p2()
            l.setLength(Projection.OffSet * math.sqrt(2))
            self.beginPoint = l.p2()

            # begin painting
            l = QLineF(self.beginPoint, self.endPoint)
            v1 = l.unitVector()
            l.setLength(l.length() - Projection.OffSet * math.sqrt(2))
            v1.setLength(Projection.ArrowSize)
            # this is important
            v1.translate(self.endPoint - self.beginPoint)

            v2 = v1.normalVector()
            v2.setLength(v1.length() * 0.4)
            v3 = v2.normalVector().normalVector()

            p0 = v1.p1()
            p1 = v1.p2()
            p2 = v2.p2()
            p3 = v3.p2()

            dist = QLineF(self.sourcePoint, self.destPoint)

            if dist.length() > Population.SIZE * math.sqrt(2) + Projection.ArrowSize:
                qpath.moveTo(self.beginPoint)
                qpath.lineTo(self.endPoint)
                qpath.addPolygon(QPolygonF([p0, p2, p1, p3, p0]))
                v3.setLength(20)
                qpath.translate(v3.p2() - v3.p1())
        else:
            rect = QRectF(0, 0, math.sqrt(2) * Population.SIZE, math.sqrt(2) * Population.SIZE)
            rect.moveCenter(self.sourcePoint)
            # begin draw arrow
            v1 = QLineF(rect.topLeft(), rect.topRight()).unitVector()
            v1.setLength(self.ArrowSize)
            v1.translate(QPointF(self.sourcePoint.x(), rect.top()) - rect.topLeft())
            v2 = v1.normalVector()
            v2.setLength(v1.length() * 0.4)
            v3 = v2.normalVector().normalVector()

            p0 = v1.p1()
            p1 = v1.p2()
            p2 = v2.p2()
            p3 = v3.p2()
            qpath.addPolygon(QPolygonF([p0, p2, p1, p3, p0]))
            # qpath.addEllipse(rect)
            qpath.moveTo(p0)
            qpath.arcTo(rect, 90, 270)
            # c1 = rect.bottomLeft()
            # c2 = self.sourcePoint
            # qpath.cubicTo(c1, c2, p1)

        return qpath

    def update(self):
        super(Projection, self).update()
        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()
        self.setPath(self.currentPath())
        self.info.update()

    def boundingRect(self):
        return super(Projection, self).boundingRect()

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        super(Projection, self).paint(QPainter, QStyleOptionGraphicsItem, None)
        if self.isSelected():
            self.setPath(self.currentPath(QColor(Qt.red)))
        else:
            self.setPath(self.currentPath(QColor(Qt.black)))


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
        return QRectF(-self.pix.width() / 2, -self.pix.height() / 2, self.pix.width(), self.pix.height() * 1.2)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)
        QPainter.drawText(self.boundingRect(), Qt.AlignBottom | Qt.AlignHCenter, self.info.currentData.get("name"))
        if self.isSelected():
            QPainter.drawRoundRect(self.boundingRect())
