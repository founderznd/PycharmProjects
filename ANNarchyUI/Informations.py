# coding: utf-8

from ast import literal_eval

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui import Population_Information, Neuron_Definition, Projection_Information, Synapse_Definition, \
    Connector_Definition


# this class is used to store all Informations of Population
class PopulationInfo(QWidget):
    sig_neuron = pyqtSignal(dict, list)
    sig_name = pyqtSignal(QString)

    def __init__(self, neurondict=None, neuronlist=None):
        super(PopulationInfo, self).__init__()
        self.ui = Population_Information.Ui_Form()
        self.ui.setupUi(self)

        # all parameters will be saved in this dictionary
        self.currentData = {
            "name"    : "",
            "geometry": "",
            "neuron"  : "LeakyIntegratorNeuron"
        }
        # self.preData = self.currentData
        # geometry infos saved in this tuple
        self.geo_tuple = None

        # regular expression matches (a1,a2,...,an)
        self.rx = QRegExp("\( *\d+ *(, *\d+ *)*\)")

        self.dialog = QDialog()
        self.dui = Neuron_Definition.Ui_Dialog()
        self.dui.setupUi(self.dialog)

        self.currentNeuron = {
            "name"       : "",
            "description": "",
            "parameters" : "",
            "equations"  : "",
            "functions"  : "",
            "spike"      : "",
            "reset"      : "",
            "refractory" : 0
        }
        # store different kinds of neuron
        self.neurondict = dict()
        self.neuronlist = [self.ui.comboBox_neuron_type.itemText(i) for i in
                           range(self.ui.comboBox_neuron_type.count())]

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

        if neurondict:
            self.neurondict.update(neurondict)
            self.neuronlist = neuronlist
            for item in self.neuronlist:
                if self.ui.comboBox_neuron_type.findText(item) == -1:
                    self.ui.comboBox_neuron_type.insertItem(self.ui.comboBox_neuron_type.count(), item)

        self.ui.comboBox_neuron_type.setCurrentIndex(
                self.ui.comboBox_neuron_type.findText(self.currentData.get("neuron")))

        self.connect(self.ui.comboBox_neuron_type, SIGNAL("activated(QString)"), self.openNeuronDefinition)
        self.connect(self.ui.name, SIGNAL("editingFinished()"), self.slot_updateName)
        self.connect(self.ui.geometry, SIGNAL("editingFinished()"), self.slot_updateGeometry)
        self.connect(self.dui.buttonBox, SIGNAL("accepted()"), self.slot_updateNeuron)
        self.connect(self.dui.buttonBox, SIGNAL("rejected()"), self.slot_rollback)

    def synchronizeDict(self, neurondict=None, neuronlist=None):
        if type(neurondict) == dict:
            self.neurondict.update(neurondict)
            self.neuronlist = neuronlist
            for key in self.neuronlist:
                if self.ui.comboBox_neuron_type.findText(key) == -1:
                    self.ui.comboBox_neuron_type.insertItem(self.ui.comboBox_neuron_type.count(), key)

    # refresh data
    def slot_updateName(self):
        self.currentData.update({"name": self.ui.name.text()})
        self.sig_name.emit(self.ui.name.text())

    def slot_updateGeometry(self):
        self.currentData.update({"geometry": self.ui.geometry.text()})
        # use method blockSignals(bool) to prevent SIGNAL("editingFinished()") emit twice when man press ENTER
        # it seems like a bug of QT
        # https://forum.qt.io/topic/39141/qlineedit-editingfinished-signal-is-emitted-twice/2
        self.ui.geometry.blockSignals(True)
        # make sure the geometry is valid
        geometry = self.currentData.get("geometry")
        if geometry:
            pos = self.rx.indexIn(geometry)
            if pos == -1:
                QMessageBox().information(None, "error", "please type paramters like (a1,a2,...,an)")
                self.currentData.update({"geometry": ""})
                self.ui.geometry.setText("")
            else:  # clean blanks
                strl = self.rx.capturedTexts()
                strl[0] = strl[0].remove(" ")
                self.ui.geometry.setText(strl[0])
                self.currentData.update({"geometry": strl[0]})
                # convert QString to Tuple
                self.geo_tuple = literal_eval(str(strl[0]))
        self.ui.geometry.blockSignals(False)

    def slot_updateNeuron(self):
        neuron_name = self.dui.neurontype.text()
        if not neuron_name.isEmpty():
            self.currentData.update({"neuron": neuron_name})
            temp = {}
            temp.update({"name": self.dui.neurontype.text()})
            temp.update({"parameters": self.dui.parameter.toPlainText()})
            temp.update({"equations": self.dui.equation.toPlainText()})
            temp.update({"spike": self.dui.spike.toPlainText()})
            temp.update({"reset": self.dui.reset.toPlainText()})
            temp.update({"refractory": self.dui.doubleSpinBox_refractory.value()})
            temp.update({"functions": self.dui.plainTextEdit_function.toPlainText()})
            temp.update({"description": self.dui.plainTextEdit_description.toPlainText()})
            self.currentNeuron = temp
            self.neurondict.update({str(neuron_name): self.currentNeuron})
            self.neuronlist.append(str(neuron_name))
            # add a neu type of neuron
            if self.ui.comboBox_neuron_type.findText(neuron_name) == -1:
                self.ui.comboBox_neuron_type.insertItem(self.ui.comboBox_neuron_type.count(), neuron_name)
            self.ui.comboBox_neuron_type.setCurrentIndex(self.ui.comboBox_neuron_type.findText(neuron_name))

        self.sig_neuron.emit(self.neurondict, self.neuronlist)
        self.dialog.accept()

    # data rollback
    def slot_rollback(self):
        self.ui.comboBox_neuron_type.setCurrentIndex(
                self.ui.comboBox_neuron_type.findText(self.currentData.get("neuron")))
        self.dialog.reject()

    def openNeuronDefinition(self, s):
        self.dui.tabWidget.setCurrentIndex(0)
        # self.preData.update(self.currentData)
        neuron = self.neurondict.get(str(s))
        if neuron:
            self.dui.neurontype.setText(neuron.get("name"))
            self.dui.parameter.setPlainText(neuron.get("parameters"))
            self.dui.equation.setPlainText(neuron.get("equations"))
            self.dui.spike.setPlainText(neuron.get("spike"))
            self.dui.reset.setPlainText(neuron.get("reset"))
            self.dui.doubleSpinBox_refractory.setValue(neuron.get("refractory"))
            self.dui.plainTextEdit_function.setPlainText(neuron.get("functions"))
            self.dui.plainTextEdit_description.setPlainText(neuron.get("description"))
            self.dui.neurontype.setReadOnly(True)
        else:
            self.dui.neurontype.clear()
            self.dui.parameter.clear()
            self.dui.equation.clear()
            self.dui.spike.clear()
            self.dui.reset.clear()
            self.dui.doubleSpinBox_refractory.clear()
            self.dui.plainTextEdit_function.clear()
            self.dui.plainTextEdit_description.clear()
            self.dui.neurontype.setReadOnly(False)

        # here changes the layout of each neuron type
        if s == "LeakyIntegratorNeuron":
            self.dui.tabWidget.setTabEnabled(2, False)
        else:
            self.dui.tabWidget.setTabEnabled(2, True)

        self.dialog.show()


class ProjectionInfo(QWidget):
    sig_synapse = pyqtSignal(dict, list)
    sig_connector = pyqtSignal(list, QObject)

    def __init__(self, source=None, dest=None, synapsedict=None, synapselist=None, connectorlist=None):
        super(ProjectionInfo, self).__init__()
        self.ui = Projection_Information.Ui_Form()
        self.ui.setupUi(self)
        # Projection
        self.currentData = {
            "name"   : "",
            "pre"    : source,
            "post"   : dest,
            "target" : "",
            "synapse": "Oja"
        }

        self.pre = source
        self.post = dest
        self.currentConnector = ""

        self.connectorlist = [self.ui.comboBox_connectivity.itemText(i) for i in
                              range(self.ui.comboBox_connectivity.count())]

        self.synapsedict = dict()
        self.synapselist = [self.ui.comboBox_synapse_type.itemText(i) for i in
                            range(self.ui.comboBox_synapse_type.count())]

        # Synapse
        self.currentSynapse = {
            "parameters" : "",
            "equations"  : "",
            "psp"        : "",
            "pre_spike"  : "",
            "post_spike" : "",
            "functions"  : "",
            "name"       : "",
            "description": ""
        }

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

        if len(connectorlist) > 12:
            self.connectorlist = connectorlist
            for item in self.connectorlist:
                if self.ui.comboBox_connectivity.findText(item) == -1:
                    self.ui.comboBox_connectivity.addItem(item)

        if synapsedict:
            self.synapsedict.update(synapsedict)
            self.synapselist = synapselist
            for key in self.synapselist:
                if self.ui.comboBox_synapse_type.findText(key) == -1:
                    self.ui.comboBox_synapse_type.insertItem(self.ui.comboBox_synapse_type.count(), key)

        self.ui.comboBox_synapse_type.setCurrentIndex(
                self.ui.comboBox_synapse_type.findText(self.currentData.get("synapse")))

        self.ui.label_pos_Pop.setText(self.post.info.currentData.get("name"))
        self.ui.label_pre_Pop.setText(self.pre.info.currentData.get("name"))

        self.dialog = QDialog()
        self.sui = Synapse_Definition.Ui_Dialog()
        self.sui.setupUi(self.dialog)

        self.stack = QDialog()
        self.stack_ui = Connector_Definition.Ui_Dialog()
        self.stack_ui.setupUi(self.stack)

        """connect signal to slot"""
        self.ui.comboBox_connectivity.activated.connect(self.openConnectorDefinition)
        self.stack_ui.buttonBox.accepted.connect(self.slot_accept_connector)
        self.stack_ui.comboBox_connectivity.activated.connect(self.stack_ui.stackedWidget.setCurrentIndex)
        self.stack_ui.pushButton_openfile.clicked.connect(self.slot_openfile)

        self.ui.comboBox_synapse_type.activated[QString].connect(self.openSynapseDefinition)
        self.ui.lineEdit_name.editingFinished.connect(self.slot_updateName)
        self.ui.lineEdit_target.editingFinished.connect(self.slot_updateTarget)
        self.sui.buttonBox.accepted.connect(self.slot_updateSynapse)
        self.sui.buttonBox.rejected.connect(self.slot_rollback)
        self.pre.info.sig_name.connect(self.slot_updatePre)
        self.post.info.sig_name.connect(self.slot_updatePost)

    def openConnectorDefinition(self, index):
        self.stack.show()
        for item in self.connectorlist:
            if self.stack_ui.comboBox_connectivity.findText(item) == -1:
                self.stack_ui.comboBox_connectivity.addItem(item)
        self.stack_ui.comboBox_connectivity.setCurrentIndex(index)
        self.stack_ui.stackedWidget.setCurrentIndex(index)

    def slot_accept_connector(self):
        self.ui.comboBox_connectivity.setCurrentIndex(self.stack_ui.comboBox_connectivity.currentIndex())
        """update current connector"""
        self.currentConnector = self.ui.comboBox_connectivity.currentText()
        if self.currentConnector == "Define Own...":
            item = self.stack_ui.page_defineown_name.text()
            if not item.isEmpty() and self.connectorlist.count(item) == 0:
                self.connectorlist.append(self.stack_ui.page_defineown_name.text())
                self.ui.comboBox_connectivity.addItem(item)
                self.ui.comboBox_connectivity.setCurrentIndex(self.ui.comboBox_connectivity.findText(item))
                # todo 这里加入新的widget，每个widget对应一个新的connector类
                newConnector = QWidget()
                vbox = QVBoxLayout(newConnector)
                vbox.addWidget(QLabel(item))
                self.stack_ui.stackedWidget.addWidget(newConnector)
                self.sig_connector.emit(self.connectorlist, newConnector)

    def sychronizeConnector(self, cl=None):
        if type(cl) == list:
            self.connectorlist = cl
            for key in self.connectorlist:
                if self.ui.comboBox_connectivity.findText(key) == -1:
                    self.ui.comboBox_connectivity.addItem(key)

    def slot_openfile(self):
        self.filename = QFileDialog().getOpenFileName(self, "Data", QDir.currentPath(), "*.data;;*.*")

    def slot_updatePre(self, name):
        self.ui.label_pre_Pop.setText(name)

    def slot_updatePost(self, name):
        self.ui.label_pos_Pop.setText(name)

    def synchronizeDict(self, syn=None, sl=None):
        if type(syn) == dict:
            self.synapsedict.update(syn)
            self.synapselist = sl
            for key in self.synapselist:
                if self.ui.comboBox_synapse_type.findText(key) == -1:
                    self.ui.comboBox_synapse_type.insertItem(self.ui.comboBox_synapse_type.count(), key)

    def slot_rollback(self):
        self.ui.comboBox_synapse_type.setCurrentIndex(
                self.ui.comboBox_synapse_type.findText(self.currentData.get("synapse")))
        self.dialog.reject()

    def slot_updateName(self):
        self.currentData.update({"name": self.ui.lineEdit_name.text()})

    def slot_updateTarget(self):
        self.currentData.update({"target": self.ui.lineEdit_target.text()})

    def slot_updateSynapse(self):
        synapse_name = self.sui.lineEdit_name.text()
        if not synapse_name.isEmpty():
            self.currentData.update({"synapse": self.sui.lineEdit_name.text()})
            tmp = {}
            tmp.update({"name": self.sui.lineEdit_name.text()})
            tmp.update({"description": self.sui.plainTextEdit_description.toPlainText()})
            tmp.update({"parameters": self.sui.plainTextEdit_parameter.toPlainText()})
            tmp.update({"equations": self.sui.plainTextEdit_equation.toPlainText()})
            tmp.update({"functions": self.sui.plainTextEdit_function.toPlainText()})
            tmp.update({"pre_spike": self.sui.plainTextEdit_pre_spike.toPlainText()})
            tmp.update({"post_spike": self.sui.plainTextEdit_pos_spike.toPlainText()})
            tmp.update({"psp": self.sui.plainTextEdit_psp.toPlainText()})

            self.currentSynapse = tmp
            self.synapsedict.update({str(synapse_name): self.currentSynapse})
            self.synapselist.append(str(synapse_name))
            # add a neu type of neuron
            if self.ui.comboBox_synapse_type.findText(synapse_name) == -1:
                self.ui.comboBox_synapse_type.insertItem(self.ui.comboBox_synapse_type.count(), synapse_name)
            self.ui.comboBox_synapse_type.setCurrentIndex(self.ui.comboBox_synapse_type.findText(synapse_name))

        self.sig_synapse.emit(self.synapsedict, self.synapselist)
        self.dialog.accept()

    def openSynapseDefinition(self, s):
        self.sui.tabWidget.setCurrentIndex(0)
        synapse = self.synapsedict.get(str(s))
        if synapse:
            self.sui.plainTextEdit_parameter.setPlainText(synapse.get("parameters"))
            self.sui.plainTextEdit_equation.setPlainText(synapse.get("equations"))
            self.sui.plainTextEdit_psp.setPlainText(synapse.get("psp"))
            self.sui.plainTextEdit_pre_spike.setPlainText(synapse.get("pre_spike"))
            self.sui.plainTextEdit_pos_spike.setPlainText(synapse.get("post_spike"))
            self.sui.plainTextEdit_function.setPlainText(synapse.get("functions"))
            self.sui.plainTextEdit_description.setPlainText(synapse.get("description"))
            self.sui.lineEdit_name.setText(synapse.get("name"))
            self.sui.lineEdit_name.setReadOnly(True)
        else:
            self.sui.plainTextEdit_parameter.clear()
            self.sui.plainTextEdit_equation.clear()
            self.sui.plainTextEdit_psp.clear()
            self.sui.plainTextEdit_pre_spike.clear()
            self.sui.plainTextEdit_pos_spike.clear()
            self.sui.plainTextEdit_function.clear()
            self.sui.plainTextEdit_description.clear()
            self.sui.lineEdit_name.clear()
            self.sui.lineEdit_name.setReadOnly(False)

        self.dialog.show()
