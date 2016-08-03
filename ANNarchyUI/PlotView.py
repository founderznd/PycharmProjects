# coding:utf-8
# widget in tab2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt4.QtGui import *


class OutputGraphic(QWidget):
    def __init__(self, *args):
        super(OutputGraphic, self).__init__(*args)
        vbox = QVBoxLayout(self)
        # free the memory
        plt.close()

        self.fig = plt.figure()
        self.fig.set_tight_layout(True)
        self.monitor = dict()

        self.canvas = FigureCanvasQTAgg(self.fig)
        toolbar = NavigationToolbar2QT(self.canvas, self)
        vbox.addWidget(self.canvas)
        vbox.addWidget(toolbar)

    def drawPlot(self, monitor=dict):

        self.fig.clear()
        self.monitor.update(monitor)
        if self.monitor.get("enabled") is not True:
            self.monitor.clear()
            self.parentWidget().parentWidget().close()
        """
             self.plt1.cla()
             self.plt2.cla()
             self.plt3.cla()
        """
        plot = self.fig.add_subplot(111)
        plot.text(0, 0.5, str(self.monitor))
        self.canvas.draw()
