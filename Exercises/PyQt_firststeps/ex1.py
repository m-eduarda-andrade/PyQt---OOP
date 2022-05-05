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
    QCheckBox,
    QComboBox,
)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        # QLabel and QComboBox definiert
        self.label = QLabel()
        self.combobox = QComboBox()

        # dict definiert

        self.text_alignments = {
            "Right": Qt.AlignRight,
            "Left": Qt.AlignLeft,
            "Top": Qt.AlignTop,
            "Bottom": Qt.AlignBottom,
            "HCenter": Qt.AlignHCenter,
            "VCenter": Qt.AlignVCenter,
        }

        # set text from Label
        self.label.setText("Hallo")

        # ComboBox: add items
        self.combobox.addItems(self.text_alignments.keys())

        # signal
        self.combobox.currentTextChanged.connect(self.combo_s_changed)


        # Layout
        layout = QVBoxLayout()  # vertical box
        layout.addWidget(self.label)
        layout.addWidget(self.combobox)

        # Container
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def combo_s_changed(self, s):
        # put a get to set default
        self.label.setAlignment(self.text_alignments[s])


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
