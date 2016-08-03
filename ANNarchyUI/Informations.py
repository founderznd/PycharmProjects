# coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui import Population_Information, Neuron_Definition, Projection_Information, Synapse_Definition, \
    Connector_Definition, MonitorUI


# this class is used to store all Informations of Population
class PopulationInfo(QWidget):
    sig_neuron = pyqtSignal(dict, list)  # synchronize the neuron list of each population
    sig_name = pyqtSignal(QString)  # synchronize the names of pre_Pop and post_Pop in projection

    def __init__(self, neurondict=None, neuronlist=None):
        super(PopulationInfo, self).__init__()

        self.ui = Population_Information.Ui_Form()
        self.ui.setupUi(self)

        # all parameters will be saved in this dictionary
        self.currentData = {
            "name"      : "",
            "geometry"  : "",
            "neuron"    : "PoissonNeuron",
            "parameters": "amp = 100.0\n"
                          "frequency = 1.0",
            "rates"     : "amp * (1.0 + sin(2*pi*frequency*t/1000.0) )/2.0"
        }

        # dialog for neuron definition
        self.neuron_dialog = QDialog()
        self.nui = Neuron_Definition.Ui_Dialog()
        self.nui.setupUi(self.neuron_dialog)

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
        self.neuronlist = list()

        self.synchronizeDict(neurondict, neuronlist)

        self.ui.comboBox_neuron_type.setCurrentIndex(
                self.ui.comboBox_neuron_type.findText(self.currentData.get("neuron")))

        self.currentMonitor = {
            "enabled"  : False,
            "obj"      : "",
            "variables": "",
            "period"   : 1.0,
            "start"    : True
        }
        self.setCurrentMonitor()
        self.monitor_dialog = QDialog()
        self.mui = MonitorUI.Ui_Dialog()

        """signal and slot"""
        """ui"""
        self.ui.comboBox_neuron_type.activated[QString].connect(self.openNeuronDefinition)
        self.ui.name.textChanged.connect(self.slot_updateName)
        self.ui.geometry.editingFinished.connect(self.slot_updateGeometry)
        """neuron"""
        self.nui.buttonBox.accepted.connect(self.slot_updateNeuron)
        self.nui.buttonBox.rejected.connect(self.slot_rollback)
        self.nui.comboBox_neuron_type.activated[QString].connect(self.openNeuronDefinition)
        """monitor"""
        self.ui.groupBox_monitor.toggled.connect(self.slot_updateEnable)
        self.ui.name.textChanged.connect(self.slot_updateObj)
        self.ui.checkBox_start.toggled.connect(self.slot_updateStart)
        self.ui.doubleSpinBox_period.valueChanged.connect(self.slot_updatePeriod)
        self.ui.lineEdit_variables.textChanged.connect(self.slot_updateVariables)

    def openMonitorDialog(self):
        if self.currentMonitor.get("enabled") is True:
            if not self.monitor_dialog.layout():
                self.mui.setupUi(self.monitor_dialog)
                self.monitor_dialog.setWindowTitle("Monitor:[ " + self.ui.name.text() + " ]")
                """initial mui setting"""
                self.mui.checkBox_start.setChecked(self.currentMonitor.get("start"))
                self.mui.doubleSpinBox_period.setValue(self.currentMonitor.get("period"))
                self.mui.lineEdit_variables.setText(self.currentMonitor.get("variables"))
                """connect slot and signal after monitor is setted up"""
                self.mui.checkBox_start.toggled.connect(self.slot_updateStart)
                self.mui.doubleSpinBox_period.valueChanged.connect(self.slot_updatePeriod)
                self.mui.lineEdit_variables.textChanged.connect(self.slot_updateVariables)
                self.mui.pushButton_monitor.clicked.connect(self.slot_draw_plot)
            self.mui.widget_matplot.drawPlot(self.currentMonitor)
            self.monitor_dialog.show()
        else:
            """
            QMessageBox.information(
                QWidget,
                QString,
                QString,
                QMessageBox.StandardButtons buttons=QMessageBox.Ok,
                QMessageBox.StandardButton defaultButton=QMessageBox.NoButton
            ) -> QMessageBox.StandardButton
            """
            QMessageBox().information(
                    self,
                    "Information",
                    "Monitor is disabled",
                    QMessageBox.Ok,
                    QMessageBox.Ok
            )

    def slot_draw_plot(self):
        self.mui.widget_matplot.drawPlot(self.currentMonitor)

    def slot_updateEnable(self, isChecked):
        self.currentMonitor.update({
            "enabled": isChecked
        })
        if not isChecked:
            self.monitor_dialog.close()

    def slot_updateObj(self, s=""):
        self.currentMonitor.update({
            "obj": str(s)
        })
        self.monitor_dialog.setWindowTitle("Monitor:[ " + s + " ]")

    def slot_updateVariables(self, s=""):
        self.currentMonitor.update({
            "variables": str(s)
        })
        self.ui.lineEdit_variables.setText(s)
        if self.monitor_dialog.layout():
            self.mui.lineEdit_variables.setText(s)

    def slot_updatePeriod(self, n=0.0):
        self.currentMonitor.update({
            "period": n
        })
        self.ui.doubleSpinBox_period.setValue(n)
        if self.monitor_dialog.layout():
            self.mui.doubleSpinBox_period.setValue(n)

    def slot_updateStart(self, isChecked):
        self.currentMonitor.update({
            "start": isChecked
        })
        self.ui.checkBox_start.setChecked(isChecked)
        if self.monitor_dialog.layout():
            self.mui.checkBox_start.setChecked(isChecked)

    def setCurrentNeuron(self, currentNeuron=None):
        if isinstance(currentNeuron, dict):
            self.currentNeuron.update(currentNeuron)

    def setCurrentMonitor(self, currentMonitor=None):
        if isinstance(currentMonitor, dict):
            self.currentMonitor.update(currentMonitor)
        self.ui.groupBox_monitor.setChecked(self.currentMonitor.get("enabled"))
        self.ui.lineEdit_variables.setText(self.currentMonitor.get("variables"))
        self.ui.checkBox_start.setChecked(self.currentMonitor.get("start"))
        self.ui.doubleSpinBox_period.setValue(self.currentMonitor.get("period"))

    # synchronize currentData
    def setCurrentData(self, currentData=None):
        if isinstance(currentData, dict):
            self.currentData.update(currentData)
            self.ui.name.setText(self.currentData.get("name"))
            self.ui.geometry.setText(self.currentData.get("geometry"))
            self.ui.comboBox_neuron_type.setCurrentIndex(
                    self.ui.comboBox_neuron_type.findText(self.currentData.get("neuron")))

    # add new neuron to list if necessary
    def synchronizeDict(self, neurondict=None, neuronlist=None):
        if isinstance(neurondict, dict) and isinstance(neuronlist, list):
            self.neurondict.update(neurondict)
            # for key in neuronlist:
            #     if self.neuronlist.count(key) == 0:
            #         self.neuronlist.append(key)
            del self.neuronlist
            self.neuronlist = neuronlist
            for key in self.neuronlist:
                if self.ui.comboBox_neuron_type.findText(key) == -1:
                    self.ui.comboBox_neuron_type.insertItem(self.ui.comboBox_neuron_type.count(), key)

    # refresh data
    def slot_updateName(self):
        self.currentData.update({"name": str(self.ui.name.text())})
        self.sig_name.emit(self.ui.name.text())

    def slot_updateGeometry(self):
        # regular expression matches (a1,a2,...,an)
        rx = QRegExp("\d+ *(, *\d+ *)*")
        self.currentData.update({"geometry": str(self.ui.geometry.text())})
        # use method blockSignals(bool) to prevent SIGNAL("editingFinished()") emit twice when man press ENTER
        # it seems like a bug of QT
        # https://forum.qt.io/topic/39141/qlineedit-editingfinished-signal-is-emitted-twice/2
        self.ui.geometry.blockSignals(True)
        """make sure the geometry is valid"""
        geometry = self.currentData.get("geometry")
        if geometry:
            pos = rx.indexIn(geometry)
            if pos == -1:
                QMessageBox().information(None, "error", "please type paramters like a1,a2,...,an")
                self.currentData.update({"geometry": ""})
                self.ui.geometry.setText("")
            else:  # clean blanks
                strl = rx.capturedTexts()
                strl[0] = strl[0].remove(" ")
                self.ui.geometry.setText(strl[0])
                self.currentData.update({"geometry": str(strl[0])})
        self.ui.geometry.blockSignals(False)

    def slot_updateNeuron(self):
        neuron_name = self.nui.neurontype.text()
        if not neuron_name.isEmpty():
            self.currentData.update({"neuron": str(neuron_name)})
            temp = {}
            temp.update({"name": str(self.nui.neurontype.text())})
            temp.update({"parameters": str(self.nui.parameter.toPlainText())})
            temp.update({"equations": str(self.nui.equation.toPlainText())})
            temp.update({"spike": str(self.nui.spike.toPlainText())})
            temp.update({"reset": str(self.nui.reset.toPlainText())})
            temp.update({"functions": str(self.nui.plainTextEdit_function.toPlainText())})
            temp.update({"description": str(self.nui.plainTextEdit_description.toPlainText())})
            temp.update({"refractory": self.nui.doubleSpinBox_refractory.value()})
            if neuron_name == "PoissonNeuron":
                self.currentData.update({
                    "parameters": str(self.nui.plainTextEdit_parameters.toPlainText()),
                    "rates"     : str(self.nui.plainTextEdit_rates.toPlainText())
                })

            self.setCurrentNeuron(temp)
            self.neurondict.update({str(neuron_name): self.currentNeuron})
            # update neuronlist
            if self.neuronlist.count(neuron_name) == 0:
                self.neuronlist.append(neuron_name)
            # add a neu type of neuron
            self.synchronizeDict(self.neurondict, self.neuronlist)
            self.ui.comboBox_neuron_type.setCurrentIndex(self.ui.comboBox_neuron_type.findText(neuron_name))

        self.sig_neuron.emit(self.neurondict, self.neuronlist)
        self.neuron_dialog.accept()

    # data rollback
    def slot_rollback(self):
        self.ui.comboBox_neuron_type.setCurrentIndex(
                self.ui.comboBox_neuron_type.findText(self.currentData.get("neuron")))
        self.neuron_dialog.reject()

    def openNeuronDefinition(self, s):
        """
        open the dialog of neuron definition
        :param s:
        :type s:
        :return:
        :rtype:
        """
        """synchronize combobox_neuron_type first"""
        l = [self.ui.comboBox_neuron_type.itemText(i) for i in range(self.ui.comboBox_neuron_type.count())]
        for item in l:
            if self.nui.comboBox_neuron_type.findText(item) == -1:
                self.nui.comboBox_neuron_type.addItem(item)
        self.nui.comboBox_neuron_type.setCurrentIndex(self.ui.comboBox_neuron_type.findText(s))

        self.nui.tabWidget.setCurrentIndex(0)
        neuron = self.neurondict.get(str(s))
        if neuron:
            name = neuron.get("name")
            parameters = neuron.get("parameters")
            equations = neuron.get("equations")
            spike = neuron.get("spike")
            reset = neuron.get("reset")
            refractory = neuron.get("refractory")
            functions = neuron.get("functions")
            description = neuron.get("description")
            self.nui.neurontype.setText(name if name else "")
            self.nui.parameter.setPlainText(parameters if parameters else "")
            self.nui.equation.setPlainText(equations if equations else "")
            self.nui.spike.setPlainText(spike if spike else "")
            self.nui.reset.setPlainText(reset if reset else "")
            self.nui.doubleSpinBox_refractory.setValue(refractory if refractory else 0)
            self.nui.plainTextEdit_function.setPlainText(functions if functions else "")
            self.nui.plainTextEdit_description.setPlainText(description if description else "")
            self.nui.neurontype.setReadOnly(True)
        else:
            self.nui.neurontype.clear()
            self.nui.parameter.clear()
            self.nui.equation.clear()
            self.nui.spike.clear()
            self.nui.reset.clear()
            self.nui.doubleSpinBox_refractory.clear()
            self.nui.plainTextEdit_function.clear()
            self.nui.plainTextEdit_description.clear()
            self.nui.neurontype.setReadOnly(False)

        """modify special neuron and populaiton"""
        if s == "LeakyIntegratorNeuron":
            self.nui.tabWidget.setTabEnabled(2, False)
        else:
            self.nui.tabWidget.setTabEnabled(2, True)

        """
        the parameters and rates are actually the members of population, so they should be save and read from
        currentData
        """
        if s == "PoissonNeuron":
            self.nui.tabWidget.setTabEnabled(3, True)
            self.nui.plainTextEdit_parameters.setPlainText(self.currentData.get("parameters"))
            self.nui.plainTextEdit_rates.setPlainText(self.currentData.get("rates"))
        else:
            self.nui.tabWidget.setTabEnabled(3, False)

        self.neuron_dialog.show()


class ProjectionInfo(QWidget):
    sig_synapse = pyqtSignal(dict, list)  # synchronize the synapse list of each projection

    # sig_connector = pyqtSignal(list, QObject)

    def __init__(self, source=None, dest=None, synapsedict=None, synapselist=None, connectorlist=None):
        super(ProjectionInfo, self).__init__()
        self.ui = Projection_Information.Ui_Form()
        self.ui.setupUi(self)
        # Projection
        self.currentData = {
            "name"     : "",
            "pre"      : str(source.info.currentData.get("name")) if source else "",
            "post"     : str(dest.info.currentData.get("name")) if dest else "",
            "target"   : "",
            "synapse"  : "None",
            "connector": "connect_one_to_one"
        }

        self.pre = source
        self.post = dest
        self.ui.comboBox_connector.setCurrentIndex(
                self.ui.comboBox_connector.findText(self.currentData.get("connector")))

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

        self.synapsedict = dict()
        self.synapselist = list()

        # synapse definition UI
        self.synapse_dialog = QDialog()
        self.synapse_ui = Synapse_Definition.Ui_Dialog()
        self.synapse_ui.setupUi(self.synapse_dialog)

        # Connector
        self.currentConnector = {
            "id": ""
        }
        self.connectorlist = [self.ui.comboBox_connector.itemText(i) for i in
                              range(self.ui.comboBox_connector.count())]
        # self.connectordict = dict()

        # connector definition UI
        self.connector_dialog = QDialog()
        self.connector_ui = Connector_Definition.Ui_Dialog()
        self.connector_ui.setupUi(self.connector_dialog)

        self.synchronizeDict(synapsedict, synapselist)
        self.synchronizeConnector()
        self.ui.comboBox_synapse_type.setCurrentIndex(
                self.ui.comboBox_synapse_type.findText(self.currentData.get("synapse")))

        self.ui.label_pos_Pop.setText(self.currentData.get("post"))
        self.ui.label_pre_Pop.setText(self.currentData.get("pre"))

        """ui"""
        self.ui.comboBox_synapse_type.activated[QString].connect(self.openSynapseDefinition)
        self.ui.lineEdit_name.editingFinished.connect(self.slot_updateName)
        self.ui.lineEdit_target.editingFinished.connect(self.slot_updateTarget)
        self.pre.info.sig_name.connect(self.slot_updatePre)
        self.post.info.sig_name.connect(self.slot_updatePost)
        """synpase ui"""
        self.synapse_ui.comboBox_synapse_type.activated[QString].connect(self.openSynapseDefinition)
        self.synapse_ui.buttonBox.accepted.connect(self.slot_updateSynapse)
        self.synapse_ui.buttonBox.rejected.connect(self.slot_rollback)

        """connect combobox to stackwidget"""
        self.connector_ui.buttonBox.accepted.connect(self.slot_updateConnector)
        self.connector_ui.buttonBox.rejected.connect(self.slot_rollback)
        self.ui.comboBox_connector.activated[QString].connect(self.openConnectorDefinition)
        # self.ui.comboBox_connector.activated.connect(self.connector_ui.comboBox_connector.setCurrentIndex)
        self.connector_ui.comboBox_connector.activated.connect(self.ui.comboBox_connector.setCurrentIndex)
        self.connector_ui.comboBox_connector.activated[QString].connect(self.openConnectorDefinition)

        """connect_all_to_all"""
        self.connector_ui.cata_rb_weights.toggled.connect(self.slot_cata_weights)
        self.connector_ui.cata_rb_delays.toggled.connect(self.slot_cata_delays)
        """connect_dog"""
        self.connector_ui.cd_rb_delays.toggled.connect(self.slot_cd_delays)
        """connect_fixed_number_post"""
        self.connector_ui.cfn_post_rb_weights.toggled.connect(self.slot_cfnpost_weights)
        self.connector_ui.cfn_post_rb_delays.toggled.connect(self.slot_cfnpost_delays)
        """connect_fixed_number_pre"""
        self.connector_ui.cfn_pre_rb_weights.toggled.connect(self.slot_cfnpre_weights)
        self.connector_ui.cfn_pre_rb_delays.toggled.connect(self.slot_cfnpre_delays)
        """connect_fixed_probability"""
        self.connector_ui.cfp_rb_weights.toggled.connect(self.slot_cfp_weights)
        self.connector_ui.cfp_rb_delays.toggled.connect(self.slot_cfp_delays)
        """connect_from_file"""
        self.connector_ui.cff_openfile.clicked.connect(self.slot_cff_openfile)

        # todo
        """think about how to read data from matrix,and how to input the matrix? especially when i has a size of
        1000X1000 or even bigger
        """
        """connect_from_matrix"""
        self.connector_ui.page_cfm.setEnabled(False)
        """connect_from_sparse"""
        self.connector_ui.page_cfs.setEnabled(False)
        """connect_with_func"""
        self.connector_ui.page_cwf.setEnabled(False)

        """connect_gaussian"""
        self.connector_ui.cg_rb_delays.toggled.connect(self.slot_cg_delays)
        """connect_one_to_one"""
        self.connector_ui.coto_rb_weights.toggled.connect(self.slot_coto_weights)
        self.connector_ui.coto_rb_delays.toggled.connect(self.slot_coto_delays)

    def slot_coto_weights(self, isToggled):
        self.connector_ui.coto_weights.setEnabled(isToggled)
        self.connector_ui.coto_weights_max.setEnabled(not isToggled)
        self.connector_ui.coto_weights_min.setEnabled(not isToggled)

    def slot_coto_delays(self, isToggled):
        self.connector_ui.coto_delays.setEnabled(isToggled)
        self.connector_ui.coto_delays_max.setEnabled(not isToggled)
        self.connector_ui.coto_delays_min.setEnabled(not isToggled)

    def slot_cg_delays(self, isToggled):
        self.connector_ui.cg_delays.setEnabled(isToggled)
        self.connector_ui.cg_delays_max.setEnabled(not isToggled)
        self.connector_ui.cg_delays_min.setEnabled(not isToggled)

    def slot_cfp_weights(self, isToggled):
        self.connector_ui.cfp_weights.setEnabled(isToggled)
        self.connector_ui.cfp_weights_max.setEnabled(not isToggled)
        self.connector_ui.cfp_weights_min.setEnabled(not isToggled)

    def slot_cfp_delays(self, isToggled):
        self.connector_ui.cfp_delays.setEnabled(isToggled)
        self.connector_ui.cfp_delays_max.setEnabled(not isToggled)
        self.connector_ui.cfp_delays_min.setEnabled(not isToggled)

    def slot_cfnpre_weights(self, isToggled):
        self.connector_ui.cfn_pre_weights.setEnabled(isToggled)
        self.connector_ui.cfn_pre_weights_max.setEnabled(not isToggled)
        self.connector_ui.cfn_pre_weights_min.setEnabled(not isToggled)

    def slot_cfnpre_delays(self, isToggled):
        self.connector_ui.cfn_pre_delays.setEnabled(isToggled)
        self.connector_ui.cfn_pre_delays_max.setEnabled(not isToggled)
        self.connector_ui.cfn_pre_delays_min.setEnabled(not isToggled)

    def slot_cfnpost_delays(self, isToggled):
        self.connector_ui.cfn_post_delays.setEnabled(isToggled)
        self.connector_ui.cfn_post_delays_max.setEnabled(not isToggled)
        self.connector_ui.cfn_post_delays_min.setEnabled(not isToggled)

    def slot_cfnpost_weights(self, isToggled):
        self.connector_ui.cfn_post_weights.setEnabled(isToggled)
        self.connector_ui.cfn_post_weights_max.setEnabled(not isToggled)
        self.connector_ui.cfn_post_weights_min.setEnabled(not isToggled)

    def slot_cd_delays(self, isToggled):
        self.connector_ui.cd_delays.setEnabled(isToggled)
        self.connector_ui.cd_delays_max.setEnabled(not isToggled)
        self.connector_ui.cd_delays_min.setEnabled(not isToggled)

    def slot_cata_weights(self, isToggled):
        self.connector_ui.cata_weights.setEnabled(isToggled)
        self.connector_ui.cata_weights_min.setEnabled(not isToggled)
        self.connector_ui.cata_weights_max.setEnabled(not isToggled)

    def slot_cata_delays(self, isToggled):
        self.connector_ui.cata_delays.setEnabled(isToggled)
        self.connector_ui.cata_delays_min.setEnabled(not isToggled)
        self.connector_ui.cata_delays_max.setEnabled(not isToggled)

    def slot_cff_openfile(self):
        self.filename = QFileDialog().getOpenFileName(self, "open connector Data", QDir().currentPath(), "*.data;;*.*")
        myDir = QDir(self.filename)
        self.connector_ui.cff_filename.setText(myDir.dirName())
        self.connector_ui.cff_filepath.setPlainText(myDir.absolutePath())

    def setCurrentSynapse(self, currentSynapse=None):
        if isinstance(currentSynapse, dict):
            self.currentSynapse.update(currentSynapse)

    def setCurrentData(self, currentData=None):
        """
        synchronize currentData

        self.currentData = {
            "name"     : "",
            "pre"      : "",
            "post"     : "",
            "target"   : "",
            "synapse"  : "",
            "connector": ""
        }
        """
        if isinstance(currentData, dict):
            self.currentData.update(currentData)
        self.ui.lineEdit_name.setText(self.currentData.get("name"))
        self.ui.lineEdit_target.setText(self.currentData.get("target"))
        self.ui.comboBox_synapse_type.setCurrentIndex(
                self.ui.comboBox_synapse_type.findText(self.currentData.get("synapse")))
        self.ui.comboBox_connector.setCurrentIndex(
                self.ui.comboBox_connector.findText(self.currentData.get("connector"))
        )
        self.slot_updatePre(self.currentData.get("pre"))
        self.slot_updatePost(self.currentData.get("post"))

    def setCurrentConnector(self, currentConnector=None):
        """
        + update self.currentConnector
        + write all parametors into widget
        :param currentConnector:
        :type currentConnector:
        :return:
        :rtype:
        """
        if isinstance(currentConnector, dict):
            self.currentConnector.update(currentConnector)
        pageid = self.currentConnector.get("id")
        # connect_all_to_all
        if pageid == "page_cata":
            weights = self.currentConnector.get("weights")
            weights_max = self.currentConnector.get("weights_max")
            weights_min = self.currentConnector.get("weights_min")
            delays = self.currentConnector.get("delays")
            delays_max = self.currentConnector.get("delays_max")
            delays_min = self.currentConnector.get("delays_min")
            asc = self.currentConnector.get("asc")
            fmw = self.currentConnector.get("fmw")
            if type(weights) is float:
                self.connector_ui.cata_rb_weights.setChecked(True)
                self.connector_ui.cata_weights.setValue(weights if weights else 0)
            else:
                self.connector_ui.cata_rb_weights2.setChecked(True)
                self.connector_ui.cata_weights_max.setValue(weights_max if weights_max else 0)
                self.connector_ui.cata_weights_min.setValue(weights_min if weights_min else 0)
            if type(delays) is float:
                self.connector_ui.cata_rb_delays.setChecked(True)
                self.connector_ui.cata_delays.setValue(delays if delays else 0)
            else:
                self.connector_ui.cata_rb_delays2.setChecked(True)
                self.connector_ui.cata_delays_max.setValue(delays_max if delays_max else 0)
                self.connector_ui.cata_delays_min.setValue(delays_min if delays_min else 0)
            self.connector_ui.cata_asc.setChecked(asc)
            self.connector_ui.cata_fmw.setChecked(fmw)
        # connect_dog
        elif pageid == "page_cd":
            delays = self.currentConnector.get("delays")
            delays_max = self.currentConnector.get("delays_max")
            delays_min = self.currentConnector.get("delays_min")
            amp_pos = self.currentConnector.get("amp_pos")
            amp_neg = self.currentConnector.get("amp_neg")
            sigma_pos = self.currentConnector.get("sigma_pos")
            sigma_neg = self.currentConnector.get("sigma_neg")
            limit = self.currentConnector.get("limit")
            asc = self.currentConnector.get("asc")
            if type(delays) is float:
                self.connector_ui.cd_rb_delays.setChecked(True)
                self.connector_ui.cd_delays.setValue(delays)
            else:
                self.connector_ui.cd_rb_delays2.setChecked(True)
                self.connector_ui.cd_delays_max.setValue(delays_max)
                self.connector_ui.cd_delays_min.setValue(delays_min)
            self.connector_ui.cd_amp_pos.setValue(amp_pos)
            self.connector_ui.cd_amp_neg.setValue(amp_neg)
            self.connector_ui.cd_sigma_pos.setValue(sigma_pos)
            self.connector_ui.cd_sigma_neg.setValue(sigma_neg)
            self.connector_ui.cd_limit.setValue(limit)
            self.connector_ui.cd_asc.setChecked(asc)
        # connect_fixed_number_post
        elif pageid == "page_cfn_post":
            weights = self.currentConnector.get("weights")
            weights_max = self.currentConnector.get("weights_max")
            weights_min = self.currentConnector.get("weights_min")
            delays = self.currentConnector.get("delays")
            delays_max = self.currentConnector.get("delays_max")
            delays_min = self.currentConnector.get("delays_min")
            number = self.currentConnector.get("number")
            asc = self.currentConnector.get("asc")
            fmw = self.currentConnector.get("fmw")
            if type(weights) is float:
                self.connector_ui.cfn_post_rb_weights.setChecked(True)
                self.connector_ui.cfn_post_weights.setValue(weights)
            else:
                self.connector_ui.cfn_post_rb_weights2.setChecked(True)
                self.connector_ui.cfn_post_weights_max.setValue(weights_max)
                self.connector_ui.cfn_post_weights_min.setValue(weights_min)
            if type(delays) is float:
                self.connector_ui.cfn_post_rb_delays.setChecked(True)
                self.connector_ui.cfn_post_delays.setValue(delays)
            else:
                self.connector_ui.cfn_post_rb_delays2.setChecked(True)
                self.connector_ui.cfn_post_delays_max.setValue(delays_max)
                self.connector_ui.cfn_post_delays_min.setValue(delays_min)
            self.connector_ui.cfn_post_number.setValue(number)
            self.connector_ui.cfn_post_asc.setChecked(asc)
            self.connector_ui.cfn_post_fmw.setChecked(fmw)
        # connect_fixed_number_pre
        elif pageid == "page_cfn_pre":
            weights = self.currentConnector.get("weights")
            weights_max = self.currentConnector.get("weights_max")
            weights_min = self.currentConnector.get("weights_min")
            delays = self.currentConnector.get("delays")
            delays_max = self.currentConnector.get("delays_max")
            delays_min = self.currentConnector.get("delays_min")
            asc = self.currentConnector.get("asc")
            fmw = self.currentConnector.get("fmw")
            number = self.currentConnector.get("number")
            if type(weights) is float:
                self.connector_ui.cfn_pre_rb_weights.setChecked(True)
                self.connector_ui.cfn_pre_weights.setValue(weights)
            else:
                self.connector_ui.cfn_pre_rb_weights2.setChecked(True)
                self.connector_ui.cfn_pre_weights_max.setValue(weights_max)
                self.connector_ui.cfn_pre_weights_min.setValue(weights_min)
            if type(delays) is float:
                self.connector_ui.cfn_pre_rb_delays.setChecked(True)
                self.connector_ui.cfn_pre_delays.setValue(delays)
            else:
                self.connector_ui.cfn_pre_rb_delays2.setChecked(True)
                self.connector_ui.cfn_pre_delays_max.setValue(delays_max)
                self.connector_ui.cfn_pre_delays_min.setValue(delays_min)
            self.connector_ui.cfn_pre_number.setValue(number)
            self.connector_ui.cfn_pre_asc.setChecked(asc)
            self.connector_ui.cfn_pre_fmw.setChecked(fmw)
        # connect_fixed_probability
        elif pageid == "page_cfp":
            weights = self.currentConnector.get("weights")
            weights_max = self.currentConnector.get("weights_max")
            weights_min = self.currentConnector.get("weights_min")
            delays = self.currentConnector.get("delays")
            delays_max = self.currentConnector.get("delays_max")
            delays_min = self.currentConnector.get("delays_min")
            asc = self.currentConnector.get("asc")
            fmw = self.currentConnector.get("fmw")
            probability = self.currentConnector.get("probability")
            if type(weights) is float:
                self.connector_ui.cfp_rb_weights.setChecked(True)
                self.connector_ui.cfp_weights.setValue(weights)
            else:
                self.connector_ui.cfp_rb_weights2.setChecked(True)
                self.connector_ui.cfp_weights_max.setValue(weights_max)
                self.connector_ui.cfp_weights_min.setValue(weights_min)
            if type(delays) is float:
                self.connector_ui.cfp_rb_delays.setChecked(True)
                self.connector_ui.cfp_delays.setValue(delays)
            else:
                self.connector_ui.cfp_rb_delays2.setChecked(True)
                self.connector_ui.cfp_delays_max.setValue(delays_max)
                self.connector_ui.cfp_delays_min.setValue(delays_min)
            self.connector_ui.cfp_asc.setChecked(asc)
            self.connector_ui.cfp_fmw.setChecked(fmw)
            self.connector_ui.cfp_probability.setValue(probability)
        # connect_from_file
        elif pageid == "page_cff":
            filepath = self.currentConnector.get("filepath")
            filename = self.currentConnector.get("filename")
            self.connector_ui.cff_filepath.setPlainText(filepath)
            self.connector_ui.cff_filename.setText(filename)
        # connect_gaussian
        elif pageid == "page_cg":
            delays = self.currentConnector.get("delays")
            delays_max = self.currentConnector.get("delays_max")
            delays_min = self.currentConnector.get("delays_min")
            amp = self.currentConnector.get("amp")
            sigma = self.currentConnector.get("sigma")
            limit = self.currentConnector.get("limit")
            asc = self.currentConnector.get("asc")
            if type(delays) is float:
                self.connector_ui.cg_rb_delays.setChecked(True)
                self.connector_ui.cg_delays.setValue(delays)
            else:
                self.connector_ui.cg_rb_delays2.setChecked(True)
                self.connector_ui.cg_delays_max.setValue(delays_max)
                self.connector_ui.cg_delays_min.setValue(delays_min)
            self.connector_ui.cg_amp.setValue(amp)
            self.connector_ui.cg_sigma.setValue(sigma)
            self.connector_ui.cg_limit.setValue(limit)
            self.connector_ui.cg_asc.setChecked(asc)
        # connect_one_to_one
        elif pageid == "page_coto":
            weights = self.currentConnector.get("weights")
            weights_max = self.currentConnector.get("weights_max")
            weights_min = self.currentConnector.get("weights_min")
            delays = self.currentConnector.get("delays")
            delays_max = self.currentConnector.get("delays_max")
            delays_min = self.currentConnector.get("delays_min")
            shift = self.currentConnector.get("shift")
            fmw = self.currentConnector.get("fmw")
            if type(weights) is float:
                self.connector_ui.coto_rb_weights.setChecked(True)
                self.connector_ui.coto_weights.setValue(weights)
            else:
                self.connector_ui.coto_rb_weights2.setChecked(True)
                self.connector_ui.coto_weights_max.setValue(weights_max)
                self.connector_ui.coto_weights_min.setValue(weights_min)
            if type(delays) is float:
                self.connector_ui.coto_rb_delays.setChecked(True)
                self.connector_ui.coto_delays.setValue(delays)
            else:
                self.connector_ui.coto_rb_delays2.setChecked(True)
                self.connector_ui.coto_delays_max.setValue(delays_max)
                self.connector_ui.coto_delays_min.setValue(delays_min)
            self.connector_ui.coto_shift.setChecked(shift)
            self.connector_ui.coto_fmw.setChecked(fmw)
        # connect_from_matrix
        elif pageid == "page_cfm":
            pass
        # connect_from_sparse
        elif pageid == "page_cfs":
            pass
        # connect_with_func
        elif pageid == "page_cwf":
            pass

    def synchronizeConnector(self, connectorlist=None):
        """
        + synchronize connectorlist if necessary
        :param connectorlist:
        :type connectorlist:
        :return:
        :rtype:
        """
        if isinstance(connectorlist, list):
            del self.connectorlist
            self.connectorlist = connectorlist
        for item in self.connectorlist:
            if self.ui.comboBox_connector.findText(item) == -1:
                self.ui.comboBox_connector.addItem(item)
            if self.connector_ui.comboBox_connector.findText(item) == -1:
                self.connector_ui.comboBox_connector.addItem(item)

    # add new synapse to list if necessary
    def synchronizeDict(self, syn=None, sl=None):
        if isinstance(syn, dict) and isinstance(sl, list):
            self.synapsedict.update(syn)
            del self.synapselist
            self.synapselist = sl
            for key in self.synapselist:
                if self.ui.comboBox_synapse_type.findText(key) == -1:
                    self.ui.comboBox_synapse_type.insertItem(self.ui.comboBox_synapse_type.count(), key)

    def slot_rollback(self):
        self.ui.comboBox_synapse_type.setCurrentIndex(
                self.ui.comboBox_synapse_type.findText(self.currentData.get("synapse")))
        self.ui.comboBox_connector.setCurrentIndex(
                self.ui.comboBox_connector.findText(self.currentData.get("connector")))
        self.synapse_dialog.reject()

    # update informations
    def slot_updateName(self):
        self.currentData.update({"name": str(self.ui.lineEdit_name.text())})

    def slot_updateTarget(self):
        self.currentData.update({"target": str(self.ui.lineEdit_target.text())})

    def slot_updatePre(self, name):
        self.currentData.update({"pre": str(name)})
        self.ui.label_pre_Pop.setText(name)

    def slot_updatePost(self, name):
        self.currentData.update({"post": str(name)})
        self.ui.label_pos_Pop.setText(name)

    def slot_updateSynapse(self):
        synapse_name = self.synapse_ui.lineEdit_name.text()
        if not synapse_name.isEmpty():
            self.currentData.update({"synapse": str(self.synapse_ui.lineEdit_name.text())})
            tmp = {}
            tmp.update({"name": str(self.synapse_ui.lineEdit_name.text())})
            if synapse_name != "None":
                tmp.update({"description": str(self.synapse_ui.plainTextEdit_description.toPlainText())})
                tmp.update({"parameters": str(self.synapse_ui.plainTextEdit_parameter.toPlainText())})
                tmp.update({"equations": str(self.synapse_ui.plainTextEdit_equation.toPlainText())})
                tmp.update({"functions": str(self.synapse_ui.plainTextEdit_function.toPlainText())})
                tmp.update({"pre_spike": str(self.synapse_ui.plainTextEdit_pre_spike.toPlainText())})
                tmp.update({"post_spike": str(self.synapse_ui.plainTextEdit_pos_spike.toPlainText())})
                tmp.update({"psp": str(self.synapse_ui.plainTextEdit_psp.toPlainText())})

            self.setCurrentSynapse(tmp)
            self.synapsedict.update({str(synapse_name): self.currentSynapse})
            # update synapselist
            if self.synapselist.count(synapse_name) == 0:
                self.synapselist.append(synapse_name)
            # add a neu type of neuron
            self.synchronizeDict(self.synapsedict, self.synapselist)

            self.ui.comboBox_synapse_type.setCurrentIndex(self.ui.comboBox_synapse_type.findText(synapse_name))

        self.sig_synapse.emit(self.synapsedict, self.synapselist)
        self.synapse_dialog.accept()

    def slot_updateConnector(self):
        """
        + update self.currentData
        + update self.connectorlist
        + update self.currentConnector
        """
        connector = self.ui.comboBox_connector.currentText()
        self.currentData.update({"connector": str(connector)})
        if self.connectorlist.count(connector) == 0:
            self.connectorlist.append(connector)
        widget = self.connector_ui.stackedWidget.currentWidget()
        self.currentConnector.clear()
        self.currentConnector.update({"id": str(widget.objectName())})
        for child in widget.children():
            if not isinstance(child, QLayout) and not isinstance(child, QLabel) and child.isEnabled():
                if isinstance(child, QDoubleSpinBox) or isinstance(child, QSpinBox):
                    """delays"""
                    if child.objectName().endsWith("delays"):
                        self.currentConnector.update({"delays": child.value()})
                    if child.objectName().endsWith("delays_min"):
                        self.currentConnector.update({"delays_min": child.value()})
                    if child.objectName().endsWith("delays_max"):
                        self.currentConnector.update({"delays_max": child.value()})
                    """weights"""
                    if child.objectName().endsWith("weights"):
                        self.currentConnector.update({"weights": child.value()})
                    if child.objectName().endsWith("weights_min"):
                        self.currentConnector.update({"weights_min": child.value()})
                    if child.objectName().endsWith("weights_max"):
                        self.currentConnector.update({"weights_max": child.value()})
                    """amp"""
                    if child.objectName().endsWith("amp"):
                        self.currentConnector.update({"amp": child.value()})
                    """sigma"""
                    if child.objectName().endsWith("sigma"):
                        self.currentConnector.update({"sigma": child.value()})
                    """limit"""
                    if child.objectName().endsWith("limit"):
                        self.currentConnector.update({"limit": child.value()})
                    """probability"""
                    if child.objectName().endsWith("probability"):
                        self.currentConnector.update({"probability": child.value()})
                    """number"""
                    if child.objectName().endsWith("number"):
                        self.currentConnector.update({"number": child.value()})
                    """amp_pos"""
                    if child.objectName().endsWith("amp_pos"):
                        self.currentConnector.update({"amp_pos": child.value()})
                    """amp_neg"""
                    if child.objectName().endsWith("amp_neg"):
                        self.currentConnector.update({"amp_neg": child.value()})
                    """sigma_pos"""
                    if child.objectName().endsWith("sigma_pos"):
                        self.currentConnector.update({"sigma_pos": child.value()})
                    """sigma_neg"""
                    if child.objectName().endsWith("sigma_neg"):
                        self.currentConnector.update({"sigma_neg": child.value()})
                if isinstance(child, QCheckBox):
                    """shift"""
                    if child.objectName().endsWith("shift"):
                        self.currentConnector.update({"shift": child.isChecked()})
                    """force_multiple_weights"""
                    if child.objectName().endsWith("fmw"):
                        self.currentConnector.update({"fmw": child.isChecked()})
                    """allow_self_connections"""
                    if child.objectName().endsWith("asc"):
                        self.currentConnector.update({"asc": child.isChecked()})
                if isinstance(child, QLineEdit):
                    """filename"""
                    if child.objectName().endsWith("filename"):
                        self.currentConnector.update({"filename": str(child.text())})
                if isinstance(child, QPlainTextEdit):
                    """filepath"""
                    if child.objectName().endsWith("filepath"):
                        self.currentConnector.update({"filepath": str(child.toPlainText())})

        print self.currentConnector

    def openConnectorDefinition(self, name):
        """
        open the child widget in self.connector_ui.stackedWidget that has the same name of accessibleName()
        :param name:
        :type name:
        :return:
        :rtype:
        """
        self.connector_dialog.show()
        self.synchronizeConnector()
        self.connector_ui.comboBox_connector.setCurrentIndex(self.ui.comboBox_connector.findText(name))
        for index in range(self.connector_ui.stackedWidget.count()):
            if self.connector_ui.stackedWidget.widget(index).accessibleName() == name:
                self.connector_ui.stackedWidget.setCurrentIndex(index)
                return

    def openSynapseDefinition(self, s):
        # synchronized combobox_synapse first
        l = [self.ui.comboBox_synapse_type.itemText(index) for index in xrange(self.ui.comboBox_synapse_type.count())]
        for item in l:
            if self.synapse_ui.comboBox_synapse_type.findText(item) == -1:
                self.synapse_ui.comboBox_synapse_type.addItem(item)
        self.synapse_ui.comboBox_synapse_type.setCurrentIndex(self.synapse_ui.comboBox_synapse_type.findText(s))

        self.synapse_ui.tabWidget.setCurrentIndex(0)
        synapse = self.synapsedict.get(str(s))
        if synapse:
            parameters = synapse.get("parameters")
            equations = synapse.get("equations")
            psp = synapse.get("psp")
            pre_spike = synapse.get("pre_spike")
            post_spike = synapse.get("post_spike")
            functions = synapse.get("functions")
            description = synapse.get("description")
            name = synapse.get("name")
            self.synapse_ui.plainTextEdit_parameter.setPlainText(parameters if parameters else "")
            self.synapse_ui.plainTextEdit_equation.setPlainText(equations if equations else "")
            self.synapse_ui.plainTextEdit_psp.setPlainText(psp if psp else "")
            self.synapse_ui.plainTextEdit_pre_spike.setPlainText(pre_spike if pre_spike else "")
            self.synapse_ui.plainTextEdit_pos_spike.setPlainText(post_spike if post_spike else "")
            self.synapse_ui.plainTextEdit_function.setPlainText(functions if functions else "")
            self.synapse_ui.plainTextEdit_description.setPlainText(description if description else "")
            self.synapse_ui.lineEdit_name.setText(name if name else "")
            self.synapse_ui.lineEdit_name.setReadOnly(True)
        else:
            self.synapse_ui.plainTextEdit_parameter.clear()
            self.synapse_ui.plainTextEdit_equation.clear()
            self.synapse_ui.plainTextEdit_psp.clear()
            self.synapse_ui.plainTextEdit_pre_spike.clear()
            self.synapse_ui.plainTextEdit_pos_spike.clear()
            self.synapse_ui.plainTextEdit_function.clear()
            self.synapse_ui.plainTextEdit_description.clear()
            self.synapse_ui.lineEdit_name.clear()
            self.synapse_ui.lineEdit_name.setReadOnly(False)

        if s == "None":
            self.synapse_ui.plainTextEdit_parameter.setEnabled(False)
            self.synapse_ui.plainTextEdit_equation.setEnabled(False)
            self.synapse_ui.plainTextEdit_psp.setEnabled(False)
            self.synapse_ui.plainTextEdit_pre_spike.setEnabled(False)
            self.synapse_ui.plainTextEdit_pos_spike.setEnabled(False)
            self.synapse_ui.plainTextEdit_function.setEnabled(False)
            self.synapse_ui.plainTextEdit_description.setEnabled(False)
            self.synapse_ui.lineEdit_name.setEnabled(False)
        else:
            self.synapse_ui.plainTextEdit_parameter.setEnabled(True)
            self.synapse_ui.plainTextEdit_equation.setEnabled(True)
            self.synapse_ui.plainTextEdit_psp.setEnabled(True)
            self.synapse_ui.plainTextEdit_pre_spike.setEnabled(True)
            self.synapse_ui.plainTextEdit_pos_spike.setEnabled(True)
            self.synapse_ui.plainTextEdit_function.setEnabled(True)
            self.synapse_ui.plainTextEdit_description.setEnabled(True)
            self.synapse_ui.lineEdit_name.setEnabled(True)

        self.synapse_dialog.show()
