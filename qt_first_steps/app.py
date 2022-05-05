import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.button = QPushButton("Press me!")
        self.button.setCheckable(True)
        # button.pressed.connect(self.the_button_was_pressed)
        self.button.clicked.connect(self.the_button_was_clicked)
        self.button.clicked.connect(self.the_button_was_clicked_too)
        self.button.clicked.connect(print)
        self.windowTitleChanged.connect(lambda: print("Title"))

        self.setWindowTitle("One shot application")


        # self.setFixedSize(QSize(400,300))
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        # in Qt there is no get, only set, for get:
        # print(self.windowTitle())
        # print(self.centralWidget())
        self.setCentralWidget(self.button)

    # when you put static, there is no need for self
    @staticmethod
    def the_button_was_clicked_too(checked):
        print("Clicked too!", checked)



    def the_button_was_clicked(self):
        print("Clicked!", self.button.isChecked())

        # disable button, it doesn't work anymore
        self.button.setEnabled(False)

        # set the text of the button after clicked
        self.button.setText("Already clicked!")

        # change the title of the windows after button was clicked
        self.windowTitleChanged.connect(self.print_title)
        self.setWindowTitle("One shot application")
        # self.(True)



        # doesn't allow to change the size of the windows anymore
        self.setFixedSize(QSize(400, 300))

    def print_title(self):
        print(self.windowTitle())


    @staticmethod
    def the_button_was_pressed(checked):
        print("Pressed!", checked)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
