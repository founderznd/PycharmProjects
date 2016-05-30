# coding:utf-8

from PyQt4.QtGui import *

import ConnectionView as cc
import PlotView as pv


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1280, 800)
        mainwidget = QWidget()
        self.setCentralWidget(mainwidget)
        hbox_1 = QHBoxLayout(mainwidget)

        tabwidget = QTabWidget()
        self.tab1 = cc.NeuronnenConnection()
        self.tab2 = pv.OutputGraphic()
        tabwidget.addTab(self.tab1, "Connections")
        tabwidget.addTab(self.tab2, "Graphics")
        hbox_1.addWidget(tabwidget)

        vbox1 = QVBoxLayout()
        self.gbox = QGroupBox("Infomation:")

        sim_button = QPushButton("Begin")
        sim_button.setFixedSize(240, 80)

        vbox1.addWidget(self.gbox)
        vbox1.addWidget(sim_button)
        hbox_1.addLayout(vbox1)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
