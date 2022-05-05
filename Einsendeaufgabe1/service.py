"""
File_name: service.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 05/12/2021

File to define services: functions used on the application
"""

import re

import pandas as pd


def __create_header_df(dataframe, cols):
    """
    Create a header for a dataframe

    :param dataframe: pandas dataframe
    :param cols: list of columns names

    :return: Pandas dataframe with header
    """
    for name in cols:
        dataframe[name] = list()

    return dataframe


def open_file(path, separator=",", decimal="."):
    """
    Open a .csv file

    :param path: absolute path of file to be opened
    :param separator: used for reading a .csv file
    :param decimal: used for comprehension of a decimal number

    :return: Pandas dataframe of the opened file
    """
    f = open(path)
    df = dict()
    first_process = True

    for line in f:
        cols = line.split(separator)

        if first_process:
            col_names = list()
            for i in cols:
                col_names.append(i.strip())

            df = __create_header_df(df, col_names)
            first_process = False

            continue

        for i in range(len(cols)):
            num = float(cols[i].strip().replace(decimal, "."))
            df[col_names[i]].append(num)

    return pd.DataFrame(df)


def get_statistics(df):
    """
    Calculate the statistics of a given Pandas dataframe.

    :param df: Pandas dataframe

    :return: statistics dataframe
    """

    res = {
        "Stat": {
            "Max": "Max",
            "Min": "Min",
            "Median": "Median",
            "Mean": "Mean",
            "Standard Deviation": "Standard Deviation"
        }
    }
    for col in df.columns.values:
        res[col] = {
            "Max": df[col].max(),
            "Min": df[col].min(),
            "Median": df[col].median(),
            "Mean": df[col].mean(),
            "Standard Deviation": df[col].std()
        }

    stat = pd.DataFrame(res)
    return stat


def regex_for_nouns(word):
    """
    Define regex rules to find the article of a given noun.

    :param word: noun.

    :return: macthed article or None.
    """
    male_suffixes = ("der", ["er", "ismus"])  # er from verbs, and ismus is always Der, others are most of times
    possible_male_suffixes = ("der", ["ant", "ling", "ner", "or"])
    female_suffixes = ("die", ["falt", "heit", "keit", "schaft", "t", "ung"])
    foreign_nouns_female_suffix = ("die", ["ade", "age", "anz", "enz", "ik", "ion", "tät", "ur"])
    possible_female_suffixes = ("die", ["e", "ei", "ie", "in"])
    neutral_suffixes = ("das", ["ial"])
    possible_neutral_suffixes = ("das", ["ment", "nis", "o", "tum", "um"])

    article = None
    for gender in [female_suffixes, male_suffixes, neutral_suffixes,
                   foreign_nouns_female_suffix, possible_female_suffixes,
                   possible_male_suffixes, possible_neutral_suffixes]:
        for suffix in gender[1]:
            if re.match(f"^[A-ZÄÖÜ][a-zäöüß]*{suffix}$", word):
                article = gender[0]
                break
        else:
            continue
        break
    return article


def regex_for_adjectives(word):
    """
    Define regex rules to find if a given word is an adjective.
    Attention: adjectives and adverbs cannot be differentiated in german. Here it is always defined as adjective.

    :param word: any given word that is not a noun.

    :return: macthed adjective or None.
    """
    adjective_suffixes = ["haft", "los", "ig", "isch", "lich", "arm", "frei", "leer", "reich", "voll",
                          "fest", "sam", "gemäß", "ant", "bar"]

    adjective = None
    for suffix in adjective_suffixes:
        if re.match(f"^[a-zäöüß]*{suffix}$", word):
            adjective = suffix
            break

    return adjective


def regex_for_verbs(word):
    """
    Define regex rules to find if a given word is a verb.

    :param word: any given word that is not a noun.

    :return: String "verb": if verb was found. None: if there was no match.
    """
    if re.match(f"^[a-zäöüß]+en$", word) or re.match(f"^[a-zäöüß]+n$", word):
        return "verb"
    return None
