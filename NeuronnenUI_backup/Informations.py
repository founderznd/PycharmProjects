# coding: utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

""" here defines all function Widgets """


class NoFunction(QGroupBox):
    def __init__(self):
        super(NoFunction, self).__init__()
        self.data = {}
        self.setTitle("Parameters:")

        layout = QGridLayout(self)
        label = QLabel("No Data!")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

    def setData(self):
        self.data["id"] = 0
        self.data["name"] = "No Data!!"
        return self.data


class Function_1(QGroupBox):
    def __init__(self):
        super(Function_1, self).__init__()
        self.data = {}
        self.setTitle("Parameters:")

        layout = QFormLayout(self)
        self.formular = QLabel("y = a * x + b")
        name1 = QLabel("a = ")
        self.par1 = QDoubleSpinBox()
        self.par1.setRange(-999.999, 999.999)
        name2 = QLabel("b = ")
        self.par2 = QDoubleSpinBox()
        self.par2.setRange(-999.999, 999.999)
        layout.addRow(self.formular)
        layout.addRow(name1, self.par1)
        layout.addRow(name2, self.par2)

    def setData(self):
        self.data["id"] = 1
        self.data["name"] = self.formular.text()
        self.data["par1"] = self.par1.value()
        self.data["par2"] = self.par2.value()
        return self.data


class Function_2(QGroupBox):
    def __init__(self):
        super(Function_2, self).__init__()
        self.data = {}
        self.setTitle("Parameters:")

        layout = QFormLayout(self)
        self.formular = QLabel("y = a * x^2")
        name1 = QLabel("a = ")
        self.par1 = QDoubleSpinBox()
        self.par1.setRange(-999.999, 999.999)

        layout.addRow(self.formular)
        layout.addRow(name1, self.par1)

    def setData(self):
        self.data["id"] = 2
        self.data["name"] = self.formular.text()
        self.data["par1"] = self.par1.value()
        return self.data


""" ################################################################## """


class Parameters(QWidget):
    def __init__(self):
        super(Parameters, self).__init__()
        self.i = 0
        # all parameters will be saved in this dictionary
        self.data = {}

        self.vbox = QVBoxLayout(self)

        self.combox = QComboBox()
        self.combox.addItems(["none", "1", "2"])
        self.vbox.addWidget(self.combox)

        self.stackHub = QStackedWidget()

        self.stack0 = NoFunction()
        self.stack1 = Function_1()
        self.stack2 = Function_2()

        self.stackHub.addWidget(self.stack0)
        self.stackHub.addWidget(self.stack1)
        self.stackHub.addWidget(self.stack2)

        self.vbox.addWidget(self.stackHub)
        self.connect(self.combox, SIGNAL("activated(int)"), self.stackHub.setCurrentIndex)

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.cancel_button)
        hbox.addWidget(self.save_button)
        self.vbox.addLayout(hbox)

        self.connect(self.cancel_button, SIGNAL("clicked()"), self.close)
        self.connect(self.save_button, SIGNAL("clicked()"), self.saveData)

    def setupInfo(self):
        f = self.stackHub.currentIndex()
        if f == 0:
            self.data.update(self.stack0.setData())
        elif f == 1:
            self.data.update(self.stack1.setData())
        elif f == 2:
            self.data.update(self.stack2.setData())

    def saveData(self):
        self.setupInfo()
        self.close()
