import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QListWidget,
)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        # QLabel and QComboBox definiert
        self.label = QLabel()
        self.list = QListWidget()

        # Settings: select more than one element at a time
        # with ctrl select multiple
        # with shift select all*
        self.list.setSelectionMode(QListWidget.ExtendedSelection)

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

        # List: add items
        self.list.addItems(self.text_alignments.keys())

        # signal
        self.list.currentTextChanged.connect(self.list_s_changed)
        self.list.itemSelectionChanged.connect(self.item_select_changed)


        # Layout
        layout = QVBoxLayout()  # vertical box
        layout.addWidget(self.label)
        layout.addWidget(self.list)

        # Container
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def list_s_changed(self, s):
        # put a get to set default
        self.label.setAlignment(self.text_alignments[s])

    def item_select_changed(self):
        print("changed")

        # print only the object
        # print(self.list.selectedItems())

        # print the text of object
        texts = [i.text() for i in self.list.selectedItems()]
        print(texts)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
