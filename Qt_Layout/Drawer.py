# coding:utf-8
# 抽屉效果的实现

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Drawer(QWidget):
    def __init__(self):
        super(Drawer, self).__init__()
        self.mainlayout = QVBoxLayout(self)
        self.toolbox = QToolBox()

        # 注意设置layout的两种方式
        # 1
        self.groupbox_1 = QGroupBox()
        self.vbox_1 = QVBoxLayout(self.groupbox_1)

        self.groupbox_2 = QGroupBox()
        self.vbox_2 = QVBoxLayout()

        self.groupbox_3 = QGroupBox()
        self.vbox_3 = QVBoxLayout()

        self.groupbox_4 = QGroupBox()
        self.vbox_4 = QVBoxLayout()

        self.button_1_1 = QToolButton()
        self.button_1_2 = QToolButton()
        self.button_1_3 = QToolButton()
        self.button_1_4 = QToolButton()

        self.button_2_1 = QToolButton()
        self.button_2_2 = QToolButton()
        self.button_2_3 = QToolButton()
        self.button_2_4 = QToolButton()
        self.button_2_5 = QToolButton()
        self.button_2_6 = QToolButton()
        self.button_2_7 = QToolButton()
        self.button_2_8 = QToolButton()

        self.initUI()
        self.show()

    def initUI(self):
        self.mainlayout.addWidget(self.toolbox)
        self.toolbox.addItem(self.groupbox_1, u"我的好友")
        self.toolbox.addItem(self.groupbox_2, u"陌生人")
        self.toolbox.addItem(self.groupbox_3, u"朋友")
        self.toolbox.addItem(self.groupbox_4, u"家人")

        # 2
        self.groupbox_2.setLayout(self.vbox_2)
        self.groupbox_3.setLayout(self.vbox_3)
        self.groupbox_4.setLayout(self.vbox_4)

        self.groupbox_1.setAlignment(Qt.AlignHCenter)

        self.vbox_1.addWidget(self.button_1_1)
        self.vbox_1.addWidget(self.button_1_2)
        self.vbox_1.addWidget(self.button_1_3)
        self.vbox_1.addWidget(self.button_1_4)

        self.vbox_2.addWidget(self.button_2_1)
        self.vbox_2.addWidget(self.button_2_2)
        self.vbox_2.addWidget(self.button_2_3)
        self.vbox_2.addWidget(self.button_2_4)
        self.vbox_2.addWidget(self.button_2_5)
        self.vbox_2.addWidget(self.button_2_6)
        self.vbox_2.addWidget(self.button_2_7)
        self.vbox_2.addWidget(self.button_2_8)


app = QApplication(sys.argv)
widget = Drawer()
sys.exit(app.exec_())
