# coding: utf-8

from ast import literal_eval

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui import ItemInformation, Neuron_Definition

"""enum for neuron type"""


class NeuronType(object):
    LeakyIntegratorNeuron = 0
    Izhikevich = 1
    DefineOwn = 2


# this class is used to store all Informations of Population
class InfoWidget(QWidget):
    def __init__(self):
        super(InfoWidget, self).__init__()
        self.ui = ItemInformation.Ui_Form()
        self.ui.setupUi(self)

        # all parameters will be saved in this dictionary
        self.data = {"name": "", "geometry": "", "parameter": "", "equation": "", "spike": "", "reset": ""}
        self.predata = self.data
        # geometry infos saved in this tuple
        self.tuple = None

        # regular expression matches (a1,a2,...,an)
        self.rx = QRegExp("\( *\d+ *(, *\d+ *)*\)")

        self.dialog = QDialog()
        self.dui = Neuron_Definition.Ui_Dialog()
        self.dui.setupUi(self.dialog)

        self.connect(self.ui.neuron_type, SIGNAL("activated(int)"), self.open_Dialog)
        self.connect(self.ui.name, SIGNAL("editingFinished()"), self.slot_updateData)
        self.connect(self.ui.geometry, SIGNAL("editingFinished()"), self.slot_updateData)
        self.connect(self.dui.buttonBox, SIGNAL("accepted()"), self.slot_updateData)
        self.connect(self.dui.buttonBox, SIGNAL("rejected()"), self.slot_rollback)

    # refresh data
    def slot_updateData(self):
        self.data.update({"name": self.ui.name.text()})
        self.data.update({"geometry": self.ui.geometry.text()})
        self.data.update({"parameter": self.dui.parameter.toPlainText()})
        self.data.update({"equation": self.dui.equation.toPlainText()})
        self.data.update({"spike": self.dui.spike.text()})
        self.data.update({"reset": self.dui.reset.text()})
        self.format_Data()
        # convert QString to Tuple
        a = str(self.data.get("geometry"))
        if a:
            self.tuple = literal_eval(a)

    # data rollback
    def slot_rollback(self):
        self.data.update(self.predata)
        self.format_Data()
        # self.ui.name.undo()
        # self.ui.geometry.undo()
        self.dui.parameter.setText(self.data.get("parameter"))
        self.dui.equation.setText(self.data.get("equation"))
        self.dui.spike.setText(self.data.get("spike"))
        self.dui.reset.setText(self.data.get("reset"))

    # make sure the data in dictionary is valid
    def format_Data(self):
        # geometry
        geometry = self.data.get("geometry")
        self.rx.indexIn(geometry)
        strl = self.rx.capturedTexts()
        strl[0] = strl[0].remove(" ")
        self.ui.geometry.setText(strl[0])
        self.data.update({"geometry": strl[0]})

    def open_Dialog(self, i):
        self.predata.update(self.data)
        # here can change layouts of dialog recorrding to neuron type
        # layout of  LeakyIntegratorNeuron
        if i is NeuronType.LeakyIntegratorNeuron:
            self.dui.label_2.hide()
            self.dui.label_4.hide()
            self.dui.spike.hide()
            self.dui.reset.hide()
            self.data.setdefault("spike")
            self.data.setdefault("reset")
        elif i is NeuronType.Izhikevich or NeuronType.DefineOwn:
            self.dui.label_2.show()
            self.dui.label_4.show()
            self.dui.spike.show()
            self.dui.reset.show()

        self.dialog.exec_()