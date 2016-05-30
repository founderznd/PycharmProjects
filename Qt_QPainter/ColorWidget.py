# coding:utf-8
# 利用QPalette改变控件颜色

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ColorWidget(QWidget):
    def __init__(self):
        super(ColorWidget, self).__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)

        self.left = self.left_widget()
        self.right = self.right_widget()

        self.layout.addWidget(self.left)
        self.layout.addWidget(self.right)

    def left_widget(self):
        widget = QWidget()
        flayout = QFormLayout(widget)

        self.window_combo = self.fill_color_list()
        flayout.addRow("QPalette.Window:", self.window_combo)
        self.connect(self.window_combo, SIGNAL("activated(int)"), self.slot_window)

        self.windowtext_combo = self.fill_color_list()
        flayout.addRow("QPalette.WindowText:", self.windowtext_combo)
        self.connect(self.windowtext_combo, SIGNAL("activated(int)"), self.slot_windowtext)

        self.button_combo = self.fill_color_list()
        flayout.addRow("QPalette.Button:", self.button_combo)
        self.connect(self.button_combo, SIGNAL("activated(int)"), self.slot_button)

        self.buttontext_combo = self.fill_color_list()
        flayout.addRow("QPalette.ButtonText:", self.buttontext_combo)
        self.connect(self.buttontext_combo, SIGNAL("activated(int)"), self.slot_buttontext)

        self.base_combo = self.fill_color_list()
        flayout.addRow("QPalette.Base:", self.base_combo)
        self.connect(self.base_combo, SIGNAL("activated(int)"), self.slot_base)

        return widget

    def right_widget(self):
        widget = QWidget()
        widget.setAutoFillBackground(True)
        vbox = QVBoxLayout(widget)
        hbox1 = QHBoxLayout()
        label = QLabel("Please select a value")
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        hbox1.addWidget(label)
        combo = QComboBox()
        combo.addItems(["1", "2", "3"])
        hbox1.addWidget(combo)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Please input a string"))
        hbox2.addWidget(QLineEdit())
        vbox.addLayout(hbox2)

        self.text = QTextEdit()
        vbox.addWidget(self.text)

        hbox3 = QHBoxLayout()
        hbox3.addStretch()
        self.button_1 = QPushButton("OK")
        hbox3.addWidget(self.button_1)
        hbox3.addWidget(QPushButton("Cancel"))
        vbox.addLayout(hbox3)

        return widget

    def fill_color_list(self):
        combo = QComboBox()
        color_list = QColor.colorNames()

        for color in color_list:
            pix = QPixmap(QSize(18, 18))
            pix.fill(QColor(color))
            combo.addItem(QIcon(pix), color)
            combo.setIconSize(pix.size())
            combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        return combo

    def slot_window(self):
        p = self.right.palette()
        p.setColor(QPalette.Window, QColor(self.window_combo.currentText()))
        self.right.setPalette(p)
        self.text.setText(self.window_combo.currentText())

    def slot_windowtext(self):
        p = self.right.palette()
        p.setColor(QPalette.WindowText, QColor(self.windowtext_combo.currentText()))
        self.right.setPalette(p)
        pass

    def slot_button(self):
        p = self.right.palette()
        p.setColor(QPalette.Button, QColor(self.button_combo.currentText()))
        self.right.setPalette(p)
        pass

    def slot_buttontext(self):
        p = self.right.palette()
        p.setColor(QPalette.ButtonText, QColor(self.buttontext_combo.currentText()))
        self.right.setPalette(p)
        pass

    def slot_base(self):
        p = self.right.palette()
        p.setColor(QPalette.Base, QColor(self.base_combo.currentText()))
        self.right.setPalette(p)
        pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = ColorWidget()
    widget.show()
    sys.exit(app.exec_())
