import sys
sys.path.append('.')
import sqlite3 as sql3
from datetime import datetime, timezone

DB_PATH = './earnings.db'




def init_db():

    con = sql3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS earnings_market (market_id TEXT PRIMARY KEY, ticker TEXT, question TEXT, earnings_date TEXT, current_odds FLOAT, current_volume FLOAT, resolved BOOLEAN, outcome TEXT, estimated_eps FLOAT, actual_eps FLOAT, price_before FLOAT, price_after FLOAT, price_change_pct FLOAT, inserted_at TEXT )")
    cur.execute("CREATE TABLE IF NOT EXISTS odds_history (market_id TEXT, timestamp TEXT, odds FLOAT, volume FLOAT, UNIQUE (market_id, timestamp))")
    con.commit()
    
    con.close()
