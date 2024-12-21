import datetime
from b3.repository import get_file
import re

def read_stock_data(ticker, year):
    """Read stock price data for a given ticker from the year's consolidated file."""
    lines = get_file(year)
    data = []

    # Iterate over each line and filter data by ticker
    for line in lines:
        line = line.strip()
        # Skip empty lines or lines that don't start with "01" (indicating valid quote data)
        if not line or not line.startswith("01"):
            continue

        # Extract the date and ticker from the line using the given positions:
        # Date starts at position 3 (YYYYMMDD) --> index 2 to 9
        # Ticker starts at position 13 (12 characters) --> index 12 to 23
        date_str = line[2:10]
        file_ticker = line[12:24].strip()  # 12 characters, strip any leading/trailing spaces

        # If the ticker matches, extract the price (assuming price is at a fixed position, e.g., 35-45)
        price = line[56:69].strip()  # Assuming price starts at index 34 and ends at 44

        if file_ticker == ticker:
            data.append({'date': date_str, 'price': price})

    return data


def get_latest_price(ticker):
    """Get the latest stock price for a given ticker."""
    today = datetime.date.today()
    year = today.year
    data = read_stock_data(ticker, year)

    # Get the latest price from the last entry in the list (simulating latest data)
    if data:
        latest_data = data[-1]
        return {'ticker': ticker, 'date': latest_data['date'], 'price': latest_data['price']}
    return None

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