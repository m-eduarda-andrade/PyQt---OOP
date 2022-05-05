import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QSpinBox,
    QMainWindow,
    QVBoxLayout,
    QDoubleSpinBox,
    QSlider,
)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        # QSpinBox
        self.spinbox = QSpinBox()
        self.spinbox = QDoubleSpinBox()

        # Slider
        self.slider = QSlider()

        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setRange(-500,1000)


        # spinbox
        self.spinbox.setMinimum(0)
        self.spinbox.setMaximum(500)
        self.spinbox.setSuffix(" &")

        self.spinbox.setSingleStep(5)

        self.dspinbox.setRange(-100, 100)

        # signals
        self.spinbox.valueChanged.connect(print)

        self.slider.valueChanged.connect(print)

        # Layout
        layout = QVBoxLayout()  # vertical box
        layout.addWidget(self.spinbox)
        layout.addWidget(self.dspinbox)
        layout.addWidget(self.slider)

        # Container
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
