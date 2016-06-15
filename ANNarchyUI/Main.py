# coding:utf-8
# main function


from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui import NeuronUI


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = NeuronUI.Ui_MainWindow()
        self.ui.setupUi(self)

        self.info_stack = self.ui.connection_gview.scene.info_stack
        vbox = QVBoxLayout()
        self.ui.information.setLayout(vbox)
        vbox.addWidget(self.info_stack)

        # connect tab1 to tab2, in order to get the data from items of tab1
        self.ui.matplot_tab.connectTo(self.ui.connection_gview)

        self.connect(self.ui.simulation_button, SIGNAL("clicked()"), self.slot_all)
        self.connect(self.ui.connection_gview.scene, SIGNAL("replot()"), self.ui.matplot_tab.slot_DrawPlot)
        self.connect(self.ui.connection_gview.population_button, SIGNAL("clicked(bool)"), self.slot_addNeuron)

    def slot_all(self):
        if self.ui.connection_gview.scene.currentItem:
            self.ui.connection_gview.scene.currentItem.info.slot_updateData()
        self.ui.matplot_tab.slot_DrawPlot()

    def slot_addNeuron(self, isChecked):
        self.ui.connection_gview.scene.isPrepared = isChecked


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
