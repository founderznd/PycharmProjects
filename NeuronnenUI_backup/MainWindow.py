# coding:utf-8

from PyQt4.QtCore import *
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
        self.tab1 = cc.NeuralConnectionView()
        self.tab2 = pv.OutputGraphic()
        # connect tab1 to tab2, in order to get the data from items of tab1
        self.tab2.connectTo(self.tab1)

        tabwidget.addTab(self.tab1, "Connections")
        tabwidget.addTab(self.tab2, "Graphics")
        hbox_1.addWidget(tabwidget)

        self.vbox1 = QVBoxLayout()
        self.info = QGroupBox()
        self.info.setTitle("Paramters:")
        info_layout = QVBoxLayout(self.info)

        info_layout.addStretch()
        self.par1 = QLabel("No Data!!")
        info_layout.addWidget(self.par1)
        self.par1.setAlignment(Qt.AlignCenter)

        info_layout.addStretch()

        self.sim_button = QPushButton("Begin")
        self.sim_button.setFixedSize(240, 80)
        self.info.setMaximumWidth(240)
        self.vbox1.addWidget(self.info)
        self.vbox1.addWidget(self.sim_button)
        hbox_1.addLayout(self.vbox1)

        self.connect(self.tab1.scene, SIGNAL("repaintSignal()"), self.slot_rewriteInfo)
        self.connect(self.tab1.scene, SIGNAL("repaintSignal()"), self.tab2.slot_DrawPlot)
        self.connect(self.sim_button, SIGNAL("clicked()"), self.tab2.slot_DrawPlot)

    def slot_rewriteInfo(self):
        data = self.tab1.getItemData()
        s = QString(str(data))
        s.remove("{")
        s.remove("}")
        self.par1.setText(s)
        self.par1.setWordWrap(True)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
