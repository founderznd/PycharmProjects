# widget in tab2
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.pyplot import *

from PyQt4.QtGui import *


class OutputGraphic(QWidget):
    def __init__(self):
        super(OutputGraphic, self).__init__()
        vbox = QVBoxLayout(self)
        self.fig = figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        toolbar = NavigationToolbar2QT(self.canvas, self)
        vbox.addWidget(self.canvas)
        vbox.addWidget(toolbar)
