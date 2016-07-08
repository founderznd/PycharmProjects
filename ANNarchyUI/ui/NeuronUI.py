# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NeuronUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1000, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.simulation_button = QtGui.QPushButton(self.centralwidget)
        self.simulation_button.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.simulation_button.setFont(font)
        self.simulation_button.setObjectName(_fromUtf8("simulation_button"))
        self.gridLayout.addWidget(self.simulation_button, 1, 1, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_network = QtGui.QWidget()
        self.tab_network.setObjectName(_fromUtf8("tab_network"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_network)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gview_network = NeuralConnectionView(self.tab_network)
        self.gview_network.setFrameShape(QtGui.QFrame.NoFrame)
        self.gview_network.setFrameShadow(QtGui.QFrame.Plain)
        self.gview_network.setLineWidth(0)
        self.gview_network.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.gview_network.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.gview_network.setSceneRect(QtCore.QRectF(0.0, 0.0, 0.0, 0.0))
        self.gview_network.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.gview_network.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.gview_network.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.gview_network.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.gview_network.setViewportUpdateMode(QtGui.QGraphicsView.MinimalViewportUpdate)
        self.gview_network.setObjectName(_fromUtf8("gview_network"))
        self.gridLayout_2.addWidget(self.gview_network, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_network, _fromUtf8(""))
        self.tab_matplot = OutputGraphic()
        self.tab_matplot.setObjectName(_fromUtf8("tab_matplot"))
        self.tabWidget.addTab(self.tab_matplot, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 2, 1)
        self.information = QtGui.QGroupBox(self.centralwidget)
        self.information.setMinimumSize(QtCore.QSize(200, 0))
        self.information.setMaximumSize(QtCore.QSize(200, 16777215))
        self.information.setObjectName(_fromUtf8("information"))
        self.gridLayout.addWidget(self.information, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.simulation_button.setText(_translate("MainWindow", "Simulation", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_network), _translate("MainWindow", "Network", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_matplot), _translate("MainWindow", "Matplot", None))
        self.information.setTitle(_translate("MainWindow", "Informations", None))

from ConnectionView import NeuralConnectionView
from PlotView import OutputGraphic

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

