# coding:utf-8

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        QThread.sleep(3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pixmap = QPixmap("image/mario.png")
    splash = QSplashScreen(pixmap.scaled(600, 600))
    splash.show()
    app.processEvents()
    # 如果不加这一句，有时候不会显示图片
    splash.showMessage("")
    window = MyWidget()
    window.show()
    splash.finish(window)

    sys.exit(app.exec_())
