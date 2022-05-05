#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Maria Eduarda Costa Leite Andrade
# Created Date: 2021/11/23
# ---------------------------------------------------------------------------
""" Details about the module and for what purpose it was built for"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QVBoxLayout,    # vertical
    QHBoxLayout,    # horizontal
    QGridLayout,    # like a matrix
    QStackedLayout, # like a book, see only one widget
    QTabWidget,
    QFormLayout,    # like a form: name, birthdate, use "addRow(text, Widget)
    QDoubleSpinBox,
    QSlider,
    QSpinBox,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QLabel,
    QStatusBar,
    QAction,
    QToolBar,
)


class MainWindow(QMainWindow):
    """MainWindow is a class for supporting the GUI of this application."""
    def __init__(self):
        """__init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1 (str): Description of `param1`.
            param2 (:obj:`int`, optional): Description of `param2`. Multiple
                lines are supported.
            param3 (:obj:`list` of :obj:`str`): Description of `param3`.

        """
        super().__init__()

        # Window settings
        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))


        # MENU
        menu = self.menuBar()       # inbuilt from inheritance of QMainWindow
        file_menu = menu.addMenu("&File")  # was macht das &-Zeichen?
        edit_menu = menu.addMenu("&Edit")

        # Action
        self.button_action = QAction(QIcon("qt-logo.svg"), "My button", self)
        self.button_action.setToolTip("This is my button")
        self.button_action.setStatusTip("This is my button")
        #   Shortcut
        self.button_action.setShortcut("Ctrl+B")

        self.button_action1 = QAction(QIcon("qt-logo.svg"), "My button 1", self)
        #   Shortcut alternative
        self.button_action1.setShortcut(Qt.CTRL + Qt.Key_D)

        # Add actions
        file_menu.addAction(self.button_action)

        # Add separator
        file_menu.addSeparator()

        # Add actions
        file_menu.addAction(self.button_action1)

        # Submenu
        submenu = file_menu.addMenu("Submenu")
        submenu.addAction(self.button_action)  ## THIS IS WRONG,DONT OUT TWICE THE SAME THING
        submenu.addAction(QAction("My new action", self))


        # TOOLBAR
        self.toolbar = QToolBar("My Main Toolbar")
        self.addToolBar(self.toolbar)

        # same action as in menu
        self.button_action.setCheckable(True)
        # self.button_action.triggered.connect(self.button_action_triggered)
        self.toolbar.addAction(self.button_action)

        # add separator
        self.toolbar.addSeparator()

        # add widget
        self.toolbar.addWidget(QLabel("My Label"))
        self.toolbar.addWidget(QCheckBox())


        # WIDGETS
        self.button = QPushButton("Press me")
        self.line = QLineEdit()
        self.label = QLabel("This is a label")
        self.checkbox = QCheckBox()
        self.spinbox = QSpinBox()
        self.doublespin = QDoubleSpinBox()
        self.slider = QSlider()


        # LAYOUT
        self.layout = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
        self.stacked = QStackedLayout()
        self.tabs = QTabWidget()


        # CONTAINER
        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

    def add_widgets(self, *args):
        for w in args:
            self.layout.addWidget(w)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
