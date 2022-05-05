import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        self.label = QLabel()
        self.label.setPixmap(QPixmap('qt-logo.svg'))

        layout = QVBoxLayout()  # vertical box
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
