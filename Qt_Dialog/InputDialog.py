# coding: utf-8
# 标准输入框的使用
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.gridbox = QGridLayout(self)
        self.setWindowTitle(u"输入你的信息")
        self.label_1 = QLabel(u"姓名：")
        self.label_2 = QLabel(u"性别：")
        self.label_3 = QLabel(u"年龄：")
        self.label_4 = QLabel(u"身高：")
        self.line_1 = QLabel()
        self.line_2 = QLabel()
        self.line_3 = QLabel()
        self.line_4 = QLabel()
        self.button_1 = QPushButton("...")
        self.button_2 = QPushButton("...")
        self.button_3 = QPushButton("...")
        self.button_4 = QPushButton("...")
        self.setupUI()
        self.show()

    def setupUI(self):
        self.move(600, 400)
        self.gridbox.addWidget(self.label_1, 0, 0)
        self.gridbox.addWidget(self.label_2, 1, 0)
        self.gridbox.addWidget(self.label_3, 2, 0)
        self.gridbox.addWidget(self.label_4, 3, 0)
        self.gridbox.addWidget(self.line_1, 0, 1)
        self.gridbox.addWidget(self.line_2, 1, 1)
        self.gridbox.addWidget(self.line_3, 2, 1)
        self.gridbox.addWidget(self.line_4, 3, 1)
        self.gridbox.addWidget(self.button_1, 0, 2)
        self.gridbox.addWidget(self.button_2, 1, 2)
        self.gridbox.addWidget(self.button_3, 2, 2)
        self.gridbox.addWidget(self.button_4, 3, 2)
        self.button_1.setFixedWidth(50)
        self.button_2.setFixedWidth(50)
        self.button_3.setFixedWidth(50)
        self.button_4.setFixedWidth(50)
        self.line_1.setMinimumWidth(80)
        self.line_2.setMinimumWidth(80)
        self.line_3.setMinimumWidth(80)
        self.line_4.setMinimumWidth(80)
        self.label_1.setMaximumWidth(50)
        self.label_2.setMaximumWidth(50)
        self.label_3.setMaximumWidth(50)
        self.label_4.setMaximumWidth(50)
        self.line_1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.line_2.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.line_3.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.line_4.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        self.connect(self.button_1, SIGNAL("clicked()"), self.slot_input_name)
        self.connect(self.button_2, SIGNAL("clicked()"), self.slot_input_sexy)
        self.connect(self.button_3, SIGNAL("clicked()"), self.slot_input_age)
        self.connect(self.button_4, SIGNAL("clicked()"), self.slot_input_height)

    def slot_input_name(self):
        name = QInputDialog.getText(None, u"名字", u"输入名字：")
        self.line_1.setText(name[0])

    def slot_input_sexy(self):
        l = [u"男", u"女"]
        sexy = QInputDialog.getItem(None, "sexy", "select your sexy:", l)
        self.line_2.setText(sexy[0])

    def slot_input_age(self):
        age = QInputDialog.getInt(None, "age", "input your age:")
        if age[0] > 0:
            self.line_3.setText(str(age[0]))

    def slot_input_height(self):
        double = QInputDialog.getDouble(None, "height", "input your height:")
        if double[0] > 0:
            self.line_4.setText(str(double[0]))


app = QApplication(sys.argv)
widget = MainWindow()
sys.exit(app.exec_())
