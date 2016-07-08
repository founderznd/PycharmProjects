# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Neuron_Definition.ui'
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
        Dialog.resize(398, 364)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout.addWidget(self.label_5)
        self.neurontype = QtGui.QLineEdit(self.tab)
        self.neurontype.setText(_fromUtf8(""))
        self.neurontype.setObjectName(_fromUtf8("neurontype"))
        self.horizontalLayout.addWidget(self.neurontype)
        self.label_8 = QtGui.QLabel(self.tab)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout.addWidget(self.label_8)
        self.doubleSpinBox_refractory = QtGui.QDoubleSpinBox(self.tab)
        self.doubleSpinBox_refractory.setObjectName(_fromUtf8("doubleSpinBox_refractory"))
        self.horizontalLayout.addWidget(self.doubleSpinBox_refractory)
        self.label_9 = QtGui.QLabel(self.tab)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout.addWidget(self.label_9)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_2.addWidget(self.label_6)
        self.plainTextEdit_description = QtGui.QPlainTextEdit(self.tab)
        self.plainTextEdit_description.setObjectName(_fromUtf8("plainTextEdit_description"))
        self.verticalLayout_2.addWidget(self.plainTextEdit_description)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.tab_2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.plainTextEdit_function = QtGui.QPlainTextEdit(self.tab_2)
        self.plainTextEdit_function.setObjectName(_fromUtf8("plainTextEdit_function"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.plainTextEdit_function)
        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_7)
        self.parameter = QtGui.QPlainTextEdit(self.tab_2)
        self.parameter.setPlainText(_fromUtf8(""))
        self.parameter.setObjectName(_fromUtf8("parameter"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.parameter)
        self.equation = QtGui.QPlainTextEdit(self.tab_2)
        self.equation.setPlainText(_fromUtf8(""))
        self.equation.setObjectName(_fromUtf8("equation"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.equation)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.formLayout_3 = QtGui.QFormLayout(self.tab_3)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_2 = QtGui.QLabel(self.tab_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_4 = QtGui.QLabel(self.tab_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.spike = QtGui.QPlainTextEdit(self.tab_3)
        self.spike.setPlainText(_fromUtf8(""))
        self.spike.setObjectName(_fromUtf8("spike"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.spike)
        self.reset = QtGui.QPlainTextEdit(self.tab_3)
        self.reset.setPlainText(_fromUtf8(""))
        self.reset.setObjectName(_fromUtf8("reset"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.reset)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Neuron", None))
        self.label_5.setText(_translate("Dialog", "Neuron Type", None))
        self.label_8.setText(_translate("Dialog", "refractory:", None))
        self.label_9.setText(_translate("Dialog", "(ms)", None))
        self.label_6.setText(_translate("Dialog", "Description:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "description", None))
        self.label_3.setText(_translate("Dialog", "Equation:", None))
        self.label.setText(_translate("Dialog", "Parameters:", None))
        self.label_7.setText(_translate("Dialog", "Functions:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "parser", None))
        self.label_2.setText(_translate("Dialog", "Spike", None))
        self.label_4.setText(_translate("Dialog", "Reset", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "spike", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

