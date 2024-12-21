import os
import datetime

DATA_DIR = os.environ.get('STOCK_DATA_DIR', '.')

# Ensure the stock data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_file(year):
    file_name = f"COTAHIST_A{year}.TXT"
    file_path = os.path.join(DATA_DIR, file_name)

    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    return lines

def get_last_date():
    return datetime.date.today() + datetime.timedelta(days=-1)

def get_first_date():
    return datetime.date(1986, 1, 1)
