"""
File_name: main_window.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 23/11/2021

Define the main windows for both applications.
"""

import pandas as pd
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QStyle,
    QTableView,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from message_box import MessageBoxError
from model import PandasModel
from service import open_file
from scheme import (
    About,
    OpenAddNewWordDialog,
    OpenFileDialog,
    SeparatorDialog,
    StatisticsWindow,
)


class MainWindowPart1(QMainWindow):
    """MainWindow is a class for supporting the GUI of this application."""
    def __init__(self):

        super().__init__()

        # variable to save all files opened
        self.opened_files = {}

        # SETTINGS
        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(600, 400))

        # Icon
        pixmap = getattr(QStyle, "SP_DirHomeIcon")
        self.icon_open = self.style().standardIcon(pixmap)
        pixmap2 = getattr(QStyle, "SP_FileDialogContentsView")
        self.icon_stat = self.style().standardIcon(pixmap2)

        # WIDGETS
        self.about = About("My App")
        self.label = QLabel("Your file(s) will be shown here")
        self.button_file = QPushButton("Open new file")
        self.button_file.setToolTip("Open .csv file")
        self.button_file.setIcon(QIcon(self.icon_open))

        # TAB
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)

        # Tab signal
        self.tabs.tabCloseRequested.connect(lambda index: self.close_tab(index))

        # LAYOUT
        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 1, 1)
        self.layout.addWidget(self.tabs, 2, 1)
        self.tabs.hide()                    # hides until there is a first tab to show
        self.layout.addWidget(self.button_file, 3, 1, alignment=Qt.AlignRight)

        # CONTAINER
        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

        # MENU
        menu = self.menuBar()
        self.file_menu = menu.addMenu("&File")
        self.help_menu = menu.addMenu("&Help")

        # ACTION

        self.button_open = QAction(QIcon(self.icon_open), "&Open", self)
        self.button_open.setShortcut("Ctrl+O")
        self.button_open.setToolTip("Open .csv file")

        self.button_about = QAction("About", self)

        # Add actions
        self.file_menu.addAction(self.button_open)
        self.help_menu.addAction(self.button_about)

        # Add Statistics Submenu
        self.stat_submenu = self.file_menu.addMenu("Show Statistics")

        # SIGNALS
        self.button_file.clicked.connect(self.open_file_dialog)
        self.button_open.triggered.connect(self.open_file_dialog)
        self.help_menu.triggered.connect(lambda: self.about.show())

    def close_tab(self, index):
        """Close tab at a given index."""

        tab_name = self.tabs.tabText(index)
        self.stat_submenu.removeAction(self.opened_files[tab_name]["action"])
        self.opened_files.pop(tab_name)
        self.tabs.removeTab(index)

    def open_file_dialog(self):
        """Open a file dialog to search for a .csv file."""
        dialog_open_file = OpenFileDialog()

        if dialog_open_file.exec_() == QDialog.Accepted:
            file_full_path = dialog_open_file.selectedFiles()
            self.open_separator_dialog(file_full_path)

    def open_separator_dialog(self, file_path, name=""):
        """
        Open a separator modal to collect data of how to handle the .csv file

        :param file_path: Absolute path of .csv file
        :param name: Name of the file, that will be displayed on the Tab
        """
        dialog_separator = SeparatorDialog(file_path[0].split("/")[-1], name)
        dialog_separator.setToolTip("Define which separators the program must use for reading the .csv file:")

        if dialog_separator.exec_() == QDialog.Accepted:

            sep = dialog_separator.separator.currentText()
            dec_sep = dialog_separator.decimal_separator.currentText()
            name = dialog_separator.name.text()

            try:
                df = open_file(file_path[0], sep, dec_sep)
                if name in self.opened_files.keys():
                    raise NameError
                if sep == dec_sep:
                    raise KeyError

                self.opened_files[name] = dict()
                self.opened_files[name]["df"] = df

                self.create_tab_df(df, name.strip())

            except ValueError:
                text = f'File cannot be opened with these separators: {sep} and {dec_sep}'
                msg = MessageBoxError(text)
                msg.exec_()

                if msg.accepted:
                    self.open_separator_dialog(file_path, name)

            except KeyError:
                text = f'File cannot be opened with EQUAL separators: {sep} and {dec_sep}'
                msg = MessageBoxError(text)
                msg.exec_()

                if msg.accepted:
                    self.open_separator_dialog(file_path, name)

            except NameError:
                text = f'File name already exists: {name}'
                msg = MessageBoxError(text)
                msg.exec_()

                if msg.accepted:
                    self.open_separator_dialog(file_path, name)

    def create_tab_df(self, df, name):
        """
        Create display TabLayout with the opened dataframe(s)

        :param df: Pandas dataframe
        :param name: Name displayed on the Tab
        """
        model = PandasModel(df)
        view = QTableView()
        view.setModel(model)

        layout = QVBoxLayout()
        layout.addWidget(view)

        # Create statistics
        self.opened_files[name]["window"] = StatisticsWindow(df=self.opened_files[name]["df"])

        # Button Statistics
        self.opened_files[name]["stat_button"] = QPushButton("Show Statistics")
        self.opened_files[name]["stat_button"].setIcon(QIcon(self.icon_stat))

        self.opened_files[name]["stat_button"].clicked.connect(lambda: self.opened_files[name]["window"].show())

        # Create Action in Submenu
        self.opened_files[name]["action"] = QAction(self.opened_files[name]["stat_button"])
        self.opened_files[name]["action"].setText(name)
        self.opened_files[name]["action"].triggered.connect(lambda: self.opened_files[name]["window"].show())
        self.stat_submenu.addAction(self.opened_files[name]["action"])

        # Create Layout/Container for Tab
        layout.addWidget(self.opened_files[name]["stat_button"], alignment=Qt.AlignLeft)
        container = QWidget()
        container.setLayout(layout)

        # Add new tab
        self.tabs.addTab(container, name)
        self.tabs.show()


class MainWindowPart2(QMainWindow):
    """MainWindow is a class for supporting the GUI of this application."""
    def __init__(self):
        super().__init__()

        # variable to save all tabs opened
        self.opened_tabs = {}

        # SETTINGS
        self.setWindowTitle("My German Dictionary")
        self.setMinimumSize(QSize(800, 600))
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # ICONS
        pixmap = getattr(QStyle, "SP_DialogSaveButton")
        icon_save = self.style().standardIcon(pixmap)
        pixmap2 = getattr(QStyle, "SP_FileIcon")
        icon_new = self.style().standardIcon(pixmap2)

        # WIDGETS
        self.about = About("My German Dictionary")
        self.button_add = QPushButton("Add New Word")
        self.button_add.setToolTip("Add new word to your dictionary")
        self.button_add.setIcon(icon_new)

        self.line = QLineEdit()
        self.line.setPlaceholderText("Search word...")

        self.button_save = QPushButton("Save")
        self.button_save.setIcon(icon_save)

        # TAB
        self.tabs_name = list()
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)

        self.create_tabs()

        # LAYOUT
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.button_save)
        self.hbox.addWidget(self.button_add)

        self.layout.addLayout(self.hbox)

        # CONTAINER
        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

        # MENU
        menu = self.menuBar()
        self.file_menu = menu.addMenu("&File")
        self.help_menu = menu.addMenu("&Help")

        # ACTION
        self.button_menu_add = QAction(QIcon(icon_new), "&Add new word", self)
        self.button_menu_add.setShortcut("Ctrl+N")
        self.button_menu_add.setToolTip("Add new word to your dictionary")

        self.button_menu_save = QAction(QIcon(icon_save), "&Save", self)
        self.button_menu_save.setShortcut("Ctrl+S")
        self.button_menu_save.setToolTip("Save your dictionary")

        self.button_menu_exit = QAction("&Exit", self)
        self.button_menu_exit.setToolTip("Exit your program")

        self.button_about = QAction("About", self)

        # Add actions
        self.file_menu.addAction(self.button_menu_add)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.button_menu_save)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.button_menu_exit)

        self.help_menu.addAction(self.button_about)

        # SIGNALS
        self.button_add.clicked.connect(self.open_add_word_dialog)
        self.button_menu_add.triggered.connect(self.open_add_word_dialog)

        self.button_save.released.connect(self.save_df)
        self.button_menu_save.triggered.connect(self.save_df)

        self.button_menu_exit.triggered.connect(self.close)
        self.help_menu.triggered.connect(lambda: self.about.show())

    def create_tabs(self):
        """Create one tab for each most used classes of words."""

        self.tabs_name = ["Nomen", "Adjektive", "Verben", "Konjuktive", "Präpositionen", "Adverbien", "Redewendungen"]
        xls = pd.ExcelFile('my_german_dictionary.xlsx')

        for tab in self.tabs_name:
            df = pd.read_excel(xls, tab)
            model = PandasModel(pd.DataFrame(df))

            self.opened_tabs[tab] = dict()
            self.opened_tabs[tab]["Model"] = model

            self.opened_tabs[tab]["View"] = QTableView()
            self.opened_tabs[tab]["View"].setModel(self.opened_tabs[tab]["Model"])

            self.tabs.addTab(self.opened_tabs[tab]["View"], tab)

    def open_add_word_dialog(self):
        """Open a dialog to add a new word to the dictionary."""
        add_word_dialog = OpenAddNewWordDialog(self.tabs_name)

        if add_word_dialog.exec_() == QDialog.Accepted:
            word = add_word_dialog.new_word.text()

            # get word class
            classes = add_word_dialog.radio_buttons_class.items()
            word_class = [name for name, button in classes if button.isChecked()][0]

            example = add_word_dialog.example.text()
            translation = add_word_dialog.translation.text()

            # get article
            articles = add_word_dialog.radio_buttons_article.items()
            if word_class == "Nomen":
                article = [art for art, button in articles if button.isChecked()][0]
                self.opened_tabs[word_class]["Model"].append_row([article, word, example, translation])
            else:
                self.opened_tabs[word_class]["Model"].append_row([word, example, translation])

    def save_df(self):
        """Save all dataframe in an excel extension with different sheets for each tab."""

        try:
            writer = pd.ExcelWriter('my_german_dictionary.xlsx', engine='xlsxwriter')

            for name, tab in self.opened_tabs.items():
                aux_df = tab["Model"].dataframe
                aux_df.to_excel(writer, sheet_name=name, index=False)

            writer.save()
            self.status_bar.showMessage("Success: file saved!", msecs=5000)
        except Exception as err:
            self.status_bar.showMessage(f"Error: file not saved: {str(err)}", msecs=5000)

    def was_there_changes(self):
        """Check if there is changes between the written excel file and the current opened tabs
        to check if unsaved changes were made before closing."""

        xls = pd.ExcelFile('my_german_dictionary.xlsx')
        for tab in self.tabs_name:
            df = pd.read_excel(xls, tab)
            df_tab = self.opened_tabs[tab]["Model"].dataframe
            if not df.equals(df_tab):
                return True

        return False

    def closeEvent(self, event):
        """Handling leaving without saving changes."""
        if self.was_there_changes():
            reply = QMessageBox.question(
                self, "Message",
                "Are you sure you want to quit? Changes were not saved.",
                QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Discard,
                QMessageBox.Save)

            if reply == QMessageBox.Save:
                self.save_df()
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
            else:
                event.accept()
