# coding: utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

""" here defines all function Widgets """


class ParameterStack(QWidget):
    def __init__(self):
        super(ParameterStack, self).__init__()
        self.i = 0
        # all parameters will be saved in this dictionary
        self.data = {}
        # geometry infos saved in this tuple
        self.tuple = None

        vbox = QVBoxLayout()
        vbox.addStretch()

        label = QLabel("Geometry")
        label.setAlignment(Qt.AlignCenter)
        label.setFrameStyle(QFrame.Box | QFrame.Sunken)
        vbox.addWidget(label)

        hbox = QHBoxLayout()
        self.row = QSpinBox()
        hbox.addWidget(QLabel("row:"))
        hbox.addWidget(self.row)
        self.col = QSpinBox()
        hbox.addWidget(QLabel("col:"))
        hbox.addWidget(self.col)

        vbox.addLayout(hbox)
        vbox.addStretch()

        label = QLabel("Neuron")
        label.setAlignment(Qt.AlignCenter)
        label.setFrameStyle(QFrame.Box | QFrame.Sunken)
        vbox.addWidget(label)

        self.paramaters = QPlainTextEdit()
        self.paramaters.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.paramaters.setFrameStyle(QFrame.Plain)
        vbox.addWidget(QLabel("parameters:"))
        vbox.addWidget(self.paramaters)

        self.equations = QPlainTextEdit()
        self.equations.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.equations.setFrameStyle(QFrame.Plain)
        vbox.addWidget(QLabel("equations:"))
        vbox.addWidget(self.equations)

        self.setLayout(vbox)

    def saveData(self):
        del self.tuple
        self.tuple = (self.row.value(), self.col.value())
        self.data["geometry_row"] = self.row.value()
        self.data["geometry_col"] = self.col.value()
        self.data["neuron_par"] = self.paramaters.toPlainText()
        self.data["neuron_eq"] = self.equations.toPlainText()
