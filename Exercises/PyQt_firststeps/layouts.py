import sys

from time import sleep

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
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
    QSplitter,
)

# flow layout (put until there is space in the same line, then goes to next)


# sometime when you put several verticals and horizontals together, it gets messy, so a gridLayout would be better

class MainWindow(QMainWindow):
    def __init__(self):
        # define all attributes in __init__
        super().__init__()

        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        # Widgets
        self.button = QPushButton("Press me")
        self.line = QLineEdit()
        self.label = QLabel("This is a label")
        self.checkbox = QCheckBox()

        # Layout
        self.layout = QHBoxLayout()  # vertical box
        self.vbox = QVBoxLayout()

        self.add_widgets(self.button, self.line, self.label, self.checkbox)

        # set in HBox
        self.vbox.addWidget(QLabel("Some Label"))
        self.vbox.addLayout(self.layout)
        self.vbox.addWidget(QLabel("Some Other Label"))

        # Container, because layout is abstract, so it must be able to show
        container = QWidget()   # must put the layout in a widget so you can show it. layout is abstract
        container.setLayout(self.vbox)
        self.setCentralWidget(container)

    def add_widgets(self, *args):
        for w in args:
            self.layout.addWidget(w)


class MainWindow2(QMainWindow):
    def __init__(self):
        # define all atributes in __init__
        super().__init__()

        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        # Widgets
        self.button = QPushButton("Press me")
        self.line = QLineEdit()
        self.label = QLabel("This is a label")
        self.checkbox = QCheckBox()

        '''
        # whitout grid
        # Layout
        self.vbox1 = QVBoxLayout()  # vertical box
        self.vbox2 = QVBoxLayout()
        self.hbox = QHBoxLayout()
        
        self.vbox1.addWidget(self.button)
        self.vbox1.addWidget(self.line)
        self.vbox2.addWidget(self.label)
        self.vbox2.addWidget(self.checkbox)
        
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        '''

        self.grid = QGridLayout()
        self.grid.addWidget(self.button, 0, 0)
        self.grid.addWidget(self.line, 1, 0)
        self.grid.addWidget(self.label, 0, 1)
        # self.grid.addWidget(QSplitter(), 2, 2)
        self.grid.addWidget(self.checkbox, 5, 5)


        # Container, because layout is abstract, so it must be able to show
        container = QWidget()  # must put the layout in a widget so you can show it. layout is abstract
        container.setLayout(self.grid)
        self.setCentralWidget(container)


class MainWindow3(QMainWindow):
    def __init__(self):
        # define all atributes in __init__
        super().__init__()

        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        # Widgets
        self.button = QPushButton("Press me")
        self.line = QLineEdit()
        self.label = QLabel("This is a label")
        self.checkbox = QCheckBox()

        self.stacked = QStackedLayout()
        self.stacked.addWidget(self.button)
        self.stacked.addWidget(self.line)
        self.stacked.addWidget(self.label)
        self.stacked.addWidget(self.checkbox)

        self.hbox = QHBoxLayout()
        self.b1 = QPushButton("Button")
        self.b2 = QPushButton("Line")
        self.b3 = QPushButton("Label")
        self.b4 = QPushButton("Checkbox")
        self.hbox.addWidget(self.b1)
        self.hbox.addWidget(self.b2)
        self.hbox.addWidget(self.b3)
        self.hbox.addWidget(self.b4)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.stacked)

        self.b1.clicked.connect(self.change_b1)
        self.b2.clicked.connect(self.change_b2)
        self.b3.clicked.connect(self.change_b3)
        self.b4.clicked.connect(self.change_b4)


        self.stacked.setCurrentIndex(3)


        # Container, because layout is abstract, so it must be able to show
        container = QWidget()  # must put the layout in a widget so you can show it. layout is abstract
        container.setLayout(self.vbox)
        self.setCentralWidget(container)

    def change_b1(self):
        self.stacked.setCurrentWidget(self.button)

    def change_b2(self):
        self.stacked.setCurrentWidget(self.line)

    def change_b3(self):
        self.stacked.setCurrentWidget(self.label)

    def change_b4(self):
        self.stacked.setCurrentWidget(self.checkbox)


class MainWindow4(QMainWindow):
    def __init__(self):
        # define all atributes in __init__
        super().__init__()

        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        # Widgets
        self.button = QPushButton("Press me")
        self.line = QLineEdit()
        self.label = QLabel("This is a label")
        self.checkbox = QCheckBox()

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.setMovable(True)

        self.tabs.addTab(self.button, "Button")
        self.tabs.addTab(self.line, "Line Edit")
        self.tabs.addTab(self.label, "Label")
        self.tabs.addTab(self.checkbox, "Checkbox")

        # Container, because layout is abstract, so it must be able to show
        # container = QWidget()  # must put the layout in a widget so you can show it. layout is abstract
        # container.setLayout(self.grid)
        self.setCentralWidget(self.tabs)


app = QApplication(sys.argv)
window = MainWindow3()
window.show()
app.exec_()
