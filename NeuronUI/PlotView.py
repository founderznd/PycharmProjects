# widget in tab2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt4.QtGui import *


class OutputGraphic(QWidget):
    def __init__(self):
        super(OutputGraphic, self).__init__()
        vbox = QVBoxLayout(self)
        self.fig = plt.figure()
        self.view = None

        self.plt1 = self.fig.add_subplot(211)
        self.plt2 = self.fig.add_subplot(212)

        self.canvas = FigureCanvasQTAgg(self.fig)
        toolbar = NavigationToolbar2QT(self.canvas, self)
        vbox.addWidget(self.canvas)
        vbox.addWidget(toolbar)

    # connect to another view, in order to get the data from items of another tab
    def connectTo(self, view):
        self.view = view

    def slot_DrawPlot(self):
        data = self.view.getItemData()

        self.plt1.cla()
        self.plt2.cla()

        self.plt1.text(0.2, 0.2, data.get("neuron_par"))

        self.plt2.text(0.2, 0.2, data.get("neuron_eq"))

        self.canvas.draw()
