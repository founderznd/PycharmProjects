# coding:utf-8
# Delegate

from PyQt4.QtGui import *


class DateDelegate(QItemDelegate):
    def __init__(self):
        super(DateDelegate, self).__init__()

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        pass

    def setEditorData(self, QWidget, QModelIndex):
        pass

    def setModelData(self, QWidget, QAbstractItemModel, QModelIndex):
        pass

    def updateEditorGeometry(self, QWidget, QStyleOptionViewItem, QModelIndex):
        pass


