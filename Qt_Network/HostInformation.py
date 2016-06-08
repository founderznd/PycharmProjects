# coding:utf-8
# 获取本机网络信息

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *


class NetworkInformation(QWidget):
    def __init__(self):
        super(NetworkInformation, self).__init__()
        layout = QFormLayout(self)

        self.hostname = QLineEdit()
        layout.addRow(QLabel("Host Name:"), self.hostname)

        self.ip = QLineEdit()
        layout.addRow(QLabel("IP Adress:"), self.ip)

        detail = QPushButton("Detail")
        layout.addRow(detail)
        self.getHostInformations()
        self.connect(detail, SIGNAL("clicked()"), self.slotDetail)

    def getHostInformations(self):
        localhostname = QHostInfo.localHostName()
        self.hostname.setText(localhostname)

        hostinfo = QHostInfo.fromName(localhostname)
        addresses = hostinfo.addresses()
        if addresses:
            self.ip.setText(addresses[0].toString())

    def slotDetail(self):
        l = QNetworkInterface.allInterfaces()
        detail = QString()

        for i in range(len(l)):
            interface = l[i]
            detail.append("Device:" + interface.name() + "\n")
            detail.append("HardwareAddress:" + interface.hardwareAddress() + "\n")
            entrylist = interface.addressEntries()
            for j in range(len(entrylist)):
                entry = entrylist[j]
                detail.append("\t" + "IP Address:" + entry.ip().toString() + "\n")
                detail.append("\t" + "Netmask:" + entry.netmask().toString() + "\n")
                detail.append("\t" + "Broadcast:" + entry.broadcast().toString() + "\n")

        QMessageBox.information(None, "Detail", detail)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = NetworkInformation()
    widget.show()
    sys.exit(app.exec_())
