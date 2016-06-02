# widget in tab2
import numpy
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.pyplot import *

from PyQt4.QtGui import *


class OutputGraphic(QWidget):
    def __init__(self):
        super(OutputGraphic, self).__init__()
        vbox = QVBoxLayout(self)
        self.fig = figure()
        self.view = None

        self.canvas = FigureCanvasQTAgg(self.fig)
        toolbar = NavigationToolbar2QT(self.canvas, self)
        vbox.addWidget(self.canvas)
        vbox.addWidget(toolbar)

    def connectTo(self, view):
        self.view = view

    def slot_DrawPlot(self):
        data = self.view.getItemData()
        func_id = data.get("id")
        if func_id > 0:
            par1 = data.get("par1")
            par2 = data.get("par2")

            x = numpy.arange(-5.0, 5.0, 0.001)

            def _f1(t):
                return par1 * numpy.cos(par1 * numpy.pi * t)

            ax = self.fig.add_subplot(211)
            # discards the old graph
            ax.hold(False)
            ax.plot(x, _f1(x))

            ax2 = self.fig.add_subplot(212)
            ax2.hold(False)
            if func_id == 1:
                ax2.plot(x, par1 * x + par2)
            elif func_id == 2:
                ax2.plot(x, par1 * x ** 2)

            self.canvas.draw()
