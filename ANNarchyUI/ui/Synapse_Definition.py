# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Synapse_Definition.ui'
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
        Dialog.resize(391, 399)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_2.addWidget(self.label_9)
        self.comboBox_synapse_type = QtGui.QComboBox(Dialog)
        self.comboBox_synapse_type.setObjectName(_fromUtf8("comboBox_synapse_type"))
        self.horizontalLayout_2.addWidget(self.comboBox_synapse_type)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_basic = QtGui.QWidget()
        self.tab_basic.setObjectName(_fromUtf8("tab_basic"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_basic)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_6 = QtGui.QLabel(self.tab_basic)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout.addWidget(self.label_6)
        self.lineEdit_name = QtGui.QLineEdit(self.tab_basic)
        self.lineEdit_name.setObjectName(_fromUtf8("lineEdit_name"))
        self.horizontalLayout.addWidget(self.lineEdit_name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_7 = QtGui.QLabel(self.tab_basic)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout.addWidget(self.label_7)
        self.plainTextEdit_description = QtGui.QPlainTextEdit(self.tab_basic)
        self.plainTextEdit_description.setObjectName(_fromUtf8("plainTextEdit_description"))
        self.verticalLayout.addWidget(self.plainTextEdit_description)
        self.tabWidget.addTab(self.tab_basic, _fromUtf8(""))
        self.tab_parameter = QtGui.QWidget()
        self.tab_parameter.setObjectName(_fromUtf8("tab_parameter"))
        self.formLayout = QtGui.QFormLayout(self.tab_parameter)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.tab_parameter)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.plainTextEdit_parameter = QtGui.QPlainTextEdit(self.tab_parameter)
        self.plainTextEdit_parameter.setPlainText(_fromUtf8(""))
        self.plainTextEdit_parameter.setObjectName(_fromUtf8("plainTextEdit_parameter"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.plainTextEdit_parameter)
        self.label_2 = QtGui.QLabel(self.tab_parameter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.plainTextEdit_equation = QtGui.QPlainTextEdit(self.tab_parameter)
        self.plainTextEdit_equation.setObjectName(_fromUtf8("plainTextEdit_equation"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.plainTextEdit_equation)
        self.label_8 = QtGui.QLabel(self.tab_parameter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_8)
        self.plainTextEdit_function = QtGui.QPlainTextEdit(self.tab_parameter)
        self.plainTextEdit_function.setObjectName(_fromUtf8("plainTextEdit_function"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.plainTextEdit_function)
        self.tabWidget.addTab(self.tab_parameter, _fromUtf8(""))
        self.tab_spike = QtGui.QWidget()
        self.tab_spike.setObjectName(_fromUtf8("tab_spike"))
        self.formLayout_2 = QtGui.QFormLayout(self.tab_spike)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_3 = QtGui.QLabel(self.tab_spike)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.plainTextEdit_pre_spike = QtGui.QPlainTextEdit(self.tab_spike)
        self.plainTextEdit_pre_spike.setObjectName(_fromUtf8("plainTextEdit_pre_spike"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.plainTextEdit_pre_spike)
        self.label_4 = QtGui.QLabel(self.tab_spike)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.plainTextEdit_pos_spike = QtGui.QPlainTextEdit(self.tab_spike)
        self.plainTextEdit_pos_spike.setObjectName(_fromUtf8("plainTextEdit_pos_spike"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.plainTextEdit_pos_spike)
        self.label_5 = QtGui.QLabel(self.tab_spike)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.plainTextEdit_psp = QtGui.QPlainTextEdit(self.tab_spike)
        self.plainTextEdit_psp.setObjectName(_fromUtf8("plainTextEdit_psp"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.plainTextEdit_psp)
        self.tabWidget.addTab(self.tab_spike, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Synapse", None))
        self.label_9.setText(_translate("Dialog", "Synapse Type:", None))
        self.label_6.setText(_translate("Dialog", "Name:", None))
        self.label_7.setText(_translate("Dialog", "description:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_basic), _translate("Dialog", "Basic", None))
        self.label.setText(_translate("Dialog", "Parameter:", None))
        self.label_2.setText(_translate("Dialog", "Equation:", None))
        self.label_8.setText(_translate("Dialog", "Functions:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_parameter), _translate("Dialog", "Parameter", None))
        self.label_3.setText(_translate("Dialog", "pre_Spike:", None))
        self.label_4.setText(_translate("Dialog", "pos_Spike:", None))
        self.label_5.setText(_translate("Dialog", "psp:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_spike), _translate("Dialog", "Spike", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

