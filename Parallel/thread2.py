import sys
import json
import time

from PyQt5.QtCore import QAbstractListModel, Qt, QSize, QTimer, QThreadPool, QRunnable, pyqtSignal, QObject
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


class SignalEmitter(QObject):
    failed = pyqtSignal(Exception)
    finished = pyqtSignal(object)


class Worker(QRunnable):
    def __init__(self, name = None, iterations=12):
        super(Worker, self).__init__()

        self.name = name
        self.emitter = SignalEmitter()
        self.iterations = iterations
        self.result = 0

    def run(self):
        try:
            for i in range(self.iterations):
                time.sleep(1)
                self.result += i/(11-i)
                print(f"{self.name}: calculated {self.result}")

        except Exception as e:
            self.emitter.failed.emit(e)
        else:
            self.emitter.finished.emit(self.result)


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
        worker.emitter.finished.connect(self.worker_finished)
        worker.emitter.failed.connect(self.worker_failed)
        self.worker_count += 1
        self.threadpool.start(worker)
        self.button.setText("Done handling")

    def worker_finished(self, r):
        print("Worker finished: result: ", r)

    def worker_failed(self, e):
        print("Worker failed: exception: ", str(e))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
