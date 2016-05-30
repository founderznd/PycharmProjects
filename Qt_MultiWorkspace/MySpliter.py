# coding: utf-8
# 多文档的实现

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MySpliter(QMainWindow):
    def __init__(self):
        super(MySpliter, self).__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.left = QVBoxLayout()
        self.right = QVBoxLayout()

        self.layout.addLayout(self.left, 0, 0)
        self.layout.addLayout(self.right, 0, 1)

        self.spliter = QSplitter(Qt.Horizontal)
        self.spliter.addWidget(QTextEdit("left"))
        self.spliter_2 = QSplitter(Qt.Vertical)
        self.spliter.addWidget(self.spliter_2)
        self.spliter_2.addWidget(QTextEdit("right upon"))
        self.spliter_2.addWidget(QTextEdit("right bottom"))

        self.left.addWidget(self.spliter)
        self.right.addWidget(QTextEdit("§§FDSFd"))
        self.right.addWidget(QTextEdit("fdghjjj"))


app = QApplication(sys.argv)
window = MySpliter()
window.show()
sys.exit(app.exec_())
