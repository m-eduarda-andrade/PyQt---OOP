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

        button_action = QAction(QIcon("qt-logo.svg"), "My button", self)
        button_action.setToolTip("This is my button")
        button_action.setStatusTip("This is my button")
        button_action.setCheckable(True)
        button_action.triggered.connect(self.button_action_triggered)
        self.toolbar.addAction(button_action)

        self.toolbar.addSeparator()

        self.toolbar.addWidget(QLabel("My Label"))
        self.toolbar.addWidget(QCheckBox())
        self.setStatusBar(QStatusBar(self))

    def button_action_triggered(self):
        print("clicked!")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()


