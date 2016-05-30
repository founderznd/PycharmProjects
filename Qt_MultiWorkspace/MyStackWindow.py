# coding:utf-8
# 利用QStackedWidget类，实现堆栈窗体

import sys

from PyQt4.QtGui import *


class MyStack(QMainWindow):
    def __init__(self):
        super(MyStack, self).__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setupUI()

    def setupUI(self):
        hbox = QHBoxLayout(self.central_widget)

        l_widget = QListWidget()
        l_widget.addItems(["window1", "window2", "window3"])

        stack_widget = QStackedWidget()
        stack_widget.addWidget(QLabel("this is window 1"))
        stack_widget.addWidget(QLabel("this is window 2"))
        stack_widget.addWidget(QLabel("this is window 3"))

        hbox.addWidget(l_widget)
        hbox.addWidget(stack_widget)

        hbox.setStretch(0, 1)
        hbox.setStretch(1, 3)

        # self.connect(l_widget, SIGNAL("currentRowChanged(int)"), stack_widget.setCurrentIndex)
        l_widget.currentRowChanged.connect(stack_widget.setCurrentIndex)


app = QApplication(sys.argv)
window = MyStack()
window.show()
sys.exit(app.exec_())
