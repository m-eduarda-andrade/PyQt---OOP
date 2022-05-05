"""
File_name: main_teil1.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 23/11/2021

Main file for an application that opens a .csv file, converts it to a dataframe and displays it.

To run the Teil 1 of the exercise:
    $ cd Einsendeaufgabe1
    $ pip install -r requirements.txt
    $ python3 main_teil1.py
"""

import sys

from PyQt5.QtWidgets import QApplication

from main_window import MainWindowPart1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowPart1()
    window.show()
    app.exec_()
