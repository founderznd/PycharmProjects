# -*- coding: utf-8 -*-
# 标准对话框的使用

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class StandardDialog(QWidget):
    def __init__(self):
        super(StandardDialog, self).__init__()
        # 添加u可以解决中文乱码问题
        self.button_1 = QPushButton(u"文件对话框")
        self.button_2 = QPushButton(u"颜色对话框")
        self.button_3 = QPushButton(u"字体对话框")
        self.text_1 = QLineEdit("File...")
        self.text_2 = QLineEdit("Color...")
        self.text_3 = QLineEdit("Font...")
        self.gridbox = QGridLayout(self)
        self.setupUI()
        self.show()

    def setupUI(self):
        self.gridbox.addWidget(self.button_1, 0, 0)
        self.gridbox.addWidget(self.button_2, 1, 0)
        self.gridbox.addWidget(self.button_3, 2, 0)
        self.gridbox.addWidget(self.text_1, 0, 1)
        self.gridbox.addWidget(self.text_2, 1, 1)
        self.gridbox.addWidget(self.text_3, 2, 1)

        self.connect(self.button_1, SIGNAL("clicked()"), self.slot_open_file_dialog)
        self.connect(self.button_2, SIGNAL("clicked()"), self.slot_select_color)
        self.connect(self.button_3, SIGNAL("clicked()"), self.slot_set_font)

    def slot_open_file_dialog(self):
        # 打开文件对话框
        # QWidget parent=None
        # QString caption=QString()
        # QString directory=QString()
        # QString filter=QString()
        # QString selectedFilter=None
        # QFileDialog.Options options=0
        # -> QString
        filename = QFileDialog.getOpenFileName(None, "open file", QDir.currentPath(),
                                               "*.py;;*.ui;;*.md;;all files(*)")
        self.text_1.setText(filename)

    def slot_select_color(self):
        # QColorDialog.getColor(QColor, QWidget, QString, QColorDialog.ColorDialogOptions options=0)
        # -> QColor
        color = QColorDialog.getColor(Qt.white)
        if color.isValid():
            self.setPalette(QPalette(color))

    def slot_set_font(self):
        # QFontDialog.getFont(QWidget parent=None)
        # -> (QFont, bool)
        qfont = QFontDialog.getFont()
        if qfont[1]:
            self.setFont(qfont[0])


app = QApplication(sys.argv)
dialog = StandardDialog()
sys.exit(app.exec_())
