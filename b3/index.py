#!/usr/bin/python3
import os
import json
import sys

DATA_DIR = os.environ.get('STOCK_DATA_DIR')

def process(year):
    index = read_index()

    file = os.path.join(DATA_DIR, str(year))
    lines = []
    with open(file, 'r', encoding='cp1252') as f:
        lines = f.readlines()

    date = None

    for i in range(len(lines)):
        if lines[i].startswith('00'):
            continue
        elif lines[i].startswith('99'):
            index[date]['file'] = year
            index[date]['endLine'] = i
            break

        newDate = lines[i][2:10]

        if newDate == date:
            continue

        if date:
            index[date]['file'] = year
            index[date]['endLine'] = i

        date = newDate

        index[date] = { 'startLine': i }

    save_index(index)

def read_index():
    with open(os.path.join(DATA_DIR, 'index.json'), 'r') as file:
        return json.load(file)

def save_index(index):
    with open(os.path.join(DATA_DIR, 'index.json'), 'w') as f:
        f.write(json.dumps(index, indent=2))


if __name__ == '__main__':
    process(sys.argv[1])
