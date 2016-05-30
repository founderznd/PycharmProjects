# coding:utf-8
# 表格的使用

import sys
from PyQt4.QtGui import *


class MyExcel(QMainWindow):
    def __init__(self):
        super(MyExcel, self).__init__()
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)
        self.tablewidget = QTableWidget(12, 5)
        self.sexylabel = QLabel("sexy")
        self.namelabel = QLabel("name")
        self.birthlabel = QLabel("birthday")
        self.careerlabel = QLabel("career")
        self.salarylabel = QLabel("salary")

        self.initUI()
        self.show()

    def initUI(self):
        self.resize(800, 600)
        self.move(400, 200)
        self.layout.addWidget(self.tablewidget)
        self.tablewidget.setCellWidget(0, 0, self.sexylabel)
        self.tablewidget.setCellWidget(0, 1, self.namelabel)
        self.tablewidget.setCellWidget(0, 2, self.birthlabel)
        self.tablewidget.setCellWidget(0, 3, self.careerlabel)
        self.tablewidget.setCellWidget(0, 4, self.salarylabel)


app = QApplication(sys.argv)
excel = MyExcel()
sys.exit(app.exec_())
