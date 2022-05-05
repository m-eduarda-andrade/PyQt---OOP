"""
File_name: plotwidget_scatter.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 21/12/2021

Scatter plot for covid cases/deaths in Germany.
"""


import pandas as pd

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow, QLabel, QWidget, QGridLayout, QVBoxLayout,
)
import pyqtgraph as pg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Corona scatter plot")
        self.plot_widget = pg.PlotWidget()

        df = pd.read_csv('covid_deutschland.csv', sep=',', parse_dates=[0])
        index = df.index.tolist()
        cases = df.new_cases.tolist()
        deaths = df.nd_10.tolist()

        points = list()

        # ordering data with color and size
        for i in index:
            spot_dic = {'pos': (cases[i], deaths[i]),
                        'pen': None,
                        'brush': ((i*255)/len(df), 200, (i*255)/len(df))
                        }

            points.append(spot_dic)

        self.plot_widget = pg.plot(name="Corona scatter plot")
        self.plot_widget.setLabel('bottom', 'Cases')
        self.plot_widget.setLabel('left', 'Deaths')

        scatter = pg.ScatterPlotItem(size=10)
        scatter.addPoints(points)
        self.plot_widget.addItem(scatter)

        # LAYOUT
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)

        # CONTAINER
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()