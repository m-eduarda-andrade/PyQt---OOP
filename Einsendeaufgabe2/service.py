"""
File_name: service.py
Author: Maria Eduarda Costa Leite Andrade
Mat.Nr.: 6041979
Date: 05/12/2021

File to define services: functions used on the application
"""

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
