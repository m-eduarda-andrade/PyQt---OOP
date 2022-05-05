"""
File_name: main_window.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 16/01/2022

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
    QMainWindow,
    QPushButton,
    QStyle,
    QTableView,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from message_box import MessageBoxError
from model import PandasModel
from scheme import (
    About,
    OpenFileDialog,
    PlotData,
    SeparatorDialog,
    StatisticsWindow,
    Crosshair,
)


class MainWindowTeil1(QMainWindow):
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
        self.tabs.hide()  # hides until there is a first tab to show
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

        self.exit_button = QAction("&Exit", self)
        self.exit_button.setToolTip("Exit Program")

        # Add actions
        self.file_menu.addAction(self.button_open)
        self.help_menu.addAction(self.button_about)

        # Add Statistics Submenu
        self.stat_submenu = self.file_menu.addMenu("Show Statistics")
        self.plot_submenu = self.file_menu.addMenu("Plot Statistics")

        # Add exit action
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_button)

        # SIGNALS
        self.button_file.clicked.connect(self.open_file_dialog)
        self.button_open.triggered.connect(self.open_file_dialog)
        self.help_menu.triggered.connect(lambda: self.about.show())
        self.exit_button.triggered.connect(lambda: self.close())

    def close_tab(self, index):
        """Close tab at a given index."""

        tab_name = self.tabs.tabText(index)
        self.stat_submenu.removeAction(self.opened_files[tab_name]["action"])
        self.plot_submenu.removeAction(self.opened_files[tab_name]["action_plot"])
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
                df = pd.read_csv(file_path[0], sep=sep, decimal=dec_sep, header=0, dtype=float)
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
        self.opened_files[name]["stat_window"] = StatisticsWindow(df=self.opened_files[name]["df"])

        # Button Statistics
        self.opened_files[name]["stat_button"] = QPushButton("Show Statistics")
        self.opened_files[name]["stat_button"].setIcon(QIcon(self.icon_stat))
        self.opened_files[name]["stat_button"].clicked.connect(lambda: self.opened_files[name]["stat_window"].show())

        # Create plot window
        self.opened_files[name]["plot_window"] = PlotData(df=self.opened_files[name]["df"], name=name)

        # Button Plot Data
        self.opened_files[name]["plot_button"] = QPushButton("Plot Data")
        self.opened_files[name]["plot_button"].setIcon(QIcon(self.icon_stat))
        self.opened_files[name]["plot_button"].clicked.connect(lambda: self.opened_files[name]["plot_window"].show())

        # Create Action in Submenu Stats
        self.opened_files[name]["action"] = QAction(self.opened_files[name]["stat_button"])
        self.opened_files[name]["action"].setText(name)
        self.opened_files[name]["action"].triggered.connect(lambda: self.opened_files[name]["window"].show())
        self.stat_submenu.addAction(self.opened_files[name]["action"])

        # Create Action in Submenu Plot
        self.opened_files[name]["action_plot"] = QAction(self.opened_files[name]["plot_window"])
        self.opened_files[name]["action_plot"].setText(name)
        self.opened_files[name]["action_plot"].triggered.connect(lambda: self.opened_files[name]["plot_window"].show())
        self.plot_submenu.addAction(self.opened_files[name]["action_plot"])

        # Create Layout/Container for Tab
        hbox = QHBoxLayout()
        hbox.addWidget(self.opened_files[name]["stat_button"], alignment=Qt.AlignLeft)
        hbox.addWidget(self.opened_files[name]["plot_button"], alignment=Qt.AlignRight)
        layout.addLayout(hbox)

        container = QWidget()
        container.setLayout(layout)

        # Add new tab
        self.tabs.addTab(container, name)
        self.tabs.show()


class MainWindowTeil2(QMainWindow):
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
        self.tabs.hide()  # hides until there is a first tab to show
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

        self.exit_button = QAction("&Exit", self)
        self.exit_button.setToolTip("Exit Program")

        # Add actions
        self.file_menu.addAction(self.button_open)
        self.help_menu.addAction(self.button_about)

        # Add Statistics Submenu
        self.stat_submenu = self.file_menu.addMenu("Show Statistics")
        self.plot_submenu = self.file_menu.addMenu("Plot Statistics")

        # Add exit action
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_button)

        # SIGNALS
        self.button_file.clicked.connect(self.open_file_dialog)
        self.button_open.triggered.connect(self.open_file_dialog)
        self.help_menu.triggered.connect(lambda: self.about.show())
        self.exit_button.triggered.connect(lambda: self.close())

    def close_tab(self, index):
        """Close tab at a given index."""

        tab_name = self.tabs.tabText(index)
        self.stat_submenu.removeAction(self.opened_files[tab_name]["action"])
        self.plot_submenu.removeAction(self.opened_files[tab_name]["action_plot"])
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
                df = pd.read_csv(file_path[0], sep=sep, decimal=dec_sep, header=0, dtype=float)
                if name in self.opened_files.keys():
                    raise NameError
                if sep == dec_sep:
                    raise KeyError

                self.opened_files[name] = dict()
                self.opened_files[name]["df"] = df

                self.create_tab_df(df, name.strip())

            except ValueError as e:
                print(str(e))
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
        self.opened_files[name]["stat_window"] = StatisticsWindow(df=self.opened_files[name]["df"])

        # Button Statistics
        self.opened_files[name]["stat_button"] = QPushButton("Show Statistics")
        self.opened_files[name]["stat_button"].setIcon(QIcon(self.icon_stat))
        self.opened_files[name]["stat_button"].clicked.connect(lambda: self.opened_files[name]["stat_window"].show())

        # Create plot window
        self.opened_files[name]["plot_window"] = Crosshair(df=self.opened_files[name]["df"], name=name)

        # Button Plot Data
        self.opened_files[name]["plot_button"] = QPushButton("Plot Data")
        self.opened_files[name]["plot_button"].setIcon(QIcon(self.icon_stat))
        self.opened_files[name]["plot_button"].clicked.connect(lambda: self.opened_files[name]["plot_window"].show())

        # Create Action in Submenu Stats
        self.opened_files[name]["action"] = QAction(self.opened_files[name]["stat_button"])
        self.opened_files[name]["action"].setText(name)
        self.opened_files[name]["action"].triggered.connect(lambda: self.opened_files[name]["window"].show())
        self.stat_submenu.addAction(self.opened_files[name]["action"])

        # Create Action in Submenu Plot
        self.opened_files[name]["action_plot"] = QAction(self.opened_files[name]["plot_window"])
        self.opened_files[name]["action_plot"].setText(name)
        self.opened_files[name]["action_plot"].triggered.connect(lambda: self.opened_files[name]["plot_window"].show())
        self.plot_submenu.addAction(self.opened_files[name]["action_plot"])

        # Create Layout/Container for Tab
        hbox = QHBoxLayout()
        hbox.addWidget(self.opened_files[name]["stat_button"], alignment=Qt.AlignLeft)
        hbox.addWidget(self.opened_files[name]["plot_button"], alignment=Qt.AlignRight)
        layout.addLayout(hbox)

        container = QWidget()
        container.setLayout(layout)

        # Add new tab
        self.tabs.addTab(container, name)
        self.tabs.show()
