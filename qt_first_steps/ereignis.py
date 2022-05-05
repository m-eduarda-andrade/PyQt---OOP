import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QSpinBox,
    QMainWindow,
    QVBoxLayout,
    QDoubleSpinBox,
    QLabel,
    QPushButton,
)


class MyButton(QPushButton):
    def mousePressEvent(self, e):
        e.ignore()  # the event is ignored by button and propragate to the main WIndow and the main window must handle it
                    # so the button is kind of not clickable anymore


class MyLabel(QLabel):
    clicked = pyqtSignal(int)       # you can emit data as well

    def mouseReleaseEvent(self, event):
        self.clicked.emit(event.button())        # data emitted
        super().mouseReleaseEvent(event)    # to act like how the class would handle this mouse event itelf, call how QLabel would handle

        # when accept: the widget decide what to do
        # when ignore: the widget decide what to do, is this is chose, it is propagated


class MainWindow(QMainWindow):
    # overwriting function from QMainWindow
    def __init__(self):
        super().__init__()
        self.label = MyLabel("Click in this window")
        self.layout = QVBoxLayout()

        self.button = MyButton("Push Me")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.label.clicked.connect(self.label_clicked)

        # self.setMouseTracking(True)
        # self.label.setMouseTracking(True)

    # overwriting function from QMainWindow (ueberladen)
    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        print(e.globalPos())    # relative to desktop
        print(e.button())       # e.button == Qt.LeftButton
        if e.button == Qt.LeftButton:
            self.label.setText("mousePressEvent")

    def mouseReleaseEvent(self, e):
        print(e.pos(), "\n")      # relative to window
        self.label.setText("mouseReleaseEvent")

    def mouseDoubleClickEvent(self, e):
        print(e.pos())
        self.label.setText("mouseDoubleClickEvent")

    def label_clicked(self, i):
        button = {Qt.RightButton: "Right", Qt.LeftButton: "Left"}.get(i, "unknown")

        print("Button clicked: ", button, "\n")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
