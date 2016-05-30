# coding:utf-8
# 综合布局实例
# 实现淡如淡出效果

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.central_widget = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.central_widget)

        left_dict = self.left_init()
        stacked_dict = self.right_init()

        self.faderWidget = None
        self.stack = stacked_dict["stack"]

        self.connect(left_dict["widget"], SIGNAL("currentRowChanged(int)"), stacked_dict["stack"].setCurrentIndex)
        self.connect(stacked_dict["button_2"], SIGNAL("clicked()"), self.close)
        self.connect(self.stack, SIGNAL("currentChanged(int)"), self.fadeInWidget)

    def left_init(self):
        left_widget = QListWidget()
        left_widget.addItems([u"个人基本资料", u"联系方式", u"详细资料"])
        self.central_widget.addWidget(left_widget)
        return {"widget": left_widget}

    def right_init(self):
        right_widget = QWidget()
        vbox = QVBoxLayout(right_widget)

        stacked_widget = QStackedWidget()
        stacked_widget.addWidget(self.init_base_info())
        stacked_widget.addWidget(self.init_contact_info())
        stacked_widget.addWidget(self.init_detail_info())

        form_layout = QHBoxLayout()
        form_layout.addStretch()
        button_1 = QPushButton(u"修改")
        button_2 = QPushButton(u"关闭")
        form_layout.addWidget(button_1)
        form_layout.addWidget(button_2)

        vbox.addWidget(stacked_widget)
        vbox.addLayout(form_layout)
        self.central_widget.addWidget(right_widget)
        return {"stack": stacked_widget, "button_1": button_1, "button_2": button_2}

    def init_base_info(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setMargin(20)
        layout.setSpacing(10)

        form_layout = QFormLayout()

        form_layout.addRow(u"用户名: ", QLineEdit())

        form_layout.addRow(u"姓名: ", QLineEdit())

        combobox = QComboBox()
        combobox.addItems([u"男", u"女"])
        form_layout.addRow(u"性别: ", combobox)

        form_layout.addRow(u"部门：", QTextEdit())

        form_layout.addRow(u"年龄：", QLineEdit())

        label = QLabel(u"备注: ")
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        form_layout.addRow(label)

        vbox_layout = QVBoxLayout()
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(QLabel(u"头像："))

        label = QLabel()
        pic = QPixmap("image/male_pic.png").scaled(50, 50)
        label.setPixmap(pic)

        hbox_layout.addWidget(label)
        hbox_layout.addWidget(QPushButton(u"更改"))

        vbox_layout.addLayout(hbox_layout)

        vbox_layout.addWidget(QLabel(u"个人说明："))

        vbox_layout.addWidget(QTextEdit())

        layout.addLayout(form_layout)
        layout.addLayout(vbox_layout)
        return widget

    def init_contact_info(self):
        widget = QWidget()

        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel(u"电子邮件："), 0, 0)
        grid_layout.addWidget(QLineEdit(), 0, 1)
        grid_layout.addWidget(QLabel(u"联系地址："), 1, 0)
        grid_layout.addWidget(QLineEdit(), 1, 1)
        grid_layout.addWidget(QLabel(u"邮政编码："), 2, 0)
        grid_layout.addWidget(QLineEdit(), 2, 1)
        grid_layout.addWidget(QLabel(u"移动电话："), 3, 0)
        grid_layout.addWidget(QLineEdit(), 3, 1)
        grid_layout.addWidget(QCheckBox(u"接受留言"), 3, 2)
        grid_layout.addWidget(QLabel(u"办公电话："), 4, 0)
        grid_layout.addWidget(QLineEdit(), 4, 1)

        widget.setLayout(grid_layout)
        return widget

    def init_detail_info(self):
        widget = QWidget()

        form_layout = QFormLayout()

        combo1 = QComboBox()
        combo1.addItems(["china", "USA", "Germany"])
        form_layout.addRow(u"国家/地区：", combo1)

        combo2 = QComboBox()
        combo2.addItems(["ChongQing", "JiangShu", "BeiJing", "ShangHai"])
        form_layout.addRow(u"省份：", combo2)

        form_layout.addRow(u"城市：", QLineEdit())

        form_layout.addRow(u"个人说明：", QTextEdit())

        widget.setLayout(form_layout)
        return widget

    def fadeInWidget(self, index):
        faderWidget = FaderWidget(self.stack.widget(index))
        faderWidget.start()


# 淡入淡出
class FaderWidget(QWidget):
    def __init__(self, parent):
        super(FaderWidget, self).__init__(parent)

        if parent:
            self.start_color = parent.palette().window().color()
        else:
            self.start_color = Qt.white

        self.currentAlpha = 0
        self.duration = 1000
        self.timer = QTimer(self)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(parent.size())
        self.connect(self.timer, SIGNAL("timeout()"), self.update)

    def start(self):
        self.currentAlpha = 255
        self.timer.start(100)
        self.show()

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        semiTransparentColor = self.start_color
        semiTransparentColor.setAlpha(self.currentAlpha)
        painter.fillRect(self.rect(), semiTransparentColor)
        self.currentAlpha -= (255 * self.timer.interval() / self.duration)

        if self.currentAlpha <= 0:
            self.timer.stop()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
