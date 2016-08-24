# coding:utf-8
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT
from pylab import *

import ANNarchy
from PyQt4.QtGui import *


class MyNeurons(list):
    def __init__(self):
        super(MyNeurons, self).__init__()

    def addNeuron(self, obj=ANNarchy.Neuron):
        self.append(obj)

    def getNeuron(self, name=str):
        for item in self:
            if isinstance(item, ANNarchy.Neuron):
                if item.name == name:
                    return item


class MySynapses(list):
    def __init__(self):
        super(MySynapses, self).__init__()

    def addSynapse(self, obj=ANNarchy.Synapse):
        self.append(obj)


class MyPopulations(list):
    def __init__(self):
        super(MyPopulations, self).__init__()

    def addPopulation(self, obj=ANNarchy.Population):
        self.append(obj)

    def getPopulation(self, name):
        for pop in self:
            if isinstance(pop, ANNarchy.Population):
                if pop.name == name:
                    return pop
        return None


class MyProjections(list):
    def __init__(self):
        super(MyProjections, self).__init__()

    def addProjection(self, obj=ANNarchy.Projection):
        self.append(obj)


class MyMonitors(list):
    def __init__(self):
        super(MyMonitors, self).__init__()

    def addMonitor(self, obj=ANNarchy.Monitor):
        self.append(obj)


class MyMonitor(QWidget):
    def __init__(self, *args):
        super(MyMonitor, self).__init__(*args)
        vbox = QVBoxLayout(self)
        # free the memory
        plt.close()

        self.fig = plt.figure()
        self.fig.set_tight_layout(True)
        self.canvas = FigureCanvasQTAgg(self.fig)
        toolbar = NavigationToolbar2QT(self.canvas, self)
        vbox.addWidget(self.canvas)
        vbox.addWidget(toolbar)

        self.populations = None
        self.projections = None

        self.Mi = None
        self.Mo = None

    # def slot_create_monitor(self, pops=MyPopulations, projs=MyProjections):
    #     self.populations = pops
    #     self.projections = projs
    #     self.Mi = ANNarchy.Monitor(self.populations.getPopulation("Input"), 'spike')
    #     self.Mo = ANNarchy.Monitor(self.populations.getPopulation("Output"), 'spike')
    #     print "monitor object done!", self.Mi, self.Mo

    def make_annarchy_objects(self, *args):
        self.populations = args[0]
        self.projections = args[1]
        self.Mi = args[2]
        self.Mo = args[3]

    def drawPlot(self):
        self.fig.clear()
        # self.monitor.update(monitor)
        # if self.monitor.get("enabled") is not True:
        #     self.monitor.clear()
        #     self.parentWidget().parentWidget().close()
        # """
        #      self.plt1.cla()
        #      self.plt2.cla()
        #      self.plt3.cla()
        # """
        # # here use monitor
        # Mo = ANNarchy.Monitor(self._population, 'spike')
        # output_spikes = Mo.get('spike')
        # output_rate = Mo.smoothed_rate(output_spikes, 100.0)
        # # weights = self._projections[0].w[0]
        # weights = 0
        #
        # plot1 = self.fig.add_subplot(311)
        # plot1.plot(output_rate[0, :])
        # plot2 = self.fig.add_subplot(312)
        # plot2.plot(weights, '.')
        # plot3 = self.fig.add_subplot(313)
        # plot3.hist(weights, bins=20)

        # plot = self.fig.add_subplot(111)
        # plot.text(0, 0.5, str(self.monitor))
        # self.canvas.draw()

        input_spikes = self.Mi.get('spike')
        output_spikes = self.Mo.get('spike')

        output_rate = self.Mo.smoothed_rate(output_spikes, 100.0)

        weights = self.projections[0].w[0]

        plot1 = self.fig.add_subplot(311)
        plot1.plot(output_rate[0, :])
        plot2 = self.fig.add_subplot(312)
        plot2.plot(weights, '.')
        plot3 = self.fig.add_subplot(313)
        plot3.hist(weights, bins=20)
        self.canvas.draw()
