import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import NeuronenUI


class MyWindow(QMainWindow, NeuronenUI.Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.init_tabwidget()
        self.init_toolbox()

    def init_tabwidget(self):
        self.figure = plt.figure()
        # use matplot as a widget
        self.canvas = FigureCanvasQTAgg(self.figure)
        toolbar = NavigationToolbar2QT(self.canvas, self)
        layout = QVBoxLayout(self.tab_2)
        layout.addWidget(self.canvas)
        layout.addWidget(toolbar)

        self.slot_matplot()
        self.connect(self.pushButton, SIGNAL("clicked()"), self.slot_matplot)

    def slot_matplot(self):
        a = self.doubleSpinBox.value()
        b = self.doubleSpinBox_2.value()
        c = self.doubleSpinBox_3.value()

        x = np.arange(-5.0, 5.0, 0.001)

        def _f1(t):
            return a * np.cos(b * np.pi * t) + c

        def _f2(t):
            return t ** a + b * t + c

        ax = self.figure.add_subplot(211)
        # discards the old graph
        ax.hold(False)
        ax.plot(x, _f1(x))

        ax2 = self.figure.add_subplot(212)
        ax2.hold(False)
        ax2.plot(x, _f2(x))

        self.canvas.draw()

    def init_toolbox(self):

        layout = QVBoxLayout(self.page)

        icon_1 = self.icon("image/neuron.png")
        # icon_2 = self.icon("image/neuron.png")
        # icon_3 = self.icon("image/neuron.png")
        # icon_4 = self.icon("image/neuron.png")

        layout.addWidget(icon_1)
        # layout.addWidget(icon_2)
        # layout.addWidget(icon_3)
        # layout.addWidget(icon_4)

    def icon(self, path):
        icon = QLabel()
        pix = QPixmap(path).scaled(60,60)
        icon.setFixedSize(pix.size())
        icon.setPixmap(pix)
        icon.setFrameStyle(QFrame.Panel|QFrame.Raised)
        icon.setAlignment(Qt.AlignCenter)
        return icon


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
