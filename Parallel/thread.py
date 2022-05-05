import sys
import json
import time

from PyQt5.QtCore import QAbstractListModel, Qt, QSize, QTimer, QThreadPool, QRunnable
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


class Worker(QRunnable):
    def __init__(self, name = None):
        super(Worker, self).__init__()

        self.name = name
    def run(self):
        for _ in range(10):
            print(f"Worker {self.name} sleeping for one more second")
            time.sleep(1)

        print(f"Worker {self.name}: work done!")


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

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(3)

        self.worker_count = 0


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
        worker = Worker()
        self.worker_counter += 1
        self.threadpool.start(worker)
        self.button.setText("Done handling")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
