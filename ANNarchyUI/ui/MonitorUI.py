# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MonitorUI.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(805, 466)
        Dialog.setSizeGripEnabled(True)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setMinimumSize(QtCore.QSize(491, 351))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget_matplot = MyMonitor(self.frame)
        self.widget_matplot.setObjectName(_fromUtf8("widget_matplot"))
        self.verticalLayout_2.addWidget(self.widget_matplot)
        self.horizontalLayout_3.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(Dialog)
        self.frame_2.setMinimumSize(QtCore.QSize(191, 448))
        self.frame_2.setMaximumSize(QtCore.QSize(191, 16777215))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox_monitor = QtGui.QGroupBox(self.frame_2)
        self.groupBox_monitor.setObjectName(_fromUtf8("groupBox_monitor"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_monitor)
        self.verticalLayout_4.setContentsMargins(2, 15, 2, 0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_7 = QtGui.QLabel(self.groupBox_monitor)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout.addWidget(self.label_7)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkBox_start = QtGui.QCheckBox(self.groupBox_monitor)
        self.checkBox_start.setText(_fromUtf8(""))
        self.checkBox_start.setObjectName(_fromUtf8("checkBox_start"))
        self.horizontalLayout.addWidget(self.checkBox_start)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_6 = QtGui.QLabel(self.groupBox_monitor)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_2.addWidget(self.label_6)
        self.doubleSpinBox_period = QtGui.QDoubleSpinBox(self.groupBox_monitor)
        self.doubleSpinBox_period.setObjectName(_fromUtf8("doubleSpinBox_period"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_8 = QtGui.QLabel(self.groupBox_monitor)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout.addWidget(self.label_8)
        self.lineEdit_variables = QtGui.QLineEdit(self.groupBox_monitor)
        self.lineEdit_variables.setObjectName(_fromUtf8("lineEdit_variables"))
        self.verticalLayout.addWidget(self.lineEdit_variables)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.pushButton_monitor = QtGui.QPushButton(self.groupBox_monitor)
        self.pushButton_monitor.setMinimumSize(QtCore.QSize(145, 50))
        self.pushButton_monitor.setDefault(False)
        self.pushButton_monitor.setObjectName(_fromUtf8("pushButton_monitor"))
        self.verticalLayout_4.addWidget(self.pushButton_monitor)
        self.verticalLayout_3.addWidget(self.groupBox_monitor)
        self.horizontalLayout_3.addWidget(self.frame_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Monitor", None))
        self.groupBox_monitor.setTitle(_translate("Dialog", "Monitor", None))
        self.label_7.setText(_translate("Dialog", "start:", None))
        self.label_6.setText(_translate("Dialog", "period:", None))
        self.label_8.setText(_translate("Dialog", "variables:", None))
        self.pushButton_monitor.setText(_translate("Dialog", "Monitor", None))

from ANNarchyData import MyMonitor

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

