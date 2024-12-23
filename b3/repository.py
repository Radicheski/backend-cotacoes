import os
import datetime
from b3.index import read_index

DATA_DIR = os.environ.get('STOCK_DATA_DIR')

# Ensure the stock data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_file(year):
    file_name = f"{year}"
    file_path = os.path.join(DATA_DIR, file_name)

    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', encoding='cp1252') as file:
        lines = file.readlines()

    return lines

def get_last_date():
    index = read_index()
    last_date = max(index.keys())
    return datetime.datetime.strptime(last_date, "%Y%m%d").date()

def get_first_date():
    return datetime.date(1986, 1, 1)
