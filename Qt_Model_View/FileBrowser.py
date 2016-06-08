# coding:utf-8
# 文件目录浏览器


from PyQt4.QtCore import *
from PyQt4.QtGui import *

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    model = QDirModel()

    list = QListView()
    tree = QTreeView()
    table = QTableView()

    tree.setModel(model)
    list.setModel(model)
    table.setModel(model)

    tree.setSelectionMode(QAbstractItemView.MultiSelection)
    list.setSelectionMode(tree.selectionMode())
    table.setSelectionMode(tree.selectionMode())

    app.connect(tree, SIGNAL("doubleClicked(QModelIndex)"), list.setRootIndex)
    app.connect(tree, SIGNAL("doubleClicked(QModelIndex)"), table.setRootIndex)

    splitter = QSplitter()
    splitter.setFixedSize(800, 600)

    splitter.addWidget(tree)
    splitter.addWidget(list)
    splitter.addWidget(table)

    splitter.setWindowTitle("Model/View")
    splitter.show()

    sys.exit(app.exec_())
