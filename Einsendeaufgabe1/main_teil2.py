"""
File_name: main_teil2.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 07/12/2021

To run the Teil 2 of the exercise:
    $ cd Einsendeaufgabe1
    $ pip install -r requirements.txt
    $ python3 main_teil2.py

Description:
    The "My German Dictionary" is an application to add new unknown german words to a certain dataframe.
    There are several dataframes, each for the most used classes of words.
    When the application is opened, it is loaded already with the previous inserted data, saved on a .xlsx file: my_german_dictionary
    It is possible to save new changes and that will overwrite "my_german_dictionary" file.
    On my_german_dictionary.xlsx, the dataframes are saved in separated sheets, as displayed on the application.

    On adding a new word, the following fields are available:
        word: the word itself
        class: the grammatical class that the word belongs
        article: when the class is a noun, one must define the article.
        example: a sentence as example for that word.
        translation: the translation of this word to portuguese.

        Regex:
        This interface makes it easier to insert words, because, with the help of regex rules, it tries to predict the
        class of a word and its article based on german grammar structures. See more: german_rules_article.txt
        Regex rules are defined on service.py
"""

import sys

from PyQt5.QtWidgets import QApplication

from main_window import MainWindowPart2


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowPart2()
    window.show()
    app.exec_()
