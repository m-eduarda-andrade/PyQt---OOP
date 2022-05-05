"""
File_name: scheme.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 16/01/2022

File to define schemes: classes of dialogs and windows

Credits:
    icon dark mode: https://www.flaticon.com/free-icons/light-mode
"""


import pandas as pd
import pyqtgraph as pg
import random

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
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenuBar,
    QPushButton,
    QStatusBar,
    QStyle,
    QTableView,
    QTextEdit,
    QWidget,
    QVBoxLayout,
    QCheckBox,
)

from model import PandasModel
from service import get_statistics


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

        self.setLayout(self.layout)

        # MENU

        menu = QMenuBar(self)
        self.file_menu = menu.addMenu("&File")

        # ACTION
        self.action_save = QAction(QIcon(self.icon_save), "&Save", self)
        self.action_save.setShortcut("Ctrl+S")
        self.action_save.setToolTip("Save Statistics as .csv file")

        self.exit_button = QAction("&Exit", self)
        self.exit_button.setToolTip("Exit Program")

        # Add actions
        self.file_menu.addAction(self.action_save)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_button)

        # SIGNALS
        self.action_save.triggered.connect(lambda: self.save_file(results))
        self.save_button.clicked.connect(lambda: self.save_file(results))

        self.note_button.clicked.connect(self.show_note_text_edit)
        self.exit_button.triggered.connect(lambda: self.close())

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


class PlotData(QWidget):
    def __init__(self, df, name):
        """
        Window to plot the curves and its statistics.
        df: dataframe used to plot.
        name: name of the dataframe.
        """
        super().__init__()
        self.setWindowTitle("Plot Data")
        self.setMinimumSize(600, 400)

        self.symbols = ["o", "t", "t1", "t2", "t3", "s", "p", "h", "star", "+", "d", "x"]

        # Plot Widget
        self.plot_widget = pg.PlotWidget(name=name)
        self.plot_widget.addLegend()
        self.plot_widget.setBackground((242, 242, 242))
        self.plot_widget.showButtons()
        self.plot_widget.enableAutoRange()
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)

        self.plotted_curves = dict()

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Widgets
        self.checkboxes = dict()
        self.label = QLabel("Select the curve(s) to be displayed:")
        self.marker_button = QPushButton("Show markers")
        self.stat_button = QPushButton("Show statistics")
        self.dark_mode = QPushButton()
        self.dark_mode.setIcon(QIcon("mode.png"))

        layout.addWidget(self.dark_mode, alignment=Qt.AlignRight)
        layout.addWidget(self.label)

        # Icons
        pixmap = getattr(QStyle, "SP_FileDialogContentsView")
        self.icon_stat = self.style().standardIcon(pixmap)
        pixmap2 = getattr(QStyle, "SP_DialogCancelButton")
        self.icon_cancel = self.style().standardIcon(pixmap2)
        pixmap3 = getattr(QStyle, "SP_TitleBarShadeButton")
        self.icon_show_marker = self.style().standardIcon(pixmap3)
        pixmap4 = getattr(QStyle, "SP_TitleBarUnshadeButton")
        self.icon_hide_marker = self.style().standardIcon(pixmap4)

        self.marker_button.setIcon(self.icon_show_marker)
        self.stat_button.setIcon(self.icon_stat)

        # curves from columns of df
        self.curves = {col: df[col].tolist() for col in df.columns.values}

        # checkboxes
        vbox = QVBoxLayout()
        for c_name in self.curves.keys():
            self.checkboxes[c_name] = QCheckBox(c_name)
            self.checkboxes[c_name].setChecked(True)
            self.checkboxes[c_name].clicked.connect(self.show_hide_curve)
            vbox.addWidget(self.checkboxes[c_name])

        # display widgets
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.marker_button)
        hbox.addWidget(self.stat_button)

        layout.addLayout(hbox)

        # plotting curves
        for c_name, curve in self.curves.items():
            self.add_curve(c_name, curve)

        # plotting stats
        self.create_statistics(df)

        # MENU
        menu = QMenuBar()
        self.file_menu = menu.addMenu("&File")
        layout.setMenuBar(menu)

        # ACTION
        self.exit_button = QAction("&Exit", self)
        self.exit_button.setToolTip("Exit Program")

        # Add actions
        self.file_menu.addAction(self.exit_button)

        # SIGNALS Actions
        self.exit_button.triggered.connect(lambda: self.close())

        # Signals
        self.marker_button.setCheckable(True)
        self.stat_button.setCheckable(True)
        self.dark_mode.setCheckable(True)
        self.marker_button.clicked.connect(self.show_hide_markers)
        self.stat_button.clicked.connect(self.show_hide_stat)
        self.dark_mode.clicked.connect(self.change_dark_mode)

    def add_curve(self, c_name, data_y):
        """Add each curve to plot_widget with random colours"""
        # set data x
        data_x = list(range(len(data_y)))

        # set random colour
        colour_r = random.choice(list(range(0, 255)))
        colour_g = random.choice(list(range(0, 255)))
        colour_b = random.choice(list(range(0, 255)))
        pen = pg.mkPen(color=(colour_r, colour_g, colour_b), width=3)

        # plot and save variable
        plot = self.plot_widget.plot(data_x, data_y, name=c_name, pen=pen, symbolBrush=(colour_r, colour_g, colour_b))
        plot.setSymbol(None)
        plot.visibleChanged.connect(self.view_changed)
        self.plotted_curves[c_name] = {'x': data_x, 'y': data_y, 'plot': plot}

    def view_changed(self):
        """Every time a plot is hidden using the legend buttons, the checkboxes must be updated."""
        for name, curve in self.plotted_curves.items():
            if curve["plot"].isVisible():
                self.checkboxes[name].setChecked(True)
            else:
                self.checkboxes[name].setChecked(False)

    def create_statistics(self, df):
        """Create infinite lines for statistics of each curve."""
        for cbox in self.checkboxes.values():
            curve_name = cbox.text()
            self.plotted_curves[curve_name]["stats"] = {}
            self.plotted_curves[curve_name]["stats"]["il_min"] = pg.InfiniteLine(
                angle=0,
                label=f"Min - {curve_name}",
                labelOpts={"movable": True},
                pos=df[curve_name].min(),
                pen=pg.mkPen(color=(102, 178, 255), width=0.3))
            self.plotted_curves[curve_name]["stats"]["il_max"] = pg.InfiniteLine(
                angle=0,
                label=f"Max - {curve_name}",
                labelOpts={"movable": True},
                pos=df[curve_name].max(),
                pen=pg.mkPen(color=(255, 51, 51), width=0.3))
            self.plotted_curves[curve_name]["stats"]["il_avg"] = pg.InfiniteLine(
                angle=0,
                label=f"Median - {curve_name}",
                labelOpts={"movable": True},
                pos=df[curve_name].median(),
                pen=pg.mkPen(color=(0, 255, 0), width=0.3))
            self.plotted_curves[curve_name]["stats"]["il_mean"] = pg.InfiniteLine(
                angle=0,
                label=f"Mean - {curve_name}",
                labelOpts={"movable": True},
                pos=df[curve_name].mean(),
                pen=pg.mkPen(color=(255, 0, 127), width=0.3))
            self.plotted_curves[curve_name]["stats"]["il_std"] = pg.InfiniteLine(
                angle=0,
                label=f"Standard Deviation - {curve_name}",
                labelOpts={"movable": True},
                pos=df[curve_name].std(),
                pen=pg.mkPen(color=(51, 51, 255), width=0.3))

            # plot and hide
            for stat in self.plotted_curves[curve_name]["stats"].values():
                self.plot_widget.addItem(stat)
                stat.hide()

    def show_hide_curve(self):
        """Show or hide curve using checkboxes."""
        for cbox in self.checkboxes.values():
            if cbox.isChecked():
                self.plotted_curves[cbox.text()]["plot"].show()

                # show stats if is checked
                if self.stat_button.isChecked():
                    for stat in self.plotted_curves[cbox.text()]["stats"].values():
                        stat.show()
            else:
                # hide curve
                self.plotted_curves[cbox.text()]["plot"].hide()
                # hide stats
                for stat in self.plotted_curves[cbox.text()]["stats"].values():
                    stat.hide()

        self.plot_widget.autoRange()

    def show_hide_markers(self):
        """Show or hide markers of the visible curves, activated by a button."""
        if self.marker_button.isChecked():
            self.marker_button.setText("Hide markers")
            self.marker_button.setIcon(self.icon_hide_marker)
        else:
            self.marker_button.setText("Show markers")
            self.marker_button.setIcon(self.icon_show_marker)

        for cbox in self.checkboxes.values():
            if cbox.isChecked() and self.marker_button.isChecked():
                self.plotted_curves[cbox.text()]["plot"].setSymbol(random.choice(self.symbols))

            else:
                self.plotted_curves[cbox.text()]["plot"].setSymbol(None)

    def show_hide_stat(self):
        """Show or hide statistics lines of the visible curves, activated by a button."""

        if self.stat_button.isChecked():
            self.stat_button.setText("Hide Statistics")
            self.stat_button.setIcon(self.icon_cancel)
        else:
            self.stat_button.setText("Show Statistics")
            self.stat_button.setIcon(self.icon_stat)

        for cbox in self.checkboxes.values():
            if cbox.isChecked() and self.stat_button.isChecked():
                for stat in self.plotted_curves[cbox.text()]["stats"].values():
                    stat.show()
            else:
                for stat in self.plotted_curves[cbox.text()]["stats"].values():
                    stat.hide()

    def change_dark_mode(self):
        """Change graph background to dark or light mode."""
        if self.dark_mode.isChecked():
            self.plot_widget.setBackground((0, 0, 0))
        else:
            self.plot_widget.setBackground((242, 242, 242))


class Crosshair(QWidget):
    def __init__(self, df, name):
        """
        Window to plot the curves and its statistics with crosshair.
        df: dataframe used to plot.
        name: name of the dataframe.
        """
        super().__init__()

        # Crosshair
        self.setWindowTitle("Crosshair Example")
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('pyqtgraph example: crosshair')

        self.label_mouse = pg.LabelItem(justify='right')
        self.win.addItem(self.label_mouse)

        self.p1 = self.win.addPlot(row=1, col=0)
        self.p2 = self.win.addPlot(row=2, col=0)
        self.p1.showGrid(x=True, y=True, alpha=0.2)
        self.p2.showGrid(x=True, y=True, alpha=0.2)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.win)
        self.setLayout(layout)

        # Stats Label
        self.label_stats = QLabel()
        self.label_stats.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label_stats.setStyleSheet("QLabel { background-color : rgb(0, 0, 0)}")
        layout.addWidget(self.label_stats)

        # Region
        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
        # item when doing auto-range calculations.
        self.p2.addItem(self.region, ignoreBounds=True)

        self.p1.setAutoVisible(x=True, y=True)
        self.p1.addLegend()
        self.p1.enableAutoRange()

        self.p2.enableAutoRange()

        # From Plot Data
        # List for random symbols
        self.symbols = ["o", "t", "t1", "t2", "t3", "s", "p", "h", "star", "+", "d", "x"]
        self.plotted_curves = dict()

        # Widgets
        self.checkboxes = dict()
        self.label = QLabel("Select the curve(s) to be displayed:")
        self.label_st = QLabel("Statistics")
        self.marker_button = QPushButton("Show markers")
        self.stat_button = QPushButton("Show statistics")
        self.dark_mode = QPushButton()
        self.dark_mode.setIcon(QIcon("mode.png"))

        hb = QHBoxLayout()
        hb.addWidget(self.label)
        hb.addWidget(self.label_st)
        layout.addLayout(hb)

        # Icons
        pixmap = getattr(QStyle, "SP_FileDialogContentsView")
        self.icon_stat = self.style().standardIcon(pixmap)
        pixmap2 = getattr(QStyle, "SP_DialogCancelButton")
        self.icon_cancel = self.style().standardIcon(pixmap2)
        pixmap3 = getattr(QStyle, "SP_TitleBarShadeButton")
        self.icon_show_marker = self.style().standardIcon(pixmap3)
        pixmap4 = getattr(QStyle, "SP_TitleBarUnshadeButton")
        self.icon_hide_marker = self.style().standardIcon(pixmap4)

        self.marker_button.setIcon(self.icon_show_marker)
        self.stat_button.setIcon(self.icon_stat)

        # curves from columns of df
        self.curves = {col: df[col].tolist() for col in df.columns.values}

        # Checkboxes
        vbox = QVBoxLayout()
        for c_name in self.curves.keys():
            self.checkboxes[c_name] = QCheckBox(c_name)
            self.checkboxes[c_name].setChecked(True)
            self.checkboxes[c_name].clicked.connect(self.show_hide_curve)
            vbox.addWidget(self.checkboxes[c_name])

        # Display Widgets
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        vb = QVBoxLayout()
        vb.addWidget(self.label_stats)
        vb.addWidget(self.dark_mode)
        hbox.addLayout(vb)

        layout.addLayout(hbox)
        layout.addWidget(self.marker_button)

        # plotting curves
        for c_name, curve in self.curves.items():
            p2d = self.add_curve(c_name, curve)

        # bound the LinearRegionItem to the plotted data
        self.region.setClipItem(p2d)

        # signals region
        self.region.sigRegionChanged.connect(self.update)
        self.p1.sigRangeChanged.connect(self.update_region)

        self.region.setRegion([1000, 2000])

        # crosshair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)

        self.vb = self.p1.vb
        self.p1.scene().sigMouseMoved.connect(self.mouse_moved)

        # plotting stats
        self.create_statistics(df)

        # MENU
        menu = QMenuBar()
        self.file_menu = menu.addMenu("&File")
        layout.setMenuBar(menu)

        # ACTION
        self.exit_button = QAction("&Exit", self)
        self.exit_button.setToolTip("Exit Program")

        # Add actions
        self.file_menu.addAction(self.exit_button)

        # SIGNALS Actions
        self.exit_button.triggered.connect(lambda: self.close())

        # Signals
        self.marker_button.setCheckable(True)
        self.stat_button.setCheckable(True)
        self.dark_mode.setCheckable(True)
        self.marker_button.clicked.connect(self.show_hide_markers)
        self.dark_mode.clicked.connect(self.change_dark_mode)

    def update(self):
        """Update the range to be seen."""
        self.region.setZValue(10)
        min_x, max_x = self.region.getRegion()
        self.p1.setXRange(min_x, max_x, padding=0)

    def update_region(self, window, view_range):
        """Update the region to be seen."""
        rgn = view_range[0]
        self.region.setRegion(rgn)

    def mouse_moved(self, evt):
        """Show the current position of mouse (x, y) and the correspondent y of each curve for such x."""
        if self.p1.sceneBoundingRect().contains(evt):
            mouse_point = self.vb.mapSceneToView(evt)
            index = int(mouse_point.x())
            if 0 < index < len(list(self.curves.values())[0]):
                # create one for each column that is checked
                s = f"<span style='font-size: 12pt'>x=%0.1f,   <span style='font-size: 12pt'>y=%0.1f</span>"
                args = [mouse_point.x(), mouse_point.y()]
                for curve in self.curves.keys():
                    if self.checkboxes[curve].isChecked():
                        s = s + f",   <span style='color: {self.plotted_curves[curve]['colour']}'>{curve}=%0.1f</span>"
                        args.append(self.curves[curve][index])
                self.label_mouse.setText(s % tuple(args))

            self.vLine.setPos(mouse_point.x())
            self.hLine.setPos(mouse_point.y())

    def add_curve(self, c_name, data_y):
        """Add each curve to plot_widget with random colours"""
        # set data x
        data_x = list(range(len(data_y)))

        # set random colour
        colour_r = random.choice(list(range(0, 255)))
        colour_g = random.choice(list(range(0, 255)))
        colour_b = random.choice(list(range(0, 255)))
        pen = pg.mkPen(color=(colour_r, colour_g, colour_b), width=3)

        # plot and save variable
        plot = self.p1.plot(data_x, data_y, name=c_name, pen=pen,
                            symbolBrush=(colour_r, colour_g, colour_b))
        plot.setSymbol(None)
        plot.setCurveClickable(True)
        plot.sigClicked.connect(lambda: self.curve_was_clicked(plot.name()))
        plot.visibleChanged.connect(self.view_changed)

        plot2 = self.p2.plot(data_x, data_y, name=c_name, pen=pen)
        plot2.visibleChanged.connect(self.view_changed)

        self.plotted_curves[c_name] = {'x': data_x, 'y': data_y, 'plot': plot,
                                       'plot2': plot2,
                                       "colour": f"rgb({colour_r}, {colour_g}, {colour_b})"}

        return plot2

    def curve_was_clicked(self, name):
        """Show statistics when curve is clicked."""
        self.label_stats.setText(f"<span style='color: {self.plotted_curves[name]['colour']}'>"
                                 f"{self.plotted_curves[name]['stats']}</span>")

    def view_changed(self):
        """Every time a plot is hidden using the legend buttons, the checkboxes must be updated."""
        for name, curve in self.plotted_curves.items():
            if curve["plot"].isVisible():
                self.checkboxes[name].setChecked(True)
            else:
                self.checkboxes[name].setChecked(False)

    def create_statistics(self, df):
        """Create string for statistics of each curve that will be plotted as label when curve is clicked."""
        for cbox in self.checkboxes.values():
            curve_name = cbox.text()
            self.plotted_curves[curve_name]["stats"] = f"{curve_name}<br>" \
                                                       f"Min: {df[curve_name].min()}<br>" \
                                                       f"Max: {df[curve_name].max()}<br>" \
                                                       f"Avg: {df[curve_name].median()}<br>" \
                                                       f"Mean: {df[curve_name].mean()}<br>" \
                                                       f"Std: {df[curve_name].std()}"

    def show_hide_curve(self):
        """Show or hide curve using checkboxes."""
        for cbox in self.checkboxes.values():
            if cbox.isChecked():
                self.plotted_curves[cbox.text()]["plot"].show()
                self.plotted_curves[cbox.text()]["plot2"].show()

            else:
                # hide curve
                self.plotted_curves[cbox.text()]["plot"].hide()
                self.plotted_curves[cbox.text()]["plot2"].hide()

        self.p1.autoRange()
        self.p2.autoRange()

    def show_hide_markers(self):
        """Show or hide markers of the visible curves, activated by a button."""
        if self.marker_button.isChecked():
            self.marker_button.setText("Hide markers")
            self.marker_button.setIcon(self.icon_hide_marker)
        else:
            self.marker_button.setText("Show markers")
            self.marker_button.setIcon(self.icon_show_marker)

        for cbox in self.checkboxes.values():
            if cbox.isChecked() and self.marker_button.isChecked():
                self.plotted_curves[cbox.text()]["plot"].setSymbol(random.choice(self.symbols))

            else:
                self.plotted_curves[cbox.text()]["plot"].setSymbol(None)

    def show_hide_stat(self):
        """Show or hide statistics lines of the visible curves, activated by a button."""
        if self.stat_button.isChecked():
            self.stat_button.setText("Hide Statistics")
            self.stat_button.setIcon(self.icon_cancel)
        else:
            self.stat_button.setText("Show Statistics")
            self.stat_button.setIcon(self.icon_stat)

        for cbox in self.checkboxes.values():
            if cbox.isChecked() and self.stat_button.isChecked():
                for stat in self.plotted_curves[cbox.text()]["stats"].values():
                    stat.show()
            else:
                for stat in self.plotted_curves[cbox.text()]["stats"].values():
                    stat.hide()

    def change_dark_mode(self):
        """Change graph background to dark or light mode."""
        if self.dark_mode.isChecked():
            self.label_stats.setStyleSheet("QLabel { background-color : rgb(242, 242, 242)}")
            self.win.setBackground((242, 242, 242))
        else:
            self.label_stats.setStyleSheet("QLabel { background-color : rgb(0, 0, 0)}")
            self.win.setBackground((0, 0, 0))
