import math

from pyqtgraph import examples

examples.run()
import re
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication, QVBoxLayout, QLineEdit, QPushButton, QWidget, QLabel

)
import pyqtgraph as pg  # PyQtGraph nach Qt importieren
from numpy.random import randint


class My(QLabel):
    clicked = pyqtSignal(int)       # you can emit data as well

    def mouseReleaseEvent(self, event):
        self.clicked.emit(event.button())        # data emitted
        super().mouseReleaseEvent(event)    # to act like how the class would handle this mouse event itelf, call how QLabel would handle

        # when accept: the widget decide what to do
        # when ignore: the widget decide what to do, is this is chose, it is propagated



class Main1(QMainWindow):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label = QLabel("hey")
        self.line = QLineEdit()
        self.button = QPushButton("Send data")

        # signals
        #self.line.textEdited.connect(self.validade_data)
        self.button.clicked.connect(self.send_data)



        # Plot window
        self.plot_widget = pg.PlotWidget(name="graph1")
        self.plot_widget.mouseReleaseEvent(ev)

        # layout
        self.layout.addWidget(self.plot_widget)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.button)

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

    def send_data(self):
        numbers = self.line.text().split()
        numbers = [float(i.strip()) for i in numbers]

        x = list(range(len(numbers)))
        y = numbers

        self.plot_widget.plot(x, y, pen=pg.mkPen(width=2))

    def validate_data(self):
        pass
        #check = re.match("[/d]")


    def mouseReleaseEvent(self, ev):
        self.label.setText(self.plot_widget.objectName())



class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label = QLabel("hey")

        # Plot window
        sin = list()
        cos = list()
        tan = list()

        for i in range(600):
            sin.append(math.sin(i/10))
            cos.append(math.cos(i / 10))
            tan.append(math.tan(i / 10))

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.plot()

        # layout
        self.layout.addWidget(self.plot_widget)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.button)

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

    def send_data(self):
        numbers = self.line.text().split()
        numbers = [float(i.strip()) for i in numbers]

        x = list(range(len(numbers)))
        y = numbers

        self.plot_widget.plot(x, y, pen=pg.mkPen(width=2))

    def validate_data(self):
        pass
        #check = re.match("[/d]")


    def mouseReleaseEvent(self, ev):
        self.label.setText(self.plot_widget.objectName())



if __name__ == "__main__":
    app = QApplication([])
    window = Main()
    window.show()
    app.exec_()


