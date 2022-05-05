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

        # QLabel
        self.input = QLineEdit()
        self.label = QLabel()

        f = self.label.font()

        f.setPixelSize(50)

        self.label.setFont(f)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        self.input.textEdited.connect(lambda text: self.label.setText(f"{text}"))

        # QCheckBox

        self.checkbox = QCheckBox("This is a checkbox")
        self.checkbox.setChecked(Qt.Checked)
        self.checkbox.stateChanged.connect(self.cb_state_changed)

        # ComboBox

        self.combobox = QComboBox()
        self.combobox.addItems(["One", "Two", "Three"])
        self.combobox.currentIndexChanged.connect(self.combo_i_changed)
        self.combobox.currentTextChanged.connect(self.combo_s_changed)


        # Layout
        layout = QVBoxLayout()  # vertical box
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.combobox)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def cb_state_changed(self, state):
        self.input.setEnabled(state == Qt.Checked) # pythonic
        '''
        if state == Qt.Checked:
            print("Checked")
            self.label.setAlignment(Qt.AlignRight)
        else:
            self.label.setAlignment(Qt.AlignLeft)
        '''
    def combo_i_changed(self, i):
        print("New index:", i)

    def combo_s_changed(self, s):
        print("New text is: ", s)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
