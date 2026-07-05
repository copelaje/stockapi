FROM python:3.12-slim

# yfinance writes a small cache; give it a writable home for the non-root user.
ENV HOME=/home/app \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Run as an unprivileged user.
RUN useradd --create-home --home-dir /home/app app
USER app

EXPOSE 5000

# gunicorn serves the Flask `app` object from app.py. Two workers is plenty
# for a personal backend; a long timeout tolerates slow yfinance fetches.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
