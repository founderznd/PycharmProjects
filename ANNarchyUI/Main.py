# coding:utf-8
# main function


import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ConnectionView import ItemType
from ui import NeuronUI


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = NeuronUI.Ui_MainWindow()
        self.ui.setupUi(self)

        self.file = QFile()
        self.filename = QString()
        # saved data
        self.saved_data = {
            "Populations": [],
            "Projections": [],
            "neuronlist" : [],
            "synapselist": [],
            "neurondict" : {},
            "synapsedict": {}
        }

        self.scene = self.ui.gview_network.scene
        self.info_stack = self.scene.info_stack
        vbox = QVBoxLayout()
        self.ui.information.setLayout(vbox)
        vbox.addWidget(self.info_stack)

        """connect tab1 to tab2, in order to get the data from items of tab1"""
        # it better to use signal
        self.ui.tab_matplot.connectTo(self.ui.gview_network)

        self.ui.simulation_button.clicked.connect(self.slot_simulation)
        self.ui.gview_network.scene.sig_replot.connect(self.ui.tab_matplot.slot_DrawPlot)
        self.ui.gview_network.population_button.clicked[bool].connect(self.ui.gview_network.scene.setPrepared)
        self.ui.actionSave.triggered.connect(self.slot_actionSave)
        self.ui.actionOpen.triggered.connect(self.slot_actionLoad)

    def slot_actionSave(self):
        QDir().mkdir("save")
        self.filename = QFileDialog().getSaveFileName(self, "save file", QDir().currentPath() + "/save", "*.save;;*.*")
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

    def create_JSON_Object(self, data=None):
        """
        encode data to a json string and return it

        data = {
            "Populations": [(pos.x(),pos.y(),currentData = dict),...],
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
            if item.type == ItemType.POPULATION:
                pops.append((item.x(), item.y(), item.info.currentData))
            if item.type == ItemType.PROJECTION:
                line = item.line()
                projs.append(
                        (line.x1(), line.y1(), line.x2(), line.y2(), item.info.currentData, item.info.currentConnector))
        self.saved_data.update({"Populations": pops})
        self.saved_data.update({"Projections": projs})

        # convert list<QString> to list<string>
        self.saved_data.update({"neuronlist": [str(item) for item in self.scene.neuronlist]})
        self.saved_data.update({"synapselist": [str(item) for item in self.scene.synapselist]})

        self.saved_data.update({"neurondict": self.scene.neurondict})
        self.saved_data.update({"synapsedict": self.scene.synapsedict})

        _json_encoder = json.dumps(self.saved_data)
        return _json_encoder

    def slot_actionLoad(self):
        """
        load data from *.save file
        :return:
        :rtype:
        """
        self.filename = QFileDialog().getOpenFileName(self, "open file", QDir().currentPath()+"/save", "*.save;;*.*")
        if not self.filename:
            return
        self.file.setFileName(self.filename)
        if self.file.open(QIODevice.ReadOnly):
            print  self.file.fileName() + " has been opened"
            ids = QDataStream(self.file)
            self.saved_data = json.loads(ids.readString())

            self.scene.clear()
            # for item in self.scene.items():
            #     self.scene.removeItem(item)

            self.scene.neuronlist = [QString(item) for item in self.saved_data.get("neuronlist")]
            self.scene.synapselist = [QString(item) for item in self.saved_data.get("synapselist")]
            self.scene.neurondict.update(self.saved_data.get("neurondict"))
            self.scene.synapsedict.update(self.saved_data.get("synapsedict"))

            pops = self.saved_data.get("Populations")
            for item in pops:
                """
                item[0]:item.x()::float
                item[1]:item.y()::float
                item[2]:item.info.currentData::dict
                """
                info = self.scene.addPopulation(QPointF(item[0], item[1]))
                info.setCurrentData(item[2])
            projs = self.saved_data.get("Projections")
            for item in projs:
                """
                item[0]:source.x()
                item[1]:source.y()
                item[2]:dest.x()
                item[3]:dest.x()
                item[4]:item.info.currentData::dict
                item[5]:item.info.currentConnector::dict
                """
                source = self.scene.itemAt(QPointF(item[0], item[1]))
                dest = self.scene.itemAt(QPointF(item[2], item[3]))
                info = self.scene.addProjection(source, dest)
                info.setCurrentData(item[4])
                info.setCurrentConnector(item[5])
        self.file.close()

    # todo finish simulation
    def slot_simulation(self):
        self.ui.gview_network.scene.update()
        """simulation 1"""
        # self.ui.tab_matplot.slot_DrawPlot()

        # setup(dt=0.1)
        #
        # COBA = Neuron(
        #         parameters="""
        #         El = -60.0          : population
        #         Vr = -60.0          : population
        #         Erev_exc = 0.0      : population
        #         Erev_inh = -80.0    : population
        #         Vt = -50.0          : population
        #         tau = 20.0          : population
        #         tau_exc = 5.0       : population
        #         tau_inh = 10.0      : population
        #         I = 20.0            : population
        #     """,
        #         equations="""
        #         tau * dv/dt = (El - v) + g_exc * (Erev_exc - v) + g_inh * (Erev_inh - v ) + I
        #
        #         tau_exc * dg_exc/dt = - g_exc
        #         tau_inh * dg_inh/dt = - g_inh
        #     """,
        #         spike="v > Vt",
        #         reset="v = Vr",
        #         refractory=5.0
        # )
        #
        # CUBA = Neuron(
        #         parameters="""
        #         El = -49.0      : population
        #         Vr = -60.0      : population
        #         Vt = -50.0      : population
        #         tau_m = 20.0    : population
        #         tau_exc = 5.0   : population
        #         tau_inh = 10.0  : population
        #     """,
        #         equations="""
        #         tau_m * dv/dt = (El - v) + g_exc + g_inh
        #
        #         tau_exc * dg_exc/dt = - g_exc
        #         tau_inh * dg_inh/dt = - g_inh
        #     """,
        #         spike="v > Vt",
        #         reset="v = Vr",
        #         refractory=5.0
        # )
        #
        # P = Population(geometry=4000, neuron=COBA)
        # Pe = P[:3200]
        # Pi = P[3200:]
        #
        # P.v = Normal(-55.0, 5.0)
        # P.g_exc = Normal(4.0, 1.5)
        # P.g_inh = Normal(20.0, 12.0)
        #
        # Ce = Projection(pre=Pe, post=P, target='exc')
        # Ce.connect_fixed_probability(weights=0.6, probability=0.02)
        #
        # Ci = Projection(pre=Pi, post=P, target='inh')
        # Ci.connect_fixed_probability(weights=6.7, probability=0.02)
        #
        # compile()
        #
        # m = Monitor(P, ['spike'])
        #
        # simulate(1000.)
        #
        # data = m.get('spike')
        #
        # t, n = m.raster_plot(data)
        #
        # print('Mean firing rate in the population: ' + str(len(t) / 4000.) + 'Hz')
        #
        # plt = self.ui.tab_matplot.plt
        # plt.plot(t, n, '.', markersize=0.5)
        # plt.set_xlabel('Time (ms)')
        # plt.set_ylabel('# neuron')

        """simulation 2"""
        # IF = Neuron(
        #         parameters="""
        #         tau_m = 10.0
        #         tau_e = 5.0
        #         vt = -54.0
        #         vr = -60.0
        #         El = -74.0
        #         Ee = 0.0
        #     """,
        #         equations="""
        #         tau_m * dv/dt = El - v + g_exc * (Ee - vr) : init = -60.0
        #         tau_e * dg_exc/dt = -g_exc
        #     """,
        #         spike="""
        #         v > vt
        #     """,
        #         reset="""
        #         v = vr
        #     """
        # )
        #
        # F = 15.0
        # N = 1000
        # Input = PoissonPopulation(name='Input', geometry=N, rates=F)
        # Output = Population(name='Output', geometry=1, neuron=IF)
        #
        # proj = Projection(
        #         pre=Input,
        #         post=Output,
        #         target='exc',
        #         synapse=STDP(tau_plus=20.0, tau_minus=20.0, A_plus=0.01, A_minus=0.0105, w_max=0.01)
        # )
        #
        # proj.connect_all_to_all(weights=Uniform(0.0, 0.01))
        # # connector = self.info_stack.currentWidget().ui.comboBox_connectivity.currentText()
        # # connector = self.ui.gview_network.scene.currentItem.info.ui.comboBox_connectivity.currentText()
        #
        # compile()
        #
        # Mi = Monitor(Input, 'spike')
        # Mo = Monitor(Output, 'spike')
        #
        # simulate(100000, measure_time=True)
        #
        # input_spikes = Mi.get('spike')
        # output_spikes = Mo.get('spike')
        #
        # output_rate = Mo.smoothed_rate(output_spikes, 100.0)
        #
        # weights = proj.w[0]
        #
        # self.ui.tab_matplot.plt1.plot(output_rate[0, :])
        # self.ui.tab_matplot.plt2.plot(weights, '.')
        # self.ui.tab_matplot.plt3.hist(weights, bins=20)
        # print self.ui.gview_network.scene.neuronlist
        # print self.ui.gview_network.scene.synapselist
        # print self.ui.gview_network.scene.neuronsdict


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
