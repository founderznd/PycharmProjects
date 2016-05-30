# coding:utf-8
# 窗口停靠效果实验

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyDock(QMainWindow):
    def __init__(self):
        super(MyDock, self).__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.central_layout = QVBoxLayout(self.main_widget)
        main_widget = QTextEdit(u"主窗口")
        main_widget.setAlignment(Qt.AlignHCenter)
        self.central_layout.addWidget(main_widget)

        dock_widget_1 = QDockWidget("1")
        dock_widget_2 = QDockWidget("2")
        dock_widget_3 = QDockWidget("3")

        dock_widget_1.setWidget(QTextEdit("dock only at left and right"))
        dock_widget_2.setWidget(QTextEdit("only can flow"))
        dock_widget_3.setWidget(QTextEdit("can do anything"))

        dock_widget_1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock_widget_1.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetVerticalTitleBar)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget_1)

        dock_widget_2.setFeatures(QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget_2)

        dock_widget_3.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock_widget_3)


app = QApplication(sys.argv)
widget = MyDock()
widget.show()
sys.exit(app.exec_())
