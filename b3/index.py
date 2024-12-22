#!/usr/bin/python3
import datetime
import os
import json

DATA_DIR = os.environ.get('STOCK_DATA_DIR', '.')

startYear = 1986
endYear = (datetime.datetime.now() + datetime.timedelta(days=-1)).year

index = {}

for year in range(startYear, endYear + 1):
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
        print(date)

        index[date] = { 'startLine': i }

with open(os.path.join(DATA_DIR, 'index.json'), 'w') as f:
    f.write(json.dumps(index, indent=2))
