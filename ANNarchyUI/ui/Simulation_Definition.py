# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Simulation_Definition.ui'
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
        Dialog.setMaximumSize(QtCore.QSize(320, 145))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.doubleSpinBox_duration = QtGui.QDoubleSpinBox(Dialog)
        self.doubleSpinBox_duration.setDecimals(1)
        self.doubleSpinBox_duration.setMaximum(10000.0)
        self.doubleSpinBox_duration.setProperty("value", 1000.0)
        self.doubleSpinBox_duration.setObjectName(_fromUtf8("doubleSpinBox_duration"))
        self.horizontalLayout.addWidget(self.doubleSpinBox_duration)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.spinBox_net_id = QtGui.QSpinBox(Dialog)
        self.spinBox_net_id.setObjectName(_fromUtf8("spinBox_net_id"))
        self.horizontalLayout.addWidget(self.spinBox_net_id)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.checkBox_callbacks = QtGui.QCheckBox(Dialog)
        self.checkBox_callbacks.setText(_fromUtf8(""))
        self.checkBox_callbacks.setChecked(True)
        self.checkBox_callbacks.setObjectName(_fromUtf8("checkBox_callbacks"))
        self.horizontalLayout_2.addWidget(self.checkBox_callbacks)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.checkBox_measure_time = QtGui.QCheckBox(Dialog)
        self.checkBox_measure_time.setText(_fromUtf8(""))
        self.checkBox_measure_time.setObjectName(_fromUtf8("checkBox_measure_time"))
        self.horizontalLayout_2.addWidget(self.checkBox_measure_time)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_3.addWidget(self.label_5)
        self.lineEdit_population = QtGui.QLineEdit(Dialog)
        self.lineEdit_population.setObjectName(_fromUtf8("lineEdit_population"))
        self.horizontalLayout_3.addWidget(self.lineEdit_population)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.comboBox_operator = QtGui.QComboBox(Dialog)
        self.comboBox_operator.setObjectName(_fromUtf8("comboBox_operator"))
        self.comboBox_operator.addItem(_fromUtf8(""))
        self.comboBox_operator.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.comboBox_operator)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Simulation", None))
        self.label.setText(_translate("Dialog", "duration:", None))
        self.label_4.setText(_translate("Dialog", "net_id:", None))
        self.label_3.setText(_translate("Dialog", "callbacks:", None))
        self.label_2.setText(_translate("Dialog", "measure_time:", None))
        self.label_5.setText(_translate("Dialog", "population:", None))
        self.label_6.setText(_translate("Dialog", "operator:", None))
        self.comboBox_operator.setItemText(0, _translate("Dialog", "and", None))
        self.comboBox_operator.setItemText(1, _translate("Dialog", "or", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

