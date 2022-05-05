"""
File_name: main_teil2.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 16/01/2022

Main file for an application that opens a .csv file, converts it to a dataframe and displays it
in table form or as graph using crosshair.

To run the Teil 2 of the exercise:
    $ cd Einsendeaufgabe2
    $ pip install -r requirements.txt
    $ python3 main_teil2.py
"""

import sys

from PyQt5.QtWidgets import QApplication
from main_window import MainWindowTeil2


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowTeil2()
    window.show()
    app.exec_()


