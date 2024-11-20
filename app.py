from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

# Get the DATA_DIR from an environment variable, with a default value if not set
DATA_DIR = os.environ.get('STOCK_DATA_DIR', '.')

# Ensure the stock data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def read_stock_data(ticker, year):
    """Read stock price data for a given ticker from the year's consolidated file."""
    # Build the file path based on the year
    file_name = f"COTAHIST_A{year}.TXT"
    file_path = os.path.join(DATA_DIR, file_name)
    
    # If the file doesn't exist, return an empty list
    if not os.path.exists(file_path):
        return []
    
    data = []
    # Open the file and read its contents
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
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

@app.route('/stock/<ticker>', methods=['GET'])
def get_stock_price(ticker):
    """Return the latest stock price for the provided ticker."""
    date = request.args.get('date')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if date:
        # User requested a specific date
        try:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            year = date_obj.year
            data = read_stock_data(ticker, year)
            for entry in data:
                if entry['date'] == date.replace('-', ''):
                    return jsonify({'ticker': ticker, 'date': date, 'price': entry['price']})
            return jsonify({'error': 'Data not found for the given date'}), 404
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD'}), 400

    if start_date and end_date:
        # User requested a date range
        try:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            year = start_date_obj.year  # Assuming the same year for simplicity
            data = read_stock_data(ticker, year)
            
            results = []
            for entry in data:
                entry_date_obj = datetime.datetime.strptime(entry['date'], "%Y%m%d").date()
                if start_date_obj <= entry_date_obj <= end_date_obj:
                    results.append({'ticker': ticker, 'date': entry['date'], 'price': entry['price']})
            
            if results:
                return jsonify(results)
            return jsonify({'error': 'No data found for the given date range'}), 404
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD'}), 400

    # Return the latest stock price
    latest_price = get_latest_price(ticker)
    if latest_price:
        return jsonify(latest_price)
    
    return jsonify({'error': 'Ticker not found or no data available'}), 404

@app.route('/stocks', methods=['GET'])
def get_multiple_stock_prices():
    """Return the latest stock prices for multiple tickers, with optional date filtering."""
    tickers = request.args.get('tickers')
    date = request.args.get('date')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Parse the comma-separated list of tickers
    if not tickers:
        return jsonify({'error': 'No tickers provided'}), 400
    
    tickers = tickers.split(',')
    
    results = []
    
    for ticker in tickers:
        ticker = ticker.strip()  # Remove any leading/trailing spaces
        
        # Handle date filtering (specific date or date range)
        if date:
            # Specific date requested
            try:
                date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                year = date_obj.year
                data = read_stock_data(ticker, year)
                found = False
                for entry in data:
                    if entry['date'] == date.replace('-', ''):
                        results.append({'ticker': ticker, 'date': date, 'price': entry['price']})
                        found = True
                        break
                if not found:
                    results.append({'ticker': ticker, 'error': f'No data found for {ticker} on {date}'})
            except ValueError:
                results.append({'ticker': ticker, 'error': 'Invalid date format. Please use YYYY-MM-DD'})
        elif start_date and end_date:
            # Date range requested
            try:
                start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                year = start_date_obj.year  # Assuming same year for simplicity
                data = read_stock_data(ticker, year)
                
                found_data = []
                for entry in data:
                    entry_date_obj = datetime.datetime.strptime(entry['date'], "%Y%m%d").date()
                    if start_date_obj <= entry_date_obj <= end_date_obj:
                        found_data.append({'ticker': ticker, 'date': entry['date'], 'price': entry['price']})
                
                if found_data:
                    results.extend(found_data)
                else:
                    results.append({'ticker': ticker, 'error': f'No data found for {ticker} in the date range {start_date} to {end_date}'})
            except ValueError:
                results.append({'ticker': ticker, 'error': 'Invalid date format. Please use YYYY-MM-DD'})
        else:
            # No specific date or range, return the latest price
            latest_price = get_latest_price(ticker)
            if latest_price:
                results.append(latest_price)
            else:
                results.append({'ticker': ticker, 'error': 'No data found'})
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
