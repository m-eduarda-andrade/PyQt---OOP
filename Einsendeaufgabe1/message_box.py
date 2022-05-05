"""
File_name: message_box.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 05/12/2021

File to define MessageBoxes, where it is displayed errors, warnings or information

"""

from PyQt5.QtWidgets import QMessageBox


class MessageBoxError(QMessageBox):
    """MessageBox for error in Separator modal: ValueError, KeyError or NameError"""
    def __init__(self, text):
        super().__init__()

        self.setIcon(QMessageBox.Critical)
        self.setText("Error")
        self.setInformativeText(text)
        self.setWindowTitle("Error")
        self.addButton(QMessageBox.StandardButton.Retry)
