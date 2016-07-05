# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Projection_Information.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(196, 450)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(-1, 40, -1, 50)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit_name = QtGui.QLineEdit(Form)
        self.lineEdit_name.setObjectName(_fromUtf8("lineEdit_name"))
        self.verticalLayout.addWidget(self.lineEdit_name)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.lineEdit_target = QtGui.QLineEdit(Form)
        self.lineEdit_target.setObjectName(_fromUtf8("lineEdit_target"))
        self.verticalLayout.addWidget(self.lineEdit_target)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.comboBox_synapse_type = QtGui.QComboBox(Form)
        self.comboBox_synapse_type.setObjectName(_fromUtf8("comboBox_synapse_type"))
        self.comboBox_synapse_type.addItem(_fromUtf8(""))
        self.comboBox_synapse_type.addItem(_fromUtf8(""))
        self.comboBox_synapse_type.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.comboBox_synapse_type)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_pos_Pop = QtGui.QLabel(Form)
        self.label_pos_Pop.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_pos_Pop.setObjectName(_fromUtf8("label_pos_Pop"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_pos_Pop)
        self.label_pre_Pop = QtGui.QLabel(Form)
        self.label_pre_Pop.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_pre_Pop.setObjectName(_fromUtf8("label_pre_Pop"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_pre_Pop)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_2.setText(_translate("Form", "Projection", None))
        self.label_5.setText(_translate("Form", "Target:", None))
        self.label_4.setText(_translate("Form", "Synapse Type", None))
        self.comboBox_synapse_type.setItemText(0, _translate("Form", "Define Own...", None))
        self.comboBox_synapse_type.setItemText(1, _translate("Form", "Rate-coded synapse", None))
        self.comboBox_synapse_type.setItemText(2, _translate("Form", "Spiking synapse", None))
        self.label.setText(_translate("Form", "pre_Pop:", None))
        self.label_3.setText(_translate("Form", "pos_Pop:", None))
        self.label_pos_Pop.setText(_translate("Form", "TextLabel", None))
        self.label_pre_Pop.setText(_translate("Form", "TextLabel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

