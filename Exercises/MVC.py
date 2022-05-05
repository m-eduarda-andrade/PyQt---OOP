import sys
import json

from PyQt5.QtCore import QAbstractListModel, Qt, QSize
from PyQt5.QtGui import QImage

from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QSpinBox,
    QMainWindow,
    QVBoxLayout,
    QDoubleSpinBox,
    QSlider,
    QListView, QPushButton, QLineEdit, QHBoxLayout

)


tick = QImage("tick.png")
tick.scaled(10, 10)


class TodoModel(QAbstractListModel):    # -> keine default habe, wir muessen definieren
    def __init__(self, todos=None):
        super().__init__()
        # unser "Data Store": [(bool, str), (bool, str), ..]
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            status, text = self.todos[index.row()]

            return text

        elif role == Qt.DecorationRole:
            status, text = self.todos[index.row()]
            if status:
                return tick

        elif role == Qt.ToolTipRole:
            status, text = self.todos[index.row()]
            return f"{text.split()[0]} - status"

    def rowCount(self, index):
        return len(self.todos)

    def add_row(self, text):
        self.todos.append((False, text))
        self.layoutChanged.emit()

    def delete_row(self, index):
        self.todos.pop(index.row())
        self.layoutChanged.emit()

    def complete_row(self, index):
        _, text = self.todos[index.row()]
        self.todos[index.row()] = (True, text)
        self.dataChanged.emit(index, index)     # welche Daten haben sich geaendert

    def load(self):
        try:
            with open("data.json", "r") as f:       # outside here the file is already closed
                self.todos = json.load(f)
        except Exception as e:
            print(str(e))

    def save(self):
        with open("data.json", "w") as f:
            json.dump(self.todos, f)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My TODO List")

        # WIDGETS

        self.list = QListView()
        self.loschen = QPushButton("Loeschen")
        self.erledigen = QPushButton("Erledigen")
        self.line = QLineEdit()
        self.add_button = QPushButton("Hinzufuegen")

        self.model = TodoModel()  # mit einer leeren Todo-Liste
        todos = [(False, 'Milch einkaufen'), (False, 'Skript hochladen')]
        self.model = TodoModel(todos)  # mit einer vorgefertigten Liste
        self.list.setModel(self.model)

        # Signals
        self.add_button.clicked.connect(self.add)
        self.loschen.clicked.connect(self.delete)
        self.erledigen.clicked.connect(self.complete)

        # Layout
        self.layout = QVBoxLayout()  # vertical box
        self.hbox = QHBoxLayout()  # vertical box
        self.layout.addWidget(self.list)
        self.hbox.addWidget(self.loschen)
        self.hbox.addWidget(self.erledigen)
        self.layout.addLayout(self.hbox)
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.add_button)

        # Container
        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

    def add(self):
        text = self.line.text().strip()
        if text:
            self.model.add_row(text)
            self.line.setText("")
            self.model.save()

    def delete(self):
        idx = self.list.selectedIndexes()[0]
        if idx:
            self.model.delete_row(idx)
            self.list.clearSelection()
            self.model.save()

    def complete(self):
        idx = self.list.selectedIndexes()[0]
        if idx:
            self.model.complete_row(idx)
            self.list.clearSelection()
            self.model.save()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
