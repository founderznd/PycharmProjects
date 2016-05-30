# coding: utf-8
# 多文档的实现

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MultiWorkSpace(QMainWindow):
    def __init__(self):
        super(MultiWorkSpace, self).__init__()
        self.setWindowTitle(u"多文档窗口")

        self.create_menu()
        self.workspace = QWorkspace()
        self.workspace.cascade()
        self.setCentralWidget(self.workspace)
        self.slot_add_window()
        self.slot_add_window()
        self.slot_add_window()

    def create_menu(self):
        menu_bar = QMenuBar()

        window_menu = menu_bar.addMenu("window")
        new_action = window_menu.addAction("new")
        close_action = window_menu.addAction("closeAll")

        layout_menu = menu_bar.addMenu("layout")
        cascade_action = layout_menu.addAction("cascade")
        tile_action = layout_menu.addAction("tile")

        other_menu = menu_bar.addAction("others")

        self.setMenuBar(menu_bar)
        self.connect(new_action, SIGNAL("triggered()"), self.slot_add_window)
        self.connect(close_action, SIGNAL("triggered()"), self.slot_close_window)
        self.connect(cascade_action, SIGNAL("triggered()"), self.slot_cascade)
        self.connect(tile_action, SIGNAL("triggered()"), self.slot_tile)
        self.connect(other_menu, SIGNAL("triggered()"), self.slot_scroll)

    def slot_add_window(self):
        l = self.workspace.windowList(QWorkspace.CreationOrder)
        new_window = QMainWindow()
        new_window.setWindowTitle("window " + str(len(l)))
        edit = QTextEdit(new_window)
        new_window.setCentralWidget(edit)
        self.workspace.addWindow(new_window)
        new_window.show()

    def slot_close_window(self):
        self.workspace.closeAllWindows()

    def slot_cascade(self):
        self.workspace.cascade()

    def slot_tile(self):
        self.workspace.tile()

    def slot_scroll(self):
        self.workspace.setScrollBarsEnabled(not self.workspace.scrollBarsEnabled())
        self.workspace.activateNextWindow()


app = QApplication(sys.argv)
window = MultiWorkSpace()
window.show()
sys.exit(app.exec_())
