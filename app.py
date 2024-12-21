from flask import Flask, request, jsonify
import datetime
from b3.service import read_stock_data, get_latest_price
app = Flask(__name__)

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
