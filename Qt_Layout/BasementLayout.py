# coding:utf-8
# 基本布局管理

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class BasementLayoutWindow(QMainWindow):
    def __init__(self):
        super(BasementLayoutWindow, self).__init__()
        self.setWindowTitle("Layout")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.base_layout = QGridLayout()
        self.centralwidget.setLayout(self.base_layout)
        self.left_layout = QGridLayout()
        self.right_layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.base_layout.setMargin(20)
        self.base_layout.setSpacing(10)

        self.left_init()
        self.right_init()
        self.bottom_init()

    def left_init(self):
        self.base_layout.addLayout(self.left_layout, 0, 0)

        username_label = QLabel("username:")
        username_line = QLineEdit()

        name_label = QLabel("name:")
        name_line = QLineEdit()

        sexy_label = QLabel("sexuality:")
        l = [u"男", u"女"]
        sexy_selected = QComboBox()
        sexy_selected.addItems(l)

        department_label = QLabel("department:")
        department_label.setAlignment(Qt.AlignTop)
        department_text = QTextEdit()

        age_label = QLabel("age:")
        age_num = QSpinBox()

        comment_label = QLabel("comment:")
        comment_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        self.left_layout.addWidget(username_label, 0, 0)
        self.left_layout.addWidget(username_line, 0, 1)
        self.left_layout.addWidget(name_label, 1, 0)
        self.left_layout.addWidget(name_line, 1, 1)
        self.left_layout.addWidget(sexy_label, 2, 0)
        self.left_layout.addWidget(sexy_selected, 2, 1)
        self.left_layout.addWidget(department_label, 3, 0)
        self.left_layout.addWidget(department_text, 3, 1)
        self.left_layout.addWidget(age_label, 4, 0)
        self.left_layout.addWidget(age_num, 4, 1)
        # spanning from col 0 to 2
        self.left_layout.addWidget(comment_label, 5, 0, 5, 2)

    def right_init(self):
        self.base_layout.addLayout(self.right_layout, 0, 1)

        head_label = QLabel("Head:")

        head_icon = QLabel()
        pix = QPixmap("image/male_pic.png").scaled(50, 50)
        head_icon.resize(pix.size())
        head_icon.setPixmap(pix)

        refresh_button = QPushButton("refresh")

        hbox = QHBoxLayout()
        hbox.addWidget(head_label)
        hbox.addWidget(head_icon)
        hbox.addWidget(refresh_button)

        about_me_label = QLabel("about me:")
        about_me_text = QTextEdit()

        self.right_layout.addLayout(hbox)
        self.right_layout.addWidget(about_me_label)
        self.right_layout.addWidget(about_me_text)

    def bottom_init(self):
        self.base_layout.addLayout(self.bottom_layout, 1, 0, 1, 2)
        ok_button = QPushButton(u"确定")
        cancel_button = QPushButton(u"取消")
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(ok_button)
        self.bottom_layout.addWidget(cancel_button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BasementLayoutWindow()
    window.show()
    sys.exit(app.exec_())
