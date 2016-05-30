# coding:utf-8
# 实现电子钟

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DigiClock(QLCDNumber):
    def __init__(self):
        super(DigiClock, self).__init__()

        p = QPalette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.showColon = True
        self.dragPos = None

        # 显示的位数
        self.setDigitCount(8)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.5)

        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), self.showTime)

        timer.start(1000)  # 以1000毫秒为周期启动定时器

        self.showTime()

        self.resize(150, 60)

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString("hh:mm:ss")

        if self.showColon:
            text.replace(5, 1, ":")
            self.showColon = False
        else:
            text.replace(5, 1, " ")
            self.showColon = True

        self.display(text)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # 记录鼠标与窗口左上角的相对位移
            self.dragPos = e.globalPos() - self.frameGeometry().topLeft()
            e.accept()

        if e.button() == Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            # 位移函数默认鼠标在窗口的左上角，为了保持鼠标与窗口的相对位置，所以要减去位移量
            self.move(e.globalPos() - self.dragPos)
            e.accept()


import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DigiClock()
    widget.show()
    sys.exit(app.exec_())
