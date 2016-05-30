# -*- coding: utf-8 -*-
# 实例1：HelloWorld

import sys
from PyQt4.QtGui import *


class HelloWorld(QWidget):
    def __init__(self):
        super(HelloWorld, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        b = QPushButton("Hello,World!", self)
        b.clicked.connect(quit)


app = QApplication(sys.argv)
widget = HelloWorld()
sys.exit(app.exec_())
