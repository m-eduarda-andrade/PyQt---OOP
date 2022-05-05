import sys
import json
import time

from PyQt5.QtCore import QAbstractListModel, Qt, QSize, QTimer
from PyQt5.QtGui import QImage

from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QSpinBox,
    QMainWindow,
    QVBoxLayout,
    QDoubleSpinBox,
    QSlider,
    QListView, QPushButton, QLineEdit, QHBoxLayout, QLabel, QLayout

)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.button = QPushButton("Click me")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.counter = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

        self.button.clicked.connect(self.button_clicked)

    def timeout(self):
        self.counter += 1
        self.label.setText(f"Counter {self.counter}")

    def long_process(self):
        for _ in range(10):
            time.sleep(1)

    def button_clicked(self):
        self.long_process()
        self.button.setText("Done handling")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
