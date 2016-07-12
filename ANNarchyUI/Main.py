# coding:utf-8
# main function


from ANNarchy import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui import NeuronUI


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = NeuronUI.Ui_MainWindow()
        self.ui.setupUi(self)

        self.info_stack = self.ui.gview_network.scene.info_stack
        vbox = QVBoxLayout()
        self.ui.information.setLayout(vbox)
        vbox.addWidget(self.info_stack)

        # connect tab1 to tab2, in order to get the data from items of tab1
        self.ui.tab_matplot.connectTo(self.ui.gview_network)

        self.connect(self.ui.simulation_button, SIGNAL("clicked()"), self.slot_simulation)
        self.connect(self.ui.gview_network.scene, SIGNAL("replot()"), self.ui.tab_matplot.slot_DrawPlot)
        self.connect(self.ui.gview_network.population_button, SIGNAL("clicked(bool)"), self.slot_addNeuron)

    def slot_addNeuron(self, isChecked):
        self.ui.gview_network.scene.isPrepared = isChecked

    # todo finish simulation
    def slot_simulation(self):
        self.ui.gview_network.scene.update()
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

        IF = Neuron(
                parameters="""
                tau_m = 10.0
                tau_e = 5.0
                vt = -54.0
                vr = -60.0
                El = -74.0
                Ee = 0.0
            """,
                equations="""
                tau_m * dv/dt = El - v + g_exc * (Ee - vr) : init = -60.0
                tau_e * dg_exc/dt = -g_exc
            """,
                spike="""
                v > vt
            """,
                reset="""
                v = vr
            """
        )

        F = 15.0
        N = 1000
        Input = PoissonPopulation(name='Input', geometry=N, rates=F)
        Output = Population(name='Output', geometry=1, neuron=IF)

        proj = Projection(
                pre=Input,
                post=Output,
                target='exc',
                synapse=STDP(tau_plus=20.0, tau_minus=20.0, A_plus=0.01, A_minus=0.0105, w_max=0.01)
        )

        proj.connect_all_to_all(weights=Uniform(0.0, 0.01))
        # connector = self.info_stack.currentWidget().ui.comboBox_connectivity.currentText()
        # connector = self.ui.gview_network.scene.currentItem.info.ui.comboBox_connectivity.currentText()
        # print connector

        compile()

        Mi = Monitor(Input, 'spike')
        Mo = Monitor(Output, 'spike')

        simulate(100000, measure_time=True)

        input_spikes = Mi.get('spike')
        output_spikes = Mo.get('spike')

        output_rate = Mo.smoothed_rate(output_spikes, 100.0)

        weights = proj.w[0]

        self.ui.tab_matplot.plt1.plot(output_rate[0, :])
        self.ui.tab_matplot.plt2.plot(weights, '.')
        self.ui.tab_matplot.plt3.hist(weights, bins=20)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
