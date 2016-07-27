# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Population_Information.ui'
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
        Form.resize(196, 479)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(-1, 25, -1, -1)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.name = QtGui.QLineEdit(Form)
        self.name.setText(_fromUtf8(""))
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.name.setObjectName(_fromUtf8("name"))
        self.verticalLayout_2.addWidget(self.name)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.geometry = QtGui.QLineEdit(Form)
        self.geometry.setText(_fromUtf8(""))
        self.geometry.setAlignment(QtCore.Qt.AlignCenter)
        self.geometry.setObjectName(_fromUtf8("geometry"))
        self.verticalLayout_2.addWidget(self.geometry)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.comboBox_neuron_type = QtGui.QComboBox(Form)
        self.comboBox_neuron_type.setObjectName(_fromUtf8("comboBox_neuron_type"))
        self.verticalLayout_2.addWidget(self.comboBox_neuron_type)
        self.groupBox_monitor = QtGui.QGroupBox(Form)
        self.groupBox_monitor.setCheckable(True)
        self.groupBox_monitor.setObjectName(_fromUtf8("groupBox_monitor"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_monitor)
        self.verticalLayout.setContentsMargins(0, 15, 0, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_7 = QtGui.QLabel(self.groupBox_monitor)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout.addWidget(self.label_7)
        self.checkBox_start = QtGui.QCheckBox(self.groupBox_monitor)
        self.checkBox_start.setText(_fromUtf8(""))
        self.checkBox_start.setObjectName(_fromUtf8("checkBox_start"))
        self.horizontalLayout.addWidget(self.checkBox_start)
        self.label_6 = QtGui.QLabel(self.groupBox_monitor)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout.addWidget(self.label_6)
        self.doubleSpinBox_period = QtGui.QDoubleSpinBox(self.groupBox_monitor)
        self.doubleSpinBox_period.setObjectName(_fromUtf8("doubleSpinBox_period"))
        self.horizontalLayout.addWidget(self.doubleSpinBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_8 = QtGui.QLabel(self.groupBox_monitor)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout.addWidget(self.label_8)
        self.lineEdit_variables = QtGui.QLineEdit(self.groupBox_monitor)
        self.lineEdit_variables.setObjectName(_fromUtf8("lineEdit_variables"))
        self.verticalLayout.addWidget(self.lineEdit_variables)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.groupBox_monitor)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Population", None))
        self.label_4.setText(_translate("Form", "name:", None))
        self.label_2.setText(_translate("Form", "Geometry:", None))
        self.geometry.setToolTip(_translate("Form", "<html><head/><body>please type paramters like (a1,a2,...,an)</span></pre></body></html>", None))
        self.label_3.setText(_translate("Form", "Neuron Type:", None))
        self.groupBox_monitor.setTitle(_translate("Form", "Monitor", None))
        self.label_7.setText(_translate("Form", "start:", None))
        self.label_6.setText(_translate("Form", "period:", None))
        self.label_8.setText(_translate("Form", "variables:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

