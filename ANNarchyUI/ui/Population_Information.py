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
        Form.resize(196, 450)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(-1, 40, -1, 50)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.name = QtGui.QLineEdit(Form)
        self.name.setText(_fromUtf8(""))
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.name.setObjectName(_fromUtf8("name"))
        self.verticalLayout.addWidget(self.name)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.geometry = QtGui.QLineEdit(Form)
        self.geometry.setText(_fromUtf8(""))
        self.geometry.setAlignment(QtCore.Qt.AlignCenter)
        self.geometry.setObjectName(_fromUtf8("geometry"))
        self.verticalLayout.addWidget(self.geometry)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.comboBox_neuron_type = QtGui.QComboBox(Form)
        self.comboBox_neuron_type.setObjectName(_fromUtf8("comboBox_neuron_type"))
        self.comboBox_neuron_type.addItem(_fromUtf8(""))
        self.comboBox_neuron_type.addItem(_fromUtf8(""))
        self.comboBox_neuron_type.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.comboBox_neuron_type)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Population", None))
        self.label_2.setText(_translate("Form", "Geometry", None))
        self.geometry.setToolTip(_translate("Form", "<html><head/><body>please type paramters like (a1,a2,...,an)</span></pre></body></html>", None))
        self.label_3.setText(_translate("Form", "Neuron Type", None))
        self.comboBox_neuron_type.setItemText(0, _translate("Form", "Define Own...", None))
        self.comboBox_neuron_type.setItemText(1, _translate("Form", "LeakyIntegratorNeuron", None))
        self.comboBox_neuron_type.setItemText(2, _translate("Form", "Izhikevich", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

