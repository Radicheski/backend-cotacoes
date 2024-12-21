from flask import Flask, jsonify
from b3.service import get_valid_tickers
app = Flask(__name__)

@app.route('/stocks/<tickers>', methods=['GET'])
def get_stock_price(tickers):
    tickers = get_valid_tickers(tickers)

    if tickers:
        return jsonify(tickers), 200
    else:
        return jsonify({'error': 'At least one valid ticker must be provided.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
