# widget in tab2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt4.QtGui import *


class OutputGraphic(QWidget):
    def __init__(self):
        super(OutputGraphic, self).__init__()
        vbox = QVBoxLayout(self)
        self.fig = plt.figure()
        self.fig.set_tight_layout(True)
        self.view = None

        self.plt1 = self.fig.add_subplot(311)
        self.plt2 = self.fig.add_subplot(312)
        self.plt3 = self.fig.add_subplot(313)

        self.canvas = FigureCanvasQTAgg(self.fig)
        toolbar = NavigationToolbar2QT(self.canvas, self)
        vbox.addWidget(self.canvas)
        vbox.addWidget(toolbar)

    # connect to another view, in order to get the data from items of another tab
    def connectTo(self, view):
        self.view = view

    def slot_DrawPlot(self):
        # data is a dictionary
        data = self.view.scene.item_data

        self.plt1.cla()
        self.plt2.cla()
        self.plt3.cla()

        self.plt1.text(0.2, 0.2, data.get("name"))

        self.plt2.text(0.2, 0.2, data.get("geometry"))

        self.plt3.text(0.2, 0.2, data.get("parameter"))

        self.canvas.draw()