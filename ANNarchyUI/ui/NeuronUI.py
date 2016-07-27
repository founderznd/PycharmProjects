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
        MainWindow.resize(1010, 650)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.gview_network = NeuralConnectionView(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gview_network.sizePolicy().hasHeightForWidth())
        self.gview_network.setSizePolicy(sizePolicy)
        self.gview_network.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gview_network.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gview_network.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.gview_network.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.gview_network.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.gview_network.setViewportUpdateMode(QtGui.QGraphicsView.MinimalViewportUpdate)
        self.gview_network.setObjectName(_fromUtf8("gview_network"))
        self.verticalLayout_4.addWidget(self.gview_network)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_3 = QtGui.QFrame(self.centralwidget)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_3)
        self.verticalLayout.setContentsMargins(4, 2, 4, 2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.information = QtGui.QGroupBox(self.frame_3)
        self.information.setMinimumSize(QtCore.QSize(200, 0))
        self.information.setMaximumSize(QtCore.QSize(200, 16777215))
        self.information.setObjectName(_fromUtf8("information"))
        self.vbox_information = QtGui.QVBoxLayout(self.information)
        self.vbox_information.setContentsMargins(0, -1, 0, -1)
        self.vbox_information.setSpacing(15)
        self.vbox_information.setObjectName(_fromUtf8("vbox_information"))
        self.verticalLayout.addWidget(self.information)
        self.simulation_button = QtGui.QPushButton(self.frame_3)
        self.simulation_button.setMinimumSize(QtCore.QSize(0, 60))
        self.simulation_button.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.simulation_button.setFont(font)
        self.simulation_button.setObjectName(_fromUtf8("simulation_button"))
        self.verticalLayout.addWidget(self.simulation_button)
        self.horizontalLayout.addWidget(self.frame_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1010, 27))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuSave = QtGui.QMenu(self.menuBar)
        self.menuSave.setObjectName(_fromUtf8("menuSave"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionOpen = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../image/file_open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../image/file_save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon1)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_as = QtGui.QAction(MainWindow)
        self.actionSave_as.setIcon(icon1)
        self.actionSave_as.setObjectName(_fromUtf8("actionSave_as"))
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.menuSave.addSeparator()
        self.menuSave.addAction(self.actionNew)
        self.menuSave.addAction(self.actionOpen)
        self.menuSave.addSeparator()
        self.menuSave.addAction(self.actionSave)
        self.menuSave.addAction(self.actionSave_as)
        self.menuSave.addSeparator()
        self.menuBar.addAction(self.menuSave.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.information.setTitle(_translate("MainWindow", "Informations", None))
        self.simulation_button.setText(_translate("MainWindow", "Simulation", None))
        self.menuSave.setTitle(_translate("MainWindow", "File", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionSave_as.setText(_translate("MainWindow", "Save as ...", None))
        self.actionSave_as.setShortcut(_translate("MainWindow", "Ctrl+Shift+S", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N", None))

from ConnectionView import NeuralConnectionView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

