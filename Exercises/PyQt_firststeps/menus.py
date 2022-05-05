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
    QHBoxLayout,    # horizontal
    QGridLayout,    # like a matrix
    QStackedLayout, # like a book, see only one widget
    QTabWidget,
    QFormLayout,    # like a form: name, birthdate, use "addRow(text, Widget)"
    QDoubleSpinBox,
    QSlider,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QLabel,
    QStatusBar,
    QAction,
    QToolBar,
)


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



    def button_action_triggered(self):

        #self.sender() # says which object triggered this function
        if self.sender() == self.button_action:
            print("Button Action was triggered")
        else:
            print("Button 1 was triggered")
        print("clicked!")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()


