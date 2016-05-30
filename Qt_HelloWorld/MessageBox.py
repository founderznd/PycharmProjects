# coding:utf-8
# 各种消息框

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MessageBox(QWidget):
    def __init__(self):
        super(MessageBox, self).__init__()
        # layout
        self.mainvbox = QVBoxLayout(self)
        self.vbox = QVBoxLayout()
        self.gridlayout = QGridLayout()

        # widget
        self.label = QLabel("About Qt: Message Box")
        self.question_button = QPushButton("Question")
        self.information_button = QPushButton("Information")
        self.warning_button = QPushButton("Warning")
        self.critical_button = QPushButton("Critical")
        self.about_button = QPushButton("About")
        self.about_qt_button = QPushButton("About Qt")

        self.setupUI()
        self.show()

    def setupUI(self):
        self.mainvbox.addLayout(self.vbox)
        self.mainvbox.addLayout(self.gridlayout)
        self.vbox.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)
        self.gridlayout.addWidget(self.question_button, 0, 0)
        self.gridlayout.addWidget(self.information_button, 0, 1)
        self.gridlayout.addWidget(self.warning_button, 1, 0)
        self.gridlayout.addWidget(self.critical_button, 1, 1)
        self.gridlayout.addWidget(self.about_button, 2, 0)
        self.gridlayout.addWidget(self.about_qt_button, 2, 1)

        self.connect(self.question_button, SIGNAL("clicked()"), self.slot_question)
        self.connect(self.information_button, SIGNAL("clicked()"), self.slot_information)
        self.connect(self.warning_button, SIGNAL("clicked()"), self.slot_warning)
        self.connect(self.critical_button, SIGNAL("clicked()"), self.slot_critical)
        self.connect(self.about_button, SIGNAL("clicked()"), self.slot_about)
        self.connect(self.about_qt_button, SIGNAL("clicked()"), self.slot_about_qt)

    def slot_question(self):
        # 第一个按钮返回0,第二个返回1,第三个返回2
        # 最后两个数字分别代表默认按钮，ESC对应按钮
        msg = QMessageBox.question(None, "Question", u"已到达文档结尾，是否从头开始？", "OK", "Abort", "Cancel", 2, 2)
        if msg == 0:
            self.label.setText("OK")
        elif msg == 1:
            self.label.setText("Abort")
        else:
            self.label.setText("Cancel")

    def slot_information(self):
        msg = QMessageBox.information(None, "information", "you must work harder!", "OK", "Abort", "Cancel", 0, 2)
        if msg == 0:
            self.label.setText("OK")
        elif msg == 1:
            self.label.setText("Abort")
        else:
            self.label.setText("Cancel")

    def slot_warning(self):
        msg = QMessageBox.warning(None, "warning", "you have no time!", "OK", "Abort", "Cancel", 0, 2)
        if msg == 0:
            self.label.setText("OK")
        elif msg == 1:
            self.label.setText("Abort")
        else:
            self.label.setText("Cancel")

    def slot_critical(self):
        msg = QMessageBox.critical(None, "critical", "you can't find job!", "OK", "Abort", "Cancel", 0, 2)
        if msg == 0:
            self.label.setText("OK")
        elif msg == 1:
            self.label.setText("Abort")
        else:
            self.label.setText("Cancel")

    def slot_about(self):
        QMessageBox.about(None, "about", "PyQt4 Excercise")
        self.label.setText("about MessageBox")

    def slot_about_qt(self):
        QMessageBox.aboutQt(None, "About Qt")
        self.label.setText("About Qt MessageBox")


app = QApplication(sys.argv)
window = MessageBox()
sys.exit(app.exec_())
