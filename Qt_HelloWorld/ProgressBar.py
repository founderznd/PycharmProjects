# coding:utf-8
# 进度条的使用

import sys, time
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ProgressBar(QMainWindow):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.centralwidget = QDialog()
        self.setCentralWidget(self.centralwidget)
        self.mainlayout = QVBoxLayout(self.centralwidget)
        self.filenumlabel = QLabel("files number")
        self.filenum = QSpinBox()
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.filenumlabel)
        self.hbox1.addWidget(self.filenum)
        self.showtypelabel = QLabel("show type")
        l = ["progress bar", "progress dialog"]
        self.combobox = QComboBox()
        self.combobox.addItems(l)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.showtypelabel)
        self.hbox2.addWidget(self.combobox)
        #
        self.progressbar = QProgressBar()
        self.mainlayout.addLayout(self.hbox1)
        self.mainlayout.addLayout(self.hbox2)
        self.mainlayout.addWidget(self.progressbar)

        self.beginbutton = QPushButton("Begin")
        self.cancelbutton = QPushButton("Cancel")
        self.mainlayout.addWidget(self.beginbutton)
        self.mainlayout.addWidget(self.cancelbutton)

        self.connect(self.beginbutton, SIGNAL("clicked()"), self.slot_begin_button)

        self.show()

    def slot_begin_button(self):
        num = int(self.filenum.text())
        if self.combobox.currentIndex() == 0:  # progressbar
            self.progressbar.setRange(0, num)
            for i in range(1, num + 1):
                self.progressbar.setValue(i)
                time.sleep(1)
        else:
            progressdialog = QProgressDialog()
            progressdialog.setWindowTitle("progress dialog")
            progressdialog.setLabelText("Copying...")
            progressdialog.setCancelButtonText("Cancel")
            progressdialog.setRange(0, num)

            for i in range(1, num + 1):
                progressdialog.setValue(i)
                QCoreApplication.processEvents()
                time.sleep(1)
                if progressdialog.wasCanceled():
                    return


app = QApplication(sys.argv)
window = ProgressBar()
sys.exit(app.exec_())
