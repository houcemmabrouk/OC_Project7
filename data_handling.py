import csv
import os
from typing import Dict, Any


def import_data(data_csv, length=None):
    dispo_stock_list = []
    with open(data_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        rows_imported = 0
        for row in reader:
            rows_imported += 1
            if (length and rows_imported <= length) or not length:
                dispo_stock_list.append((row['name'], float(row['price']), float(row['profit'])))
        return dispo_stock_list


def filter_and_sort_data(dispo_stock_list):
    # filter positive price
    dispo_stock_list = list(filter(lambda stock: stock[1] > 0, dispo_stock_list))
    # filter positive profit
    dispo_stock_list = list(filter(lambda stock: stock[2] > 0, dispo_stock_list))
    # remove duplicate
    dispo_stock_list = list(set(dispo_stock_list))
    # sort by profit
    dispo_stock_list = sorted(dispo_stock_list, key=lambda stock: stock[2], reverse=True)
    return dispo_stock_list


def write_in_csv(data_rows: Dict[str, Any], filename, writing_mode):
    fieldnames = data_rows.keys()
    file_exists = os.path.isfile(filename)
    with open(filename, writing_mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if file_exists is False:
            writer.writeheader()
        writer.writerow(data_rows)
