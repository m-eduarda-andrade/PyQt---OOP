# Created By  : Maria Eduarda Costa Leite Andrade
# Created Date: 2021/11/23
# ---------------------------------------------------------------------------
""" Details about the module and for what purpose it was built for"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sys
import re
from datetime import datetime

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QVBoxLayout,    # vertical
    QFormLayout,    # like a form: name, birthdate, use "addRow(text, Widget)
    QDateEdit,
    QComboBox,
    QSlider,
    QSpinBox,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QLabel,
    QStatusBar,
    QAction,
)


class MainWindow(QMainWindow):
    """MainWindow is a class for supporting the GUI of this application."""
    def __init__(self):

        super().__init__()

        # Window settings
        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(800, 600))
        self.setMinimumSize(QSize(400, 300))

        # WIDGETS
        self.matrikel = QSpinBox()
        self.settings_matrikel()

        self.name = QLineEdit()
        self.settings_name()

        self.birthdate = QDateEdit()

        self.study_place = QComboBox()
        self.settings_study_place()

        self.button = QPushButton("Absenden")


        # FORM
        self.form = QFormLayout()
        self.set_widgets_form()

        #LAYOUT
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.form)
        self.layout.addWidget(self.button, Qt.AlignRight)


        # CONTAINER
        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

        # MENU
        menu = self.menuBar()  # inbuilt from inheritance of QMainWindow
        file_menu = menu.addMenu("&File")  # was macht das &-Zeichen?

        # Action
        self.button_absenden = QAction("Absenden", self)
        self.button_loeschen = QAction("Loeschen", self)

        # Add actions
        file_menu.addAction(self.button_loeschen)
        file_menu.addAction(self.button_absenden)


        # Testing info
        self.button.clicked.connect(self.check_info)
        self.button_absenden.triggered.connect(self.check_info)
        self.button_loeschen.triggered.connect(self.delete_info)


    def settings_matrikel(self):
        self.matrikel.setRange(30_000, 10_000_000)

    def settings_name(self):
        self.name.setPlaceholderText("Vorname Nachname")

    def settings_study_place(self):
        self.study_place.addItems(["Oldenburg", "Wilhelmshaven", "Elsfleth"])

    def set_widgets_form(self):
        widgets = {
            "Matrikelnummer": self.matrikel,
            "Name": self.name,
            "Geburtsdatum": self.birthdate,
            "Studienort": self.study_place
        }

        for key, value in widgets.items():
            self.form.addRow(key, value)

    def check_info(self):
        match = re.match('[a-zA-Z]+ [a-zA-Z]+', self.name.text())
        if match is None:
            print("Name muss Vorname und Nachname haben")

    def delete_info(self):
        for i in [self.birthdate, self.name, self.matrikel, self.study_place]:
            i.clear()

        self.settings_name()
        self.settings_matrikel()
        self.settings_study_place()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
