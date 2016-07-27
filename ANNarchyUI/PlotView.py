# widget in tab2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt4.QtGui import *


class OutputGraphic(QWidget):
    def __init__(self, *args):
        super(OutputGraphic, self).__init__(*args)
        vbox = QVBoxLayout(self)
        self.fig = plt.figure()
        self.fig.set_tight_layout(True)
        self.monitor = dict()

        # self.plt1 = self.fig.add_subplot(311)
        # self.plt2 = self.fig.add_subplot(312)
        # self.plt3 = self.fig.add_subplot(313)
        self.plt = self.fig.add_subplot(111)

        self.canvas = FigureCanvasQTAgg(self.fig)
        toolbar = NavigationToolbar2QT(self.canvas, self)
        vbox.addWidget(self.canvas)
        vbox.addWidget(toolbar)

    def slot_draw_plot(self, monitor=dict):
        self.monitor.update(monitor)
        if self.monitor.get("enabled") is not True:
            self.monitor.clear()
            self.parentWidget().parentWidget().close()
        """
             self.plt1.cla()
             self.plt2.cla()
             self.plt3.cla()
        """
        self.plt.cla()
        # self.plt.text(str(self.monitor))
        self.plt.text(0, 0.5, str(self.monitor))
        self.canvas.draw()
