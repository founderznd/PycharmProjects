# coding: utf-8

from ast import literal_eval

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui import Population_Information, Neuron_Definition, Projection_Information, Synapse_Definition


# this class is used to store all Informations of Population
class PopulationInfo(QWidget):
    sig_neuron = pyqtSignal(dict)
    sig_name = pyqtSignal(QString)

    def __init__(self, neurondict=None):
        super(PopulationInfo, self).__init__()
        self.ui = Population_Information.Ui_Form()
        self.ui.setupUi(self)

        # all parameters will be saved in this dictionary
        self.ui.comboBox_neuron_type.setCurrentIndex(self.ui.comboBox_neuron_type.findText("LeakyIntegratorNeuron"))
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
        # a map for different kinds of neuron
        self.neurondict = dict()

        # neurondict initialization
        self.neurondict.update({
            "LeakyIntegratorNeuron": {
                "name"       : "LeakyIntegratorNeuron",
                "description": "",
                "parameters" : "",
                "equations"  : "",
                "functions"  : "",
                "spike"      : "",
                "reset"      : "",
                "refractory" : 0
            }
        })
        self.neurondict.update({
            "Izhikevich": {
                "name"       : "Izhikevich",
                "description": """
                    This script reproduces the simple pulse-coupled network proposed by Eugene Izhikevich in the
                    article:Izhikevich, E.M. (2003). Simple Model of Spiking Neurons, IEEE Transaction on Neural
                    Networks, 14:6.
                """,
                "parameters" : """
                    noise = 5.0 : population
                    a = 0.02
                    b = 0.2
                    c = -65.0
                    d = 2.0
                    v_thresh = 30.0
                """,
                "equations"  : """
                    I = g_exc - g_inh + noise * Normal(0.0, 1.0)
                    dv/dt = 0.04 * v^2 + 5.0 * v + 140.0 - u + I
                    du/dt = a * (b*v - u)
                """,
                "functions"  : """
                """,
                "spike"      : """
                    v >= v_thresh
                """,
                "reset"      : """
                    v = c
                    u += d
                """,
                "refractory" : 0
            }
        })
        if neurondict:
            self.neurondict.update(neurondict)
            for key in self.neurondict.keys():
                if self.ui.comboBox_neuron_type.findText(key) == -1:
                    self.ui.comboBox_neuron_type.insertItem(self.ui.comboBox_neuron_type.count(), key)

        self.connect(self.ui.comboBox_neuron_type, SIGNAL("activated(QString)"), self.openDialog)
        self.connect(self.ui.name, SIGNAL("editingFinished()"), self.slot_updateName)
        self.connect(self.ui.geometry, SIGNAL("editingFinished()"), self.slot_updateGeometry)
        self.connect(self.dui.buttonBox, SIGNAL("accepted()"), self.slot_updateNeuron)
        self.connect(self.dui.buttonBox, SIGNAL("rejected()"), self.slot_rollback)

    def synchronizeDict(self, neurondict=None):
        if type(neurondict) == dict:
            self.neurondict.update(neurondict)
            for key in self.neurondict.keys():
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
            self.addNeuron(temp)
            self.ui.comboBox_neuron_type.setCurrentIndex(self.ui.comboBox_neuron_type.findText(neuron_name))

        self.neurondict.update({str(neuron_name): self.currentNeuron})
        # self.emit(SIGNAL("neuron(PyQt_PyObject)"), self.neurondict)
        self.sig_neuron.emit(self.neurondict)
        self.dialog.accept()

    def addNeuron(self, neuron):
        neuron_name = neuron.get("name")
        # add a neu type of neuron
        if self.ui.comboBox_neuron_type.findText(neuron_name) == -1:
            self.ui.comboBox_neuron_type.insertItem(self.ui.comboBox_neuron_type.count(), neuron_name)

    # data rollback
    def slot_rollback(self):
        self.ui.comboBox_neuron_type.setCurrentIndex(
                self.ui.comboBox_neuron_type.findText(self.currentData.get("neuron")))
        self.dialog.reject()

    def openDialog(self, s):
        self.dui.tabWidget.setCurrentIndex(0)
        # self.preData.update(self.currentData)
        neuron = self.neurondict.get(str(s))
        if neuron:
            # self.dui.neurontype.setText(str(self.ui.comboBox_neuron_type.currentText()))
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

        self.dialog.exec_()


class ProjectionInfo(QWidget):
    sig_synapse = pyqtSignal(dict)

    def __init__(self, source=None, dest=None, synapsedict=None):
        super(ProjectionInfo, self).__init__()
        self.ui = Projection_Information.Ui_Form()
        self.ui.setupUi(self)
        # Projection
        self.ui.comboBox_synapse_type.setCurrentIndex(self.ui.comboBox_synapse_type.findText("Rate-coded synapse"))
        self.currentData = {
            "name"   : "",
            "pre"    : source,
            "post"   : dest,
            "target" : "",
            "synapse": "Rate-coded synapse"
        }

        self.pre = source
        self.post = dest
        self.synapsedict = dict()

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
            "Rate-coded synapse": {
                "parameters" : "",
                "equations"  : "",
                "psp"        : "",
                "pre_spike"  : "",
                "post_spike" : "",
                "functions"  : "",
                "name"       : "Rate-coded synapse",
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

        if synapsedict:
            self.synapsedict.update(synapsedict)
            for key in self.synapsedict.keys():
                if self.ui.comboBox_synapse_type.findText(key) == -1:
                    self.ui.comboBox_synapse_type.insertItem(self.ui.comboBox_synapse_type.count(), key)

        self.ui.label_pos_Pop.setText(self.post.info.currentData.get("name"))
        self.ui.label_pre_Pop.setText(self.pre.info.currentData.get("name"))

        self.dialog = QDialog()
        self.sui = Synapse_Definition.Ui_Dialog()
        self.sui.setupUi(self.dialog)

        self.ui.comboBox_synapse_type.activated.connect(self.openDialog)
        self.ui.lineEdit_name.editingFinished.connect(self.slot_updateName)
        self.ui.lineEdit_target.editingFinished.connect(self.slot_updateTarget)
        self.sui.buttonBox.accepted.connect(self.slot_updateSynapse)
        self.sui.buttonBox.rejected.connect(self.slot_rollback)
        self.pre.info.sig_name.connect(self.slot_updatePre)
        self.post.info.sig_name.connect(self.slot_updatePost)

    def slot_updatePre(self, pre):
        self.ui.label_pre_Pop.setText(pre)

    def slot_updatePost(self, post):
        self.ui.label_pos_Pop.setText(post)

    def synchronizeDict(self, syn=None):
        if type(syn) == dict:
            self.synapsedict.update(syn)
            for key in self.synapsedict.keys():
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
            self.addSynapse(self.currentSynapse)
            self.ui.comboBox_synapse_type.setCurrentIndex(self.ui.comboBox_synapse_type.findText(synapse_name))

        self.synapsedict.update({str(self.currentSynapse.get("name")): self.currentSynapse})
        self.sig_synapse.emit(self.synapsedict)
        self.dialog.accept()

    def addSynapse(self, neuron):
        neuron_name = neuron.get("name")
        # add a neu type of neuron
        if self.ui.comboBox_synapse_type.findText(neuron_name) == -1:
            self.ui.comboBox_synapse_type.insertItem(self.ui.comboBox_synapse_type.count(), neuron_name)

    def openDialog(self, s):
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

        self.dialog.exec_()
