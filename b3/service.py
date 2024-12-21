import datetime
from b3.repository import get_file
import re

def get_valid_tickers(tickers):
    tickers = tickers.split(',')
    tickers = filter(lambda ticker: re.fullmatch('[A-Z]{4}[0-9]{1,2}', ticker), tickers)
    tickers = set(tickers)
    return list(tickers)


def get_stocks_prices(tickers, dates):
    lines = get_file(dates[0].year)
    data = []

    for line in lines:
        if line[:2] != '01':
            continue

        if line[12:24].strip() not in tickers:
            continue

        if datetime.datetime.strptime(line[2:10], '%Y%m%d').date() not in dates:
            continue

        data.append(line)

    return data