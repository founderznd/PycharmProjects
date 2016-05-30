# coding:utf-8
# 可扩展对话框的实现

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Extension(QDialog):
    def __init__(self):
        super(Extension, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        # 使对话框尺寸保持相对固定
        self.layout.setSizeConstraint(QLayout.SetFixedSize)

        self.base_info = self.base_widget()
        self.detail_info = self.detail_widget()

        self.layout.addWidget(self.base_info)
        self.layout.addWidget(self.detail_info)

    def base_widget(self):
        base_info = QWidget()
        layout = QGridLayout(base_info)
        layout.addWidget(QLabel(u"姓名："), 0, 0)
        layout.addWidget(QLineEdit(), 0, 1)
        button_1 = QPushButton(u"确认")
        layout.addWidget(button_1, 0, 2)
        layout.addWidget(QLabel(u"性别："), 1, 0)
        combo_1 = QComboBox()
        combo_1.addItems([u"男", u"女"])
        layout.addWidget(combo_1, 1, 1)
        button_2 = QPushButton(u"详细")
        layout.addWidget(button_2, 1, 2)
        self.connect(button_2, SIGNAL("clicked()"), self.slot_show)
        return base_info

    def detail_widget(self):
        detail_widget = QWidget()
        form_layout = QFormLayout(detail_widget)
        form_layout.addRow("Age: ", QLineEdit())
        combo = QComboBox()
        combo.addItems(["1", "2", "3", "4"])
        form_layout.addRow("Department: ", combo)
        form_layout.addRow("Email:", QLineEdit())
        detail_widget.hide()
        return detail_widget

    def slot_show(self):
        if self.detail_info.isHidden():
            self.detail_info.show()
        else:
            self.detail_info.hide()


import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Extension()
    widget.show()
    sys.exit(app.exec_())
