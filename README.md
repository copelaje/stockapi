# stockapi

A tiny web API over [yfinance](https://pypi.org/project/yfinance/) that returns
the latest available price and trading date for a stock ticker as JSON. Meant as
a personal backend for KMyMoney's online price quotes.

## Run

```bash
./venv/bin/python app.py
# serves on http://127.0.0.1:5000
```

Or via flask:

```bash
./venv/bin/flask --app app run
```

## Endpoint

```
GET /quote/<ticker>
```

Example:

```bash
curl http://127.0.0.1:5000/quote/AAPL
```

```json
{"symbol": "AAPL", "price": 308.63, "date": "2026-07-02", "currency": "USD"}
```

- `price` is the most recent available **closing** price.
- `date` is the actual trading date that price was observed (YYYY-MM-DD).
- Unknown symbol → HTTP 404 with `{"error": ...}`.
- Upstream/network failure → HTTP 502 with `{"error": ...}`.

## KMyMoney configuration

Settings → Configure KMyMoney → Online Quotes → New source:

- **URL:** `http://localhost:5000/quote/%1`
  (`%1` is substituted with the security's symbol)
- **Price regex:** `"price":\s*([0-9.]+)`
- **Date regex:** `"date":\s*"([0-9]+)-([0-9]+)-([0-9]+)"`
- **Date format:** `%y %m %d`

Then, on a security/equity's *Online update* settings, choose this source as the
Online source. KMyMoney fetches the URL and applies the regexes to the JSON body.

## Notes

- Binds to `127.0.0.1` only. To query from another machine on your LAN, change
  `host` in `app.py` to `"0.0.0.0"`.
- Uses Flask's built-in dev server, which is fine for single-user local use. For
  something longer-running, put it behind `waitress`/`gunicorn`.
