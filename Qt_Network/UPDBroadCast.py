# coding:utf-8
# 基于UDP的网络广播程序

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *


class UdpServer(QDialog):
    def __init__(self):
        super(UdpServer, self).__init__()
        self.setWindowTitle("UDP Server")

        vbox = QVBoxLayout(self)

        vbox.addWidget(QLabel("Timer:"))

        self.line = QLineEdit()
        vbox.addWidget(self.line)

        self.startbutton = QPushButton("Start")
        vbox.addWidget(self.startbutton)

        self.connect(self.startbutton, SIGNAL("clicked()"), self.slotStart)

        self.port = 5555
        self.isStarted = False
        self.udpSocket = QUdpSocket()

        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.timeout)

    def slotStart(self):
        if self.isStarted:
            self.timer.stop()
        else:
            self.timer.start(1000)
        self.isStarted = not self.isStarted

    def timeout(self):
        msg = self.line.text()
        if msg == "":
            return
        length = self.udpSocket.writeDatagram(msg, QHostAddress.Broadcast, self.port)

        if length != len(msg):
            return


class UdpClient(QDialog):
    def __init__(self):
        super(UdpClient, self).__init__()
        self.setWindowTitle("UDP Client")

        vbox = QVBoxLayout(self)

        self.text = QTextEdit()
        vbox.addWidget(self.text)

        closebutton = QPushButton("close")
        vbox.addWidget(closebutton)

        self.connect(closebutton, SIGNAL("clicked()"), self.close)

        self.udpSocket = QUdpSocket()

        self.port = 5555

        # 第二个参数决定了是否支持多客户端，默认只支持单客户端
        result = self.udpSocket.bind(self.port, QUdpSocket.ShareAddress)
        if result is False:
            QMessageBox.information(None, "error", "udp socket create error!")
            return
        self.connect(self.udpSocket, SIGNAL("readyRead()"), self.datareceive)

    def datareceive(self):
        while self.udpSocket.hasPendingDatagrams():
            s = self.udpSocket.pendingDatagramSize()
            datagram = self.udpSocket.readDatagram(s)
            msg = datagram[0]
            self.text.insertPlainText(msg)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    server = UdpServer()
    server.show()
    client = UdpClient()
    client.show()

    sys.exit(app.exec_())
