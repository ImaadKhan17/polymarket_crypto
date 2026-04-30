import sys
sys.path.append('.')
import requests
import sqlite3
from utils.config import DB_PATH, BINANCE_URL
import time
from utils.db import insert_price
from datetime import datetime
import pytz



def fetch_prices(symbol, start_time, end_time):
    data=None
    while start_time<end_time:
        for attempt in range(3):
            try:
                r = requests.get(BINANCE_URL, params={
                    "symbol": symbol,
                    "interval": "1m",
                    "startTime": start_time,
                    "endTime": end_time,
                    "limit": 1000
                })
                if r.status_code == 200:
                    data = r.json()
                    break
                time.sleep(3)
            except:
                time.sleep(3)
        if not data:
            return

        for price in data:
            insert_price({"symbol": symbol, "timestamp": price[0], "open": price[1],"high":price[2], "low":price[3], "close":price[4] })
        
        start_time = data[-1][0] + 60000  # last candle timestamp + 1 minute


# end = int(time.time() * 1000)
# start = int(datetime(2025, 11, 1, tzinfo=ET).timestamp() * 1000)

# fetch_prices("BTCUSDT", start, end)

