#!/usr/bin/env python3
import csv
import sys
import os
import pandas as pd
from difflib import SequenceMatcher
from test import *


def get_columns(file):
    colums = {}
    with open(file, "r") as f:
        for lines in f:
            splitted_line = lines.split(";")
            if (splitted_line[0][0] == "#" or splitted_line[0][0] == "\n"):
                continue
            if (splitted_line[-1][-1] == "\n" or splitted_line[-1][-1] == ";"):
                splitted_line[-1] = splitted_line[-1][:-1]
            colums[splitted_line[0]] = tuple(splitted_line[1:])
    return colums

def name_is_same(s1, s2):
    s1 = s1.upper()
    s2 = s2.upper()
    ratio = SequenceMatcher(None, s1, s2).ratio()
    if (ratio > 0.75):
        return True
    return False

def check_key(columns, column_name, new_row, df, source):
    new_file = []
    for index, row in df.iterrows():
        for key in columns["key"]:
             if (new_row[column_name.index(key)] == row[key] 
             and len(new_row[column_name.index(key)])) or (len(columns["key"]) > 1 and key != columns["key"][0]and len(new_row[column_name.index(key)]) and name_is_same(new_row[column_name.index(key)], row[key])):
                for i in range(len(row) - 1):
                    if (len(row[i]) == 0 and len(new_row[i]) > 0):
                        row[i] = new_row[i]
                        row[i + 1] = cut_path(source)
                return False
    return True

def iterate_csv(column_name, columns, df):
    for i in range(len(sys.argv)):
        if (i > 1):
            with open("final_" + cut_path(sys.argv[i]), "r", encoding="utf-8") as f_2:
                reader = csv.DictReader(f_2, delimiter=";")
                for row in reader:
                    new_row = []
                    for c_name in column_name:
                        appended = False
                        if c_name in row:
                            new_row.append(row[c_name])
                            if (len(row[c_name])):
                                new_row.append(sys.argv[i])
                            else:
                                new_row.append("")
                            appended = True
                        elif "_source" not in c_name:
                            for c_sy in columns[c_name]:
                                if c_sy in row:
                                    new_row.append(row[c_sy])
                                    new_row.append(cut_path(sys.argv[i]))
                                    appended = True
                                    break
                        if appended == False and "_source" not in c_name:
                            new_row.append("")
                            new_row.append("")
                    if check_key(columns, column_name, new_row, df, sys.argv[i]):
                        df.loc[len(df)] = new_row

def cut_path(path):
    splitted_path = path.split("/")
    return splitted_path[-1]

def file_to_utf(argv):
    i = 2
    while (i < len(argv)):
        with open(argv[i], 'r', encoding='utf-8', errors='ignore') as f, open("final_" + cut_path(argv[i]), "w") as outfile:
            inputs = csv.reader(f)
            output = csv.writer(outfile)
            for index, row in enumerate(inputs):
                output.writerow(row)
        i += 1

def consolidate():
    colums = get_columns(sys.argv[1])
    columns_name = [key for key in colums.keys() if key != "key"]
    j = 1
    for i in range(len(columns_name)):
        columns_name.insert(i + j, columns_name[i + j - 1] + "_source")
        j += 1
    df = pd.DataFrame(columns = columns_name)
    iterate_csv(columns_name, colums, df)
    df.to_csv("output.csv", sep=";", index=False)



def main():
    if (len(sys.argv) == 2 and sys.argv[1] == '-h'):
        print("\nHELP\n\n1. You need to provide at least 2 files.\n2. The priority of the file over the others are defined by it's position as an argument (first argument has the highest priority)\n3. The model of the outputed csv file must be defined in the model.txt file following the format specifeid in the model.txt file\n")
    elif (len(sys.argv) < 4):
        print("error: you need to provide at least one model file and two csv")
    else:
        priority = []
        for i in range(len(sys.argv)):
            if i != 0 and (i + 1) % 2 == 0 and os.path.isfile(sys.argv[i]) == False:
                print("error: argument {} is not a valid file".format(i))
                return
        file_to_utf(sys.argv)
        consolidate()
        for i in range(len(sys.argv)):
            if (i > 1):
                os.remove("final_" + cut_path(sys.argv[i]))
        

if __name__ == "__main__":
    main()    