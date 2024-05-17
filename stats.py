"""
Module to report on stats of output csv files. Used instead of some global counting.
"""
import csv

def count_ul_items(filename: str) -> int:
    with open(filename, "r", encoding="utf8") as f:
        csv_reader = csv.reader(f)
        counter = int()
        for row in csv_reader:
            if "<ul>" in row[1]:
                counter += 1
    return counter

def count_total_items(filename: str) -> int:
    with open(filename, "r", encoding="utf8") as f:
        csv_reader = csv.reader(f)
        counter = int()
        for row in csv_reader:
            counter += 1
    return counter

def get_report(filename: str) -> str:
    print(f"Lines that use HTML lists in file: {count_ul_items(filename)} (out of {count_total_items(filename)})")

if __name__ == '__main__':    
    get_report("output3.csv")
