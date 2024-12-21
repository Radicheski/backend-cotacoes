from flask import Flask, jsonify, request
from b3.service import get_valid_tickers
from b3.repository import get_first_date, get_last_date
import datetime
app = Flask(__name__)

@app.route('/stocks/<tickers>', methods=['GET'])
def get_stock_price(tickers):
    tickers = get_valid_tickers(tickers)

    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    date = request.args.get('date')

    try:
        startDate = parse_date(startDate)
        endDate = parse_date(endDate)
        date = parse_date(date)
    except:
        return jsonify({'error': 'Invalid date'}), 400

    dates = set()

    if date and get_first_date() <= date <= get_last_date():
        dates.add(date)

    if startDate or endDate:
        dates = dates.union(get_date_range(startDate, endDate))

    if not dates:
        dates.add(get_last_date())

    dates = sorted(dates)

    if tickers:
        return jsonify([tickers, dates]), 200
    else:
        return jsonify({'error': 'At least one valid ticker must be provided.'}), 400

if __name__ == '__main__':
    app.run(debug=True)

def get_date_range(start=get_first_date(), end=get_last_date()):
    current = max(start, get_first_date()) if start else get_first_date()
    end = min(end, get_last_date()) if end else get_last_date()
    while current <= end:
        yield current
        current += datetime.timedelta(days=1)

def parse_date(date):
    if date:
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
    else:
        return None
