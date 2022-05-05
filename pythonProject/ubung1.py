import csv
import math


def __create_header_df(dataframe, siz_cols):
    for i in range(siz_cols):
        col_name = "dataset_" + str(i + 1)
        dataframe[col_name] = list()

    return dataframe


def main():
    f = open("data.csv")
    df = dict()
    first_process = True

    for line in f:
        cols = line.split(";")

        if first_process:
            df = __create_header_df(df, len(cols))
            first_process = False

        for i in range(len(cols)):
            col_name = "dataset_" + str(i + 1)
            num = float(cols[i].strip().replace(",", "."))
            df[col_name].append(num)

    print("\n\n", df, "\n\n")
    for col in df.keys():
        print(col)
        print(df[col], "\n")
        print("Max:", max(df[col]))
        print("Min:", min(df[col]))
        print("Avg:", sum(df[col])/len(df[col]))
        print("\n\n")


main()
