"""
File_name: model.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 05/12/2021

Description: Create a table model based in Pandas dataframe to be displayed with Qt.
"""

import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt


class PandasModel(QAbstractTableModel):
    """Define an abstract table model for a Pandas dataframe."""
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.dataframe = df

    def rowCount(self, parent=None):
        return self.dataframe.shape[0]

    def columnCount(self, parent=None):
        return self.dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.dataframe.iloc[index.row(), index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.dataframe.columns[col]
        return None

    def append_row(self, row):
        """
        This function add new rows to a dynamic dataframe.
        :param row: row to be added in the Pandas dataframe.
        """
        self.dataframe.loc[len(self.dataframe)] = row
        self.layoutChanged.emit()
