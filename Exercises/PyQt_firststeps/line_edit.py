import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QListWidget,
    QTextEdit,
)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        # QLineEdit
        self.line = QLineEdit()
        self.text = QTextEdit()

        # settings
        # self.line.setPlaceholderText("Hey tehre")
        # self.line.inputMask(###.###.###;c)
        self.line.returnPressed.connect(self.return_pressed)
        self.line.selectionChanged.connect(print)




        # Layout
        layout = QVBoxLayout()  # vertical box
        layout.addWidget(self.line)
        layout.addWidget(self.text)

        # Container
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def return_pressed(self):
        print("hey")

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
