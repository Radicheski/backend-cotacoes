import os

DATA_DIR = os.environ.get('STOCK_DATA_DIR', '.')

# Ensure the stock data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_file(year):
    # Build the file path based on the year
    file_name = f"COTAHIST_A{year}.TXT"
    file_path = os.path.join(DATA_DIR, file_name)

    # If the file doesn't exist, return an empty list
    if not os.path.exists(file_path):
        return []

    # Open the file and read its contents
    with open(file_path, 'r') as file:
        lines = file.readlines()

    return lines