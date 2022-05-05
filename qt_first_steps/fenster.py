'''
date: today
author:

'what I want to acompplish with this exercise'
'''

import sys

from time import sleep

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QSpinBox,
    QMainWindow,
    QVBoxLayout,    # vertical
    QMessageBox,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QLabel,
    QStatusBar,
    QAction,
    QToolBar,
    QDialogButtonBox,
    QDialog,

)


class AnotherWindow(QWidget): # oder QMainWindow wenn Sie wollen
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        # define all atributes in __init__
        super().__init__()

        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        self.setCentralWidget(QLabel("Hello"))
        self.toolbar = QToolBar("My Main Toolbar")
        self.addToolBar(self.toolbar)


        self.toolbar.addWidget(QLabel("My Label"))
        self.toolbar.addWidget(QCheckBox())
        self.setStatusBar(QStatusBar(self))
        self.toolbar.setMovable(False)

        # Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")  # was macht das &-Zeichen?
        file_menu.addSeparator()
        other_action = QAction("My other action", self)


        ##############################################################################

        # FENSTER -> it is not modal, you can alternate between the windows

        # widget without parent, is a window

        ##############################################################################

        self.button = QPushButton("Push for Window")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.show_new_window)
        self.w = AnotherWindow()    # save with self, otherwise the garbage collector will del it

        self.input = QLineEdit()
        self.input.textChanged.connect(self.w.label.setText)
        vbox = QVBoxLayout()
        vbox.addWidget(self.button)
        vbox.addWidget(self.input)
        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)


    def show_new_window(self, checked):
        if checked:
            self.w.show()

        else:
            self.w.hide()


# this does not work for all OS:
# windows and linux:
    # ok | cancel
# MacOS
    # cancel | ok



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()


