# coding:utf-8
# main function
import ast
import json
from pylab import *

import ANNarchy
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ANNarchyData
import ConnectionView
from ui import NeuronUI, Simulation_Definition


class MainWindow(QMainWindow):
    sig_populations = pyqtSignal(ANNarchyData.MyPopulations, ANNarchyData.MyProjections)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = NeuronUI.Ui_MainWindow()
        self.ui.setupUi(self)

        self.file = QFile()
        self.filename = QString()
        self.isSimulated = False

        # annarchy object
        self.neurons = ANNarchyData.MyNeurons()
        self.synapses = ANNarchyData.MySynapses()
        self.populations = ANNarchyData.MyPopulations()
        self.projections = ANNarchyData.MyProjections()

        # saved data
        self.saved_data = {
            "Populations": [],
            "Projections": [],
            "neurondict" : {},
            "synapsedict": {}
        }

        self.scene = self.ui.gview_network.scene
        self.info_stack = self.scene.info_stack
        self.ui.vbox_information.addWidget(self.info_stack)

        self.simulation_dialog = QDialog()
        self.simulation_ui = Simulation_Definition.Ui_Dialog()
        self.simulation_ui.setupUi(self.simulation_dialog)

        self.error_input = QString()

        """signal and slot"""
        self.ui.simulation_button.clicked.connect(self.slot_simulation)
        self.ui.actionNew.triggered.connect(self.slot_actionNew)
        self.ui.actionOpen.triggered.connect(self.slot_actionLoad)
        self.ui.actionSave.triggered.connect(self.slot_actionSave)
        self.ui.actionSave_as.triggered.connect(self.slot_actionSave_as)

    def slot_actionNew(self):
        """
        create a new network
        :return:
        :rtype:
        """
        """
        QMessageBox.question(
            QWidget,
            QString,
            QString,
            QMessageBox.StandardButtons buttons=QMessageBox.Ok,
            QMessageBox.StandardButton defaultButton=QMessageBox.NoButton
        ) -> QMessageBox.StandardButton
        """
        button = QMessageBox().question(
                self,
                "Warning!",
                "Do you want to save this file before create a new one?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
        )
        if button == QMessageBox.Cancel:
            return
        if button == QMessageBox.Yes:
            self.slot_actionSave_as()
        self.filename = ""
        self.scene.clear()

    def slot_actionSave(self):
        """
        save data
        :return:
        :rtype:
        """
        if self.filename == "":
            QDir().mkdir("save")
            """
            QFileDialog.getSaveFileName(
                QWidget parent=None,
                QString caption=QString(),
                QString directory=QString(),
                QString filter=QString(),
                QString selectedFilter=None,
                QFileDialog.Options options=0
            ) -> QString
            """
            self.filename = QFileDialog().getSaveFileName(
                    self,
                    "save file",
                    QDir().currentPath() + "/save",
                    "*.save;;*.*"
            )
            if not self.filename:
                return
            if not self.filename.endsWith(".save"):
                self.file.setFileName(self.filename.append(".save"))
            else:
                self.file.setFileName(self.filename)

        if self.file.open(QIODevice.WriteOnly | QIODevice.Truncate):
            ods = QDataStream(self.file)
            js = self.create_JSON_Object()
            ods.writeString(js)
            print  self.filename + " has been saved"
        self.file.close()

    def slot_actionSave_as(self):
        self.filename = ""
        self.slot_actionSave()

    def create_JSON_Object(self, data=None):
        """
        encode data to a json string and return it

        data = {
            "Populations": [(pos.x(),pos.y(),currentData = dict,currentMonitor = dict),...],
            "Projections": [(source.x(),source.y(),dest.x(),dest.y(),currentData = dict,currentConnector = dict),...],
            "neuronlist" : [self.scene.neuronlist],
            "synapselist": [self.scene.synapselist],
            "neurondict" : {self.scene.neurondict},
            "synapsedict": {self.scene.synapsedict}
        }
        :param data:
        :type data:
        :return: _json_encoder
        :rtype: string
        """
        if isinstance(data, dict):
            self.saved_data.update(data)
        pops = list()
        projs = list()
        for item in self.scene.items():
            if isinstance(item, ConnectionView.Population):
                pops.append((item.x(), item.y(), item.info.currentData, item.info.currentMonitor))
            if isinstance(item, ConnectionView.Projection):
                projs.append(
                        (
                            item.sourcePoint.x(), item.sourcePoint.y(),
                            item.destPoint.x(), item.destPoint.y(),
                            item.info.currentData, item.info.currentConnector
                        )
                )
        self.saved_data.update({"Populations": pops})
        self.saved_data.update({"Projections": projs})

        self.saved_data.update({"neurondict": self.scene.data.neurons})
        self.saved_data.update({"synapsedict": self.scene.data.synapses})

        _json_encoder = json.dumps(self.saved_data)
        return _json_encoder

    def slot_actionLoad(self):
        """
        load data from *.save file
        :return:
        :rtype:
        """
        """
        QFileDialog.getOpenFileName(
            QWidget parent=None,
            QString caption=QString(),
            QString directory=QString(),
            QString filter=QString(),
            QString selectedFilter=None,
            QFileDialog.Options options=0
        ) -> QString
        """
        self.filename = QFileDialog().getOpenFileName(self, "open file", QDir().currentPath() + "/save", "*.save;;*.*")
        if not self.filename:
            print "file is not opened"
            return
        self.file.setFileName(self.filename)
        if self.file.open(QIODevice.ReadOnly):
            print  self.file.fileName() + " has been opened"

            try:
                ids = QDataStream(self.file)
                self.saved_data = json.loads(ids.readString())
            except IOError:
                print IOError.message

            self.scene.clear()

            self.scene.data.neurons.update(self.saved_data.get("neurondict"))
            self.scene.data.synapses.update(self.saved_data.get("synapsedict"))

            try:
                pops = self.saved_data.get("Populations")
                for item in pops:
                    """
                    float   item[0]:item.x()
                    float   item[1]:item.y()
                    dict    item[2]:item.info.currentData
                    dict    item[3]:item.info.currentMonitor
                    """
                    info = self.scene.addPopulation(QPointF(item[0], item[1]))
                    info.setCurrentData(item[2])
                    info.setCurrentMonitor(item[3])
                    info.setCurrentNeuron(self.scene.data.neurons.get(info.currentData.get("neuron")))

            except IndexError:
                print IndexError, " in Populations"

            try:
                projs = self.saved_data.get("Projections")
                for item in projs:
                    """
                    float   item[0]:source.x()
                    float   item[1]:source.y()
                    float   item[2]:dest.x()
                    float   item[3]:dest.y()
                    dict    item[4]:item.info.currentData
                    dict    item[5]:item.info.currentConnector
                    """
                    source = self.scene.itemAt(QPointF(item[0], item[1]))
                    dest = self.scene.itemAt(QPointF(item[2], item[3]))
                    info = self.scene.addProjection(source, dest)
                    info.setCurrentData(item[4])
                    info.setCurrentConnector(item[5])
                    info.setCurrentSynapse(self.scene.data.synapses.get(info.currentData.get("synapse")))
            except IndexError:
                print IndexError, " in Projections"

            self.file.close()

    # todo finish simulation
    def slot_simulation(self):
        """simulation:
        + 1 check all inputs
        + 2 define neuron
        + 3 create population regard to defined neuron
        + 4 turn to step 2 until all populations are created
        + 5 define synapse
        + 6 create projection between populations regard to defined synapse
        + 7 set connector of each projection
        + 8 turn to step 5 until all projections are created
        + 9 compile()
        + 10 monitor
        + 11 simulate
        + 12 plot()
        :return:
        :rtype:
        """
        if self.isSimulated:
            print "already simulated"
            return

        """check all inputs"""
        if not self.checkAllSignals():
            QMessageBox().information(self, "information", "please check your input:\n" + self.error_input)
            return

        for item in self.scene.items():
            """create poisson population and its neuron"""
            if isinstance(item, ConnectionView.Population):
                if item.info.currentData.get("neuron") == "PoissonNeuron":
                    # convert QString to Tuple
                    geo_tuple = ast.literal_eval(item.info.currentData.get("geometry"))
                    pop = ANNarchy.PoissonPopulation(
                            geo_tuple,
                            item.info.currentData.get("name"),
                            item.info.currentData.get("rates"),
                            item.info.currentData.get("target"),
                            item.info.currentData.get("parameters"),
                            item.info.currentData.get("refractory")
                    )
                    self.populations.addPopulation(pop)
                else:
                    """
                      *Parameters*:
                          * **parameters**: parameters of the neuron and their initial value.
                          * **equations**: equations defining the temporal evolution of variables.
                          * **spike**: condition to emit a spike (only for spiking neurons).
                          * **reset**: changes to the variables after a spike (only for spiking neurons).
                          * **refractory**: refractory period of a neuron after a spike (only for spiking neurons).
                          * **functions**: additional functions used in the variables' equations.
                          * **name**: name of the neuron type (used for reporting only).
                          * **description**: short description of the neuron type (used for reporting).
                      """
                    neuron = ANNarchy.Neuron(
                            item.info.currentNeuron.get("parameters"),
                            item.info.currentNeuron.get("equations"),
                            item.info.currentNeuron.get("spike"),
                            item.info.currentNeuron.get("reset"),
                            item.info.currentNeuron.get("refractory"),
                            item.info.currentNeuron.get("functions"),
                            item.info.currentNeuron.get("name"),
                            item.info.currentNeuron.get("description"),
                    )
                    self.neurons.addNeuron(neuron)

                    pop = ANNarchy.Population(
                            ast.literal_eval(item.info.currentData.get("geometry")),
                            neuron,
                            item.info.currentData.get("name"),
                            None
                    )
                    self.populations.addPopulation(pop)

        for item in self.scene.items():
            """create projection and its synapse"""
            if isinstance(item, ConnectionView.Projection):
                """
                *Parameters*:
                    * **parameters**: parameters of the neuron and their initial value.
                    * **equations**: equations defining the temporal evolution of variables.
                    * **psp**: influence of a single synapse on the post-synaptic neuron (default for rate-coded:
                    w*pre.r).
                    * **operation**: operation (sum, max, min, mean) performed by the post-synaptic neuron on the
                    individual psp (rate-coded only, default=sum).
                    * **pre_spike**: updating of variables when a pre-synaptic spike is received (spiking only).
                    * **post_spike**: updating of variables when a post-synaptic spike is emitted (spiking only).
                    * **functions**: additional functions used in the equations.
                    * **name**: name of the synapse type (used for reporting only).
                    * **description**: short description of the synapse type (used for reporting).
                """
                synapse = ANNarchy.Synapse(
                        parameters=item.info.currentSynapse.get("parameters"),
                        equations=item.info.currentSynapse.get("equations"),
                        psp=item.info.currentSynapse.get("psp"),
                        operation="sum",
                        pre_spike=item.info.currentSynapse.get("pre_spike"),
                        post_spike=item.info.currentSynapse.get("post_spike"),
                        functions=item.info.currentSynapse.get("functions"),
                        pruning=None,
                        creating=None,
                        name=item.info.currentSynapse.get("name"),
                        description=item.info.currentSynapse.get("description"),
                        extra_values={}
                )
                # synapse = ANNarchy.STDP(tau_plus=20.0, tau_minus=20.0, A_plus=0.01, A_minus=0.0105, w_max=0.01)
                # synapse = ANNarchy.STDP()
                self.synapses.addSynapse(synapse)
                """
                *Parameters*:
                    * **pre**: pre-synaptic population (either its name or a ``Population`` object).
                    * **post**: post-synaptic population (either its name or a ``Population`` object).
                    * **target**: type of the connection.
                    * **synapse**: a ``Synapse`` instance.
                    * **name**: unique name of the projection (optional).

                    By default, the synapse only ensures linear synaptic transmission:

                    * For rate-coded populations: ``psp = w * pre.r``
                    * For spiking populations: ``g_target += w``
                """
                print "proj name: ", item.info.currentData.get("name")
                proj = ANNarchy.Projection(
                        pre=item.info.currentData.get("pre"),
                        post=item.info.currentData.get("post"),
                        target=item.info.currentData.get("target"),
                        synapse=synapse,
                        name=item.info.currentData.get("name")
                )
                self.projections.addProjection(proj)
                """set connector"""
                connector = item.info.currentConnector
                if connector.get("id") == "page_cata":
                    weights = connector.get("weights")
                    weights_max = connector.get("weights_max")
                    weights_min = connector.get("weights_min")
                    delays = connector.get("delays")
                    delays_max = connector.get("delays_max")
                    delays_min = connector.get("delays_min")
                    asc = connector.get("asc")
                    fmw = connector.get("fmw")
                    if type(weights) is not float:
                        weights = ANNarchy.Uniform(weights_min, weights_max)
                    if type(delays) is not float:
                        delays = ANNarchy.Uniform(delays_min, delays_max)
                    proj.connect_all_to_all(weights)

        ANNarchy.core.Global.config['verbose'] = True
        # compile
        ANNarchy.compile(debug_build=True)

        # Mi = ANNarchy.Monitor(self.populations.getPopulation("Input"), 'spike')
        # Mo = ANNarchy.Monitor(self.populations.getPopulation("Output"), 'spike')

        self.sig_populations.emit(self.populations, self.projections)

        """just for test"""
        for item in self.scene.items():
            if isinstance(item, ConnectionView.Population):
                item.info.slot_create_monitor(self.populations, self.projections)

        # self.simulation_dialog.show()
        ANNarchy.simulate(10000, measure_time=True)

        self.isSimulated = True

    def checkAllSignals(self):
        isAllRight = True
        self.error_input.clear()
        for item in self.scene.items():
            """population"""
            if isinstance(item, ConnectionView.Population):
                """name"""
                data = item.info.currentData.get("name")
                if data == "":
                    # print  "Population: ", item.info.currentData.get("name"), " has no name"
                    self.error_input.append("Population: " + item.info.currentData.get("name") + " has no name\n")
                    isAllRight = False
                """geometry"""
                data = item.info.currentData.get("geometry")
                if data == "":
                    # print  "Population: ", item.info.currentData.get("name"), " has no geometry"
                    self.error_input.append("Population: " + item.info.currentData.get("name") + " has no geometry\n")
                    isAllRight = False
                """currentMonitor"""
                if item.info.currentMonitor.get("enabled"):
                    data = item.info.currentMonitor.get("variables")
                    if data == "":
                        # print  "Population: ", item.info.currentData.get("name"), " has no variables"
                        self.error_input.append(
                                "Population: " + item.info.currentData.get("name") + " has no variables\n")
                        isAllRight = False
            """projection"""
            if isinstance(item, ConnectionView.Projection):
                """name"""
                data = item.info.currentData.get("name")
                if data == "":
                    # print  "Projection: ", item.info.currentData.get("name"), " has no name"
                    self.error_input.append("Projection: " + item.info.currentData.get("name") + " has no name\n")
                    isAllRight = False
                """target"""
                data = item.info.currentData.get("target")
                if data == "":
                    # print  "Projection: ", item.info.currentData.get("name"), " has no target"
                    self.error_input.append("Projection: " + item.info.currentData.get("name") + " has no target\n")
                    isAllRight = False
        return isAllRight


if __name__ == '__main__':
    import sys, gc

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    sys.exit(gc.collect())
