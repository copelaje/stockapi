"""Tiny web API over yfinance: latest available price + date for a ticker.

Intended as a personal backend for KMyMoney's online quote feature.
Returns JSON. See README.md for the KMyMoney source configuration.
"""

from flask import Flask, jsonify

import yfinance as yf

app = Flask(__name__)


def latest_quote(ticker: str) -> dict:
    """Return the most recent available close price and its trading date.

    Uses the daily history (last few sessions) so the price is always paired
    with the actual date it was observed, which is what a portfolio tool wants.
    """
    ticker = ticker.strip().upper()
    tk = yf.Ticker(ticker)

    hist = tk.history(period="5d", auto_adjust=False)
    if hist.empty:
        return {"symbol": ticker, "error": "no data for symbol"}

    row = hist.iloc[-1]
    when = hist.index[-1]

    currency = None
    try:
        currency = tk.fast_info.get("currency")
    except Exception:
        pass

    return {
        "symbol": ticker,
        "price": round(float(row["Close"]), 4),
        "date": when.strftime("%Y-%m-%d"),
        "currency": currency,
    }


@app.route("/quote/<ticker>")
def quote(ticker):
    try:
        result = latest_quote(ticker)
    except Exception as exc:  # network / yfinance failure
        return jsonify({"symbol": ticker.upper(), "error": str(exc)}), 502

    if "error" in result:
        return jsonify(result), 404
    return jsonify(result)


@app.route("/")
def index():
    return jsonify({
        "service": "stockapi",
        "usage": "GET /quote/<ticker>  e.g. /quote/AAPL",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
