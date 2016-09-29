# coding:utf-8
import math

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Informations


class UiData(object):
    def __init__(self):
        self.neurons = {
            "Define Own..."        : {},
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
        }

        self.synapses = {
            "Define Own..."  : {},
            "None"           : {
                "name": "None"
            },
            "Oja"            : {
                "parameters": "tau = 5000\n"
                              "alpha = 8.0",
                "equations" : "tau * dw / dt = pre.r * post.r - alpha * post.r^2 * w",
                "functions" : "product(x,y) = x * y",
                "name"      : "Oja",
            },
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
        }


class ViewButton(QToolButton):
    SIZE = 50

    def __init__(self, iconpath):
        super(ViewButton, self).__init__()
        self.setFixedSize(self.SIZE, self.SIZE)
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


class PopulationMenu(QMenu):
    def __init__(self):
        super(PopulationMenu, self).__init__()
        self.action_projection = self.addAction(QIcon("image/proj_to_other.png"), "project to ...")
        self.action_neuron = self.addAction(QIcon("image/setup.png"), "setting neuron")
        self.action_monitor = self.addAction(QIcon("image/monitor.png"), "Monitor")


class ProjectionMenu(QMenu):
    def __init__(self):
        super(ProjectionMenu, self).__init__()
        self.action_synapse = self.addAction(QIcon("image/setup.png"), "setting synapse")
        self.action_connector = self.addAction(QIcon("image/setup.png"), "setting connector")


class MyView(QGraphicsView):
    def __init__(self, parent):
        super(MyView, self).__init__(parent)
        self.scene = MyScene()
        self.setScene(self.scene)

        self._currentItem = None

        self.layout = QGridLayout(self)
        self.population_button = ViewButton("image/population.png")
        self.population_button.setToolTip("click to add a Population to scene")

        self.centerOn_button = ViewButton("image/centerOn.png")
        self.centerOn_button.setToolTip("focus on the selected Population")
        self.centerOn_button.setCheckable(False)

        self.dragdrop_button = ViewButton("image/Drag_Drop.png")
        self.dragdrop_button.setToolTip("swith drag mode")

        self.layout.addWidget(self.population_button, 0, 0)
        self.layout.addWidget(self.centerOn_button, 0, 2)
        self.layout.addWidget(self.dragdrop_button, 0, 4)

        # self.layout.setRowStretch(1,1)
        self.layout.setRowStretch(self.layout.rowCount(), 1)
        self.layout.setColumnStretch(1,1)
        self.layout.setColumnStretch(self.layout.columnCount(), 1)

        self.connect(self.centerOn_button, SIGNAL("clicked()"), self.slot_centerOn)
        self.connect(self.dragdrop_button, SIGNAL("clicked(bool)"), self.slot_swith_dragMode)
        self.connect(self.population_button, SIGNAL("clicked(bool)"), self.slot_add_population)

        self.scene.sig_isProjectionPrepared.connect(self.slot_changeCursor)

        self.pop_menu = PopulationMenu()
        self.connect(self.pop_menu.action_projection, SIGNAL("triggered()"), self.scene.setProjectionPrepared)
        self.connect(self.pop_menu.action_neuron, SIGNAL("triggered()"), self.scene.slot_set_neuron)
        self.connect(self.pop_menu.action_monitor, SIGNAL("triggered()"), self.scene.slot_monitor)

        self.proj_menu = ProjectionMenu()
        self.connect(self.proj_menu.action_connector, SIGNAL("triggered()"), self.scene.slot_set_connector)
        self.connect(self.proj_menu.action_synapse, SIGNAL("triggered()"), self.scene.slot_set_synapse)

    @property
    def currentItem(self):
        return self._currentItem

    @currentItem.setter
    def currentItem(self, item=QGraphicsItem):
        self._currentItem = item
        self.scene.currentItem = item

    def slot_changeCursor(self, isPrepared):
        if isPrepared:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def slot_centerOn(self):
        if self.scene.currentItem:
            self.centerOn(self.scene.currentItem)

    def slot_swith_dragMode(self, isPrepared):
        if isPrepared:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QGraphicsView.NoDrag)

    def slot_add_population(self, isPrepared):
        self.scene.setPopulationPrepared(isPrepared)

    def setDefault(self):
        self.population_button.setChecked(False)
        self.dragdrop_button.setChecked(False)
        self.slot_swith_dragMode(False)
        self.slot_add_population(False)
        self.scene.setDefault()

    # delete currentItem when press "del" on keyboard
    def keyPressEvent(self, e):
        if self.currentItem and e.key() == Qt.Key_Delete:
            if isinstance(self.currentItem, Population):
                self.scene.removeProjectionsOf(self.scene.currentItem)
            self.scene.removeItem(self.scene.currentItem)
            self.scene.info_stack.removeWidget(self.scene.currentItem.info)
            self.scene.currentItem = None
            self.scene.sig_replot.emit()

        if e.key() == Qt.Key_Escape:
            self.setDefault()

        self.scene.update()

    def mouseMoveEvent(self, e):
        super(MyView, self).mouseMoveEvent(e)
        if e.buttons() == Qt.LeftButton and self.currentItem:
            for item in self.scene.items():
                if isinstance(item, Projection):
                    item.update()
                    self.scene.update()

    def mouseDoubleClickEvent(self, e):
        if self.currentItem and e.button() == Qt.LeftButton:
            if isinstance(self.currentItem, Population):
                self.currentItem.info.openNeuronDefinition(self.currentItem.info.currentData.get("neuron"))
            if isinstance(self.currentItem, Projection):
                self.currentItem.info.openSynapseDefinition(self.currentItem.info.currentData.get("synapse"))

    def mousePressEvent(self, e):
        super(MyView, self).mousePressEvent(e)
        if self.dragMode() == QGraphicsView.NoDrag:
            self.currentItem = self.scene.itemAt(self.mapToScene(e.pos()))

        if self.currentItem:
            for item in self.scene.items():
                item.setSelected(False)
            self.currentItem.setSelected(True)

        if e.button() == Qt.LeftButton:
            """add a new Population"""
            if self.currentItem is None and self.scene.isPopulationPrepared:
                self.scene.isProjectionPrepared = False
                self.scene.addPopulation(self.mapToScene(e.pos()))
            """show info of Item"""
            if self.currentItem:
                index = self.scene.info_stack.indexOf(self.currentItem.info)
                self.scene.info_stack.setCurrentIndex(index)
            """add a new Projection"""
            if isinstance(self.currentItem, Population) and self.scene.isProjectionPrepared:
                self.dest = self.currentItem
                self.scene.addProjection(self.source, self.dest)
                self.setCursor(Qt.ArrowCursor)
                self.scene.isProjectionPrepared = False

        if e.button() == Qt.RightButton:
            if self.scene.currentItem is None:
                self.setDefault()

            if isinstance(self.currentItem, Population):
                self.source = self.currentItem
                self.pop_menu.exec_(e.globalPos())

            if isinstance(self.currentItem, Projection):
                self.proj_menu.exec_(e.globalPos())


class MyScene(QGraphicsScene):
    sig_replot = pyqtSignal()
    sig_isProjectionPrepared = pyqtSignal(bool)

    def __init__(self):
        super(MyScene, self).__init__()
        self.setItemIndexMethod(QGraphicsScene.BspTreeIndex)
        self.setSceneRect(0, 0, 1920, 1080)

        self.data = UiData()

        self.currentItem = None
        self.isPopulationPrepared = False
        self.isProjectionPrepared = False
        self.info_stack = QStackedWidget()

    def setDefault(self):
        self.setPopulationPrepared(False)
        self.setProjectionPrepared(False)

    def setPopulationPrepared(self, isPrepared):
        self.isPopulationPrepared = isPrepared

    def setProjectionPrepared(self, isPrepared=bool):
        if type(isPrepared) is bool:
            self.isProjectionPrepared = isPrepared
        else:
            self.isProjectionPrepared = True
        self.sig_isProjectionPrepared.emit(self.isProjectionPrepared)

    def slot_monitor(self):
        if isinstance(self.currentItem, Population):
            self.currentItem.info.openMonitorDialog()

    def slot_set_neuron(self):
        if isinstance(self.currentItem, Population):
            self.currentItem.info.openNeuronDefinition(self.currentItem.info.currentData.get("neuron"))

    def slot_set_synapse(self):
        if isinstance(self.currentItem, Projection):
            self.currentItem.info.openSynapseDefinition(self.currentItem.info.currentData.get("synapse"))

    def slot_set_connector(self):
        if isinstance(self.currentItem, Projection):
            self.currentItem.info.openConnectorDefinition(self.currentItem.info.currentData.get("connector"))

    def update(self, *__args):
        super(MyScene, self).update()
        rect = self.itemsBoundingRect()
        rect = rect.united(self.sceneRect())
        self.setSceneRect(rect)
        if self.currentItem:
            self.currentItem.info.update()

    def addPopulation(self, pos=QPointF):
        item = Population(self.data.neurons)
        item.setPos(pos)
        self.addItem(item)
        self.info_stack.addWidget(item.info)
        item.info.sig_neuron.connect(self.updateNeurondict)
        return item.info

    # synchronize neuron types to all Populations
    def updateNeurondict(self, nd):
        self.data.neurons.update(nd)
        for item in self.items():
            if isinstance(item, Population):
                item.info.synchronizeDict(self.data.neurons)

    def addProjection(self, source, dest):
        projection = Projection(source, dest, self.data.synapses)
        for item in self.items():
            if isinstance(item, Projection) and item.isSameTo(projection):
                return
        self.addItem(projection)
        self.info_stack.addWidget(projection.info)
        projection.info.sig_synapse.connect(self.updateSynapsedict)
        self.source = None
        self.dest = None
        return projection.info

    # synchronize synapse types to all Projections
    def updateSynapsedict(self, sd):
        self.data.synapses.update(sd)
        for item in self.items():
            if isinstance(item, Projection):
                item.info.synchronizeDict(self.data.synapses)

    def removeProjectionsOf(self, item):
        for proj in self.items():
            if isinstance(proj, Projection) and proj.contains(item.pos()):
                self.info_stack.removeWidget(proj.info)
                self.removeItem(proj)
                self.update()


class Projection(QGraphicsPathItem):
    ArrowSize = 14
    LineWidth = 4

    pen = QPen()
    pen.setWidth(LineWidth)
    pen.setJoinStyle(Qt.MiterJoin)

    brush = QBrush()
    brush.setStyle(Qt.SolidPattern)

    def __init__(self, sourceNode, destNode, synapsedict=dict):
        super(Projection, self).__init__()

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.source = sourceNode
        self.dest = destNode

        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()

        self.setPath(self.generatePath())

        if type(synapsedict) == dict:
            self.info = Informations.ProjectionInfo(self.source, self.dest, synapsedict)
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

    def generatePath(self, color=None):
        qpath = QPainterPath()

        if isinstance(color, QColor):
            self.pen.setColor(color)
            self.brush.setColor(color)

        self.setPen(self.pen)

        dist = QLineF(self.sourcePoint, self.destPoint).length()

        if dist > 0:

            self.setBrush(self.brush)

            l = QLineF(self.sourcePoint, self.destPoint)
            l.setLength(l.length() - Population.SIZE / 2 * math.sqrt(2) - Projection.ArrowSize)
            self.endPoint = l.p2()
            l.setLength(Population.SIZE / 2 * math.sqrt(2))
            self.beginPoint = l.p2()

            # begin painting
            l = QLineF(self.beginPoint, self.endPoint)
            v1 = l.unitVector()
            l.setLength(l.length() - Population.SIZE / 2 * math.sqrt(2))
            v1.setLength(Projection.ArrowSize)
            # this is important
            v1.translate(self.endPoint - self.beginPoint)

            v2 = v1.normalVector()
            v2.setLength(v1.length() * 0.3)
            v3 = v2.normalVector().normalVector()

            p0 = v1.p1()
            p1 = v1.p2()
            p2 = v2.p2()
            p3 = v3.p2()

            if dist > Population.SIZE * math.sqrt(2) + self.ArrowSize:
                qpath.moveTo(self.beginPoint)
                qpath.lineTo(self.endPoint)
                qpath.addPolygon(QPolygonF([p0, p2, p1, p3, p0]))
                v3.setLength(20)
                qpath.translate(v3.p2() - v3.p1())
        else:

            rect = QRectF(0, 0, Population.neuron_size * math.sqrt(2) * 2, Population.neuron_size * math.sqrt(2) * 2)
            # begin draw arrow
            v1 = QLineF(rect.topLeft(), rect.bottomLeft()).unitVector()
            v1.setLength(self.ArrowSize)
            v1.translate(QPointF(rect.left(), rect.center().y() - self.ArrowSize / 2) - rect.topLeft())
            v2 = v1.normalVector()
            v2.setLength(v1.length() * 0.3)
            v3 = v2.normalVector().normalVector()

            p0 = v1.p1()
            p1 = v1.p2()
            p2 = v2.p2()
            p3 = v3.p2()

            qpath.moveTo(rect.center().x() + Population.neuron_size, rect.center().y() - Population.neuron_size)
            qpath.arcTo(rect, 45, 270)
            qpath.moveTo(p0)
            qpath.addPolygon(QPolygonF([p0, p2, p1, p3, p0]))

            qpath.translate(
                    self.sourcePoint.x() - Population.neuron_size * (math.sqrt(2) + 1),
                    self.sourcePoint.y() - Population.neuron_size * math.sqrt(2)
            )

        return qpath

    def update(self):
        super(Projection, self).update()
        self.sourcePoint = self.source.scenePos()
        self.destPoint = self.dest.scenePos()
        self.setPath(self.generatePath())
        self.info.update()

    def boundingRect(self):
        return super(Projection, self).boundingRect()

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        super(Projection, self).paint(QPainter, QStyleOptionGraphicsItem, None)
        QPainter.setPen(self.pen)
        if self.isSelected():
            self.setPath(self.generatePath(QColor(Qt.red)))
        else:
            self.setPath(self.generatePath(QColor(Qt.black)))


class Population(QGraphicsItem):
    SIZE = 90
    neuron_size = 30
    font_size = 12

    font = QFont()
    font.setPointSize(font_size)

    pen = QPen()
    pen.setStyle(Qt.DashLine)

    def __init__(self, neurondict=dict):
        super(Population, self).__init__()
        self.pix = QPixmap("image/population.png").scaled(self.SIZE, self.SIZE)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        # make sure items alway above edges
        self.setZValue(1)

        self.info = Informations.PopulationInfo(neurondict)

    def boundingRect(self):
        return QRectF(
                -self.SIZE * 0.5 - 3,
                -self.SIZE * 0.5 - self.font_size * 1.5,
                self.SIZE + 6,
                self.SIZE + self.font_size * 1.5 * 2
        )

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):

        QPainter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)

        QPainter.setFont(self.font)
        """write name of population"""
        QPainter.drawText(self.boundingRect(), Qt.AlignBottom | Qt.AlignHCenter, self.info.currentData.get("name"))
        """write geometry of population"""
        QPainter.drawText(self.boundingRect(), Qt.AlignTop | Qt.AlignHCenter, self.info.currentData.get("geometry"))

        QPainter.setPen(self.pen)
        if self.isSelected():
            QPainter.drawRoundRect(self.boundingRect())
