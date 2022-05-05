import sys
# from PyQt5 import QtWidgets as qw # besser als *

from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")


        layout = QVBoxLayout()  # vertical box

        widgets = [
            QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox,
            QFontComboBox, QLCDNumber, QLabel, QLineEdit, QProgressDialog, QPushButton,
            QRadioButton, QSlider, QSpinBox, QTimeEdit, QMessageBox, QFileDialog
        ]

        for w in widgets:
            layout.addWidget(w())

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
