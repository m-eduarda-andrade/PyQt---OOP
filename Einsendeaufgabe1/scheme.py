"""
File_name: scheme.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 05/12/2021

File to define schemes: classes of dialogs and windows
"""

import re

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenuBar,
    QPushButton,
    QRadioButton,
    QStatusBar,
    QStyle,
    QTableView,
    QTextEdit,
    QWidget,
    QVBoxLayout,
)

from model import PandasModel
from service import (
    regex_for_adjectives,
    regex_for_nouns,
    regex_for_verbs,
    get_statistics,
)


class About(QWidget):
    """
    This is a window for showing about.
    """

    def __init__(self, name):

        super().__init__()
        self.setWindowTitle(f"About {name}")
        self.setMinimumSize(200, 100)

        self.date = QLabel("Built on December 07, 2021")
        self.version = QLabel("Built in Python 3.8")
        self.name = QLabel("Copyright © 2021 Maria Eduarda Costa Leite Andrade")

        self.layout = QGridLayout()
        self.layout.addWidget(self.date, 1, 1, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.version, 2, 1, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.name, 3, 1, alignment=Qt.AlignHCenter)

        self.setLayout(self.layout)


class OpenFileDialog(QFileDialog):
    """
    This modal is a QFileDialog.
    It is used to open .csv files.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Open Single File")
        self.setNameFilter('CSV files (*.csv)')  # set filter for data type


class SeparatorDialog(QDialog):
    """
    This modal is a QDialog.
    It is used to define which separator should be used when .csv file is read.
    """

    def __init__(self, file_name, name=""):
        super().__init__()
        self.setWindowTitle("Separators .csv")

        # Layouts
        self.layout = QVBoxLayout()
        self.grid = QGridLayout()

        # Label

        # self.label = QLabel("")
        self.label = QLabel(f"File '{file_name}'")

        # Frame
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.HLine)
        self.frame.setFrameShadow(QFrame.Sunken)

        # Separator
        self.grid.addWidget(QLabel("Separator: "), 0, 0)

        self.separator = QComboBox()
        self.separator.addItems([",", ";", ".", "-"])
        self.separator.setCurrentIndex(0)

        self.grid.addWidget(self.separator, 0, 1)

        # Decimal separator
        self.grid.addWidget(QLabel("Decimal separator: "), 1, 0)

        self.decimal_separator = QComboBox()
        self.decimal_separator.addItems([".", ",", ";"])
        self.decimal_separator.setCurrentIndex(0)

        self.grid.addWidget(self.decimal_separator, 1, 1)

        # Name of file
        self.grid.addWidget(QLabel("File name: "), 2, 0)
        self.name = QLineEdit()
        if name == "":
            self.name.setText(file_name.split(".")[0])
        else:
            self.name.setText(name)
        self.grid.addWidget(self.name, 2, 1)

        # Buttons
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Define Layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.frame)
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.buttonBox)

        # Set Layout of this window
        self.setLayout(self.layout)


class StatisticsWindow(QWidget):
    """
    This is a window for calculating and showing the statistics of a given dataframe of time series.
    """

    def __init__(self, df):

        super().__init__()
        self.setWindowTitle("Statistics")
        self.setMinimumSize(800, 400)

        results = get_statistics(df)

        model = PandasModel(results)
        view = QTableView()
        view.setModel(model)

        # Icons
        pixmap = getattr(QStyle, "SP_CommandLink")
        self.icon_new = self.style().standardIcon(pixmap)
        pixmap = getattr(QStyle, "SP_DialogCancelButton")
        self.icon_cancel = self.style().standardIcon(pixmap)
        pixmap = getattr(QStyle, "SP_DialogSaveButton")
        self.icon_save = self.style().standardIcon(pixmap)

        # Add note Button
        self.note_button = QPushButton("Add Note")
        self.note_button.setCheckable(True)
        self.note_button.setIcon(QIcon(self.icon_new))

        # Save statistics Button
        self.save_button = QPushButton("Save Statistics")
        self.save_button.setIcon(QIcon(self.icon_save))

        # Note
        self.note = QTextEdit()
        self.note.setPlaceholderText("Write here your notes/observations to this statistics")
        self.note.setToolTip("To save your note together with your statistics, simply press 'Save Statistics'")

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(view)
        self.layout.addWidget(self.note)
        self.note.hide()
        self.layout.addWidget(self.note_button, alignment=Qt.AlignLeft)

        self.layout.addWidget(self.save_button, alignment=Qt.AlignRight)

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setLayout(self.layout)

        # MENU

        menu = QMenuBar(self)
        self.file_menu = menu.addMenu("&File")

        # ACTION
        self.action_save = QAction(QIcon(self.icon_save), "&Save", self)
        self.action_save.setShortcut("Ctrl+S")
        self.action_save.setToolTip("Save Statistics as .csv file")

        # Add actions
        self.file_menu.addAction(self.action_save)

        # SIGNALS
        self.action_save.triggered.connect(lambda: self.save_file(results))
        self.save_button.clicked.connect(lambda: self.save_file(results))

        self.note_button.clicked.connect(self.show_note_text_edit)

        # Add menu
        self.layout.setMenuBar(menu)

        # Add status bar
        self.status_bar = QStatusBar(self)

        self.layout.addWidget(self.status_bar)

    def show_note_text_edit(self):
        """Define when button is for adding or discarding a note, and displaying the text box."""
        if self.note_button.isChecked():
            self.note.show()
            self.note_button.setText("Discard Note")

            self.note_button.setIcon(QIcon(self.icon_cancel))

            self.note_button.setToolTip(
                "To NOT save your note together with your statistics, simply press 'Discard Note'")
            self.note_button.update()
        else:
            self.note.hide()
            self.note.clear()
            self.note_button.setText("Add Note")
            self.note_button.setIcon(QIcon(self.icon_new))
            self.note_button.setToolTip(
                "To save your note together with your statistics, simply press 'Save Statistics'")

    def save_file(self, df):
        """
        Create dialog to save the statistics.

        :param df: Pandas dataframe used for statistics
        """

        try:
            file_name = QFileDialog.getSaveFileName(self, "Save Statistics", "", "Save .csv (*.csv)")

            # Add observation to dataframe
            if self.note.toPlainText() != "":
                df.loc[df.shape[0]] = None
                new_rows = ["Observation", self.note.toPlainText()]
                for i in range(df.shape[1] - 2):
                    new_rows.append("")

                series_obj = pd.Series(new_rows, index=df.columns)
                df = df.append(series_obj, ignore_index=True)

            df.to_csv(file_name[0].split(".")[0] + ".csv", index=False)
            self.status_bar.showMessage("File was saved successfully!!!", msecs=5000)

        except (KeyError, ValueError, NameError, IndexError, AttributeError) as err:
            self.status_bar.showMessage(f"Something went wrong: file was not saved :(\n{str(err)}", msecs=5000)


class OpenAddNewWordDialog(QDialog):
    def __init__(self, tabs_name):
        """
        Dialog box for entering a new word into the dictionary.
        :param tabs_name: names of tabs of main window.
        """
        super().__init__()
        self.setWindowTitle("Add New Word")
        self.setMinimumSize(600, 400)

        # GROUP 1
        self.group_class = QGroupBox("Select the class of the word:")

        self.radio_buttons_class = dict()
        for name in tabs_name:
            self.radio_buttons_class[name] = QRadioButton(name)

        self.create_group_class()

        # GROUP 2
        self.group_article = QGroupBox("Select the article:")

        self.radio_buttons_article = dict()
        for article in ["der", "die", "das"]:
            self.radio_buttons_article[article] = QRadioButton(article)

        self.create_group_article()

        # WIDGETS
        self.label_word = QLabel("Enter your new word:")

        self.new_word = QLineEdit()
        self.new_word.setPlaceholderText("e.g. 'warscheinlich'")

        self.label_example = QLabel("Enter an example:")
        self.example = QLineEdit()
        self.example.setPlaceholderText("e.g. 'Warscheinlich kommt er heute.'")

        self.label_translation = QLabel("Enter translation:")
        self.translation = QLineEdit()
        self.translation.setPlaceholderText("e.g. 'probable'")

        # SIGNALS
        self.new_word.textChanged.connect(self.new_word_entry_signals_regex)

        for name, button in self.radio_buttons_class.items():
            if name == "Nomen":
                button.clicked.connect(self.noun_clicked)
            elif name == "Redewendungen":
                button.clicked.connect(self.expression_clicked)
            else:
                button.clicked.connect(self.not_noun_clicked)

        # LAYOUT
        self.layout = QVBoxLayout()
        self.new_word_layout = QHBoxLayout()
        self.new_word_layout.addWidget(self.label_word)
        self.new_word_layout.addWidget(self.new_word)

        self.layout.addLayout(self.new_word_layout)

        self.layout.addStretch()
        self.layout.addWidget(self.group_class)

        self.layout.addStretch()
        self.layout.addWidget(self.group_article)

        self.layout.addStretch()
        self.grid_box = QGridLayout()

        self.grid_box.addWidget(self.label_example, 1, 1)
        self.grid_box.addWidget(self.example, 1, 2)

        self.grid_box.addWidget(self.label_translation, 2, 1)
        self.grid_box.addWidget(self.translation, 2, 2)

        self.layout.addLayout(self.grid_box)

        # BUTTONS
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        self.layout.addWidget(self.buttonBox)

        # SET LAYOUT
        self.setLayout(self.layout)

    def new_word_entry_signals_regex(self):
        """Run regex for each change made on the word to search to which class that word belongs, and if it is a noun,
        searches for the article. For each result found, a radio button is selected, and/or article box is enabled/disabled."""

        word = self.new_word.text().strip()

        if word != "":
            self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        # check noun
        if re.match("^[A-ZÄÖÜ]", word):
            gender_nouns = regex_for_nouns(word)
            self.radio_buttons_class["Nomen"].setChecked(True)

            if gender_nouns is not None:
                self.radio_buttons_article[gender_nouns].setChecked(True)
            self.group_article.setDisabled(False)
        else:
            funcs = {
                "Adjektive": regex_for_adjectives(word),
                "Verben": regex_for_verbs(word)
            }

            for name, func in funcs.items():
                if func is not None:
                    self.radio_buttons_class[name].setChecked(True)
                    break
            else:
                if self.radio_buttons_class["Nomen"].isChecked():
                    self.radio_buttons_class["Adjektive"].setChecked(True)

            self.group_article.setDisabled(True)

    def create_group_class(self):
        """Create a group box with the radio buttons for classes."""
        # CREATE LAYOUT FOR RADIO BUTTONS
        count_buttons = 0
        count_layout = 0
        new_layout = list()

        for button in self.radio_buttons_class.values():
            if count_buttons == 3:
                count_layout += 1
                count_buttons = 0

            if count_buttons == 0:
                new_layout.append(QHBoxLayout())

            new_layout[count_layout].addWidget(button)
            count_buttons += 1

        layout = QVBoxLayout()
        for hbox in new_layout:
            layout.addLayout(hbox)

        self.radio_buttons_class["Nomen"].setChecked(True)
        self.group_class.setLayout(layout)

    def create_group_article(self):
        """Create a group box with the radio buttons for articles."""
        button_article_layout = QHBoxLayout()
        for button in self.radio_buttons_article.values():
            button_article_layout.addWidget(button)

        self.radio_buttons_article["der"].setChecked(True)
        self.group_article.setLayout(button_article_layout)

    def noun_clicked(self):
        """Class selected is noun, so word must be upper case."""
        self.group_article.setDisabled(False)
        word = self.new_word.text()
        if not re.match("^[A-ZÄÖÜ]", word):
            word = word.title()
            self.new_word.setText(word)


    def not_noun_clicked(self):
        """Class selected is not a noun, so word must be lower case."""
        self.group_article.setDisabled(True)
        word = self.new_word.text()
        if re.match("^[A-ZÄÖÜ]", word):
            word = word.lower()
            self.new_word.setText(word)


    def expression_clicked(self):
        """Some expression may have more than one word and one of them could be capital. Therefore, it is not possible
        to use "not_noun_clicked" function."""
        self.group_article.setDisabled(True)


