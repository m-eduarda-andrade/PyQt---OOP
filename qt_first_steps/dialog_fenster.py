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


# Leere Fenster -> make your own dialog
class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HELLO!")

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        message = QLabel("Something happened, is that OK?")

        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


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

        self.button_action = QAction(QIcon("qt-logo.svg"), "My button", self)
        self.button_action.setToolTip("This is my button")
        self.button_action.setStatusTip("This is my button")

        # Shortcut
        self.button_action.setShortcut("Ctrl+B")

        # button_action.setCheckable(True)
        self.button_action.triggered.connect(self.button_action_triggered)

        #Button 1

        self.button_action1 = QAction(QIcon("qt-logo.svg"), "My button 1", self)
        self.button_action1.setToolTip("This is my button 1")
        self.button_action1.setStatusTip("This is my button 1")

        # Shortcut alternative
        self.button_action1.setShortcut(Qt.CTRL + Qt.Key_D)

        # button_action.setCheckable(True)
        self.button_action1.triggered.connect(self.button_action_triggered)

        # put in toolbar
        self.toolbar.addAction(self.button_action)
        self.toolbar.addAction(self.button_action1)

        self.toolbar.addSeparator()

        self.toolbar.addWidget(QLabel("My Label"))
        self.toolbar.addWidget(QCheckBox())
        self.setStatusBar(QStatusBar(self))
        self.toolbar.setMovable(False)

        # Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")  # was macht das &-Zeichen?
        file_menu.addAction(self.button_action)  # die gleiche Action
        file_menu.addAction(self.button_action1)
        file_menu.addSeparator()
        other_action = QAction("My other action", self)
        file_menu.addAction(other_action)  # die neue Action

        # Untermenu
        submenu = file_menu.addMenu("Submenu")
        submenu.addAction(self.button_action)       ## THIS IS WRONG,DONT OUT TWICE THE SAME THING
        submenu.addAction(QAction("My new action", self))


        ##############################################################################

        # DIALOG FENSTER

        ##############################################################################
        button_dialog = QPushButton("Press me for a dialog!")
        button_dialog.clicked.connect(self.button_clicked)
        self.setCentralWidget(button_dialog)


        ###################################

        # Message

        ########################

    def button_clicked(self):
        dlg = QMessageBox(self)

        dlg.setWindowTitle("I have a question!")
        dlg.setText("This is a simple dialog")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Critical)
        response = dlg.exec_()
        # noch einfacher
        # button = QMessageBox.question(self, "I have a question!",
        # "This is a simple dialog")
        if response == QMessageBox.Yes:
            print("YES!")

    def button_clicked1(self):
        dlg = QMessageBox(self)

        dlg.setWindowTitle("I have a question!")
        dlg.setText("This is a simple dialog")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        response = dlg.exec_()
        # noch einfacher
        # button = QMessageBox.question(self, "I have a question!",
        # "This is a simple dialog")
        if response == QMessageBox.Yes:
            print("YES!")

    def button_clicked1(self):
        dlg = CustomDialog()  # parent ist das MainWindow, modal dafür
        if dlg.exec_():  # eine eigene Ereignisschleife startet
            print("Success")
        else:
            print("Canceled")

    def button_action_triggered(self):

        #self.sender() # says which object triggered this function
        if self.sender() == self.button_action:
            print("Button Action was triggered")
        else:
            print("Button 1 was triggered")
        print("clicked!")


# this does not work for all OS:
# windows and linux:
    # ok | cancel
# MacOS
    # cancel | ok



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()


