import sqlite3 as sql3
import os
from datetime import datetime, timezone
DB_PATH = "data/database.db"

con = sql3.connect(DB_PATH)
cur = con.cursor()

def init_db():

    cur.execute("CREATE TABLE IF NOT EXISTS traders (wallet_address TEXT PRIMARY KEY, rank INTEGER, weekly_pnl REAL, weekly_volume REAL, last_updated TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS trades (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_hash TEXT UNIQUE, wallet TEXT, timestamp TEXT, condition_id TEXT,title TEXT, outcome TEXT,  side TEXT, size REAL, usdc_size REAL, price REAL, inserted_at TEXT)")

    con.commit()

init_db()

def insert_trader(trader):
    
    
    cur.execute("INSERT INTO traders (wallet_address, rank, weekly_pnl, weekly_volume, last_updated) VALUES (?,?,?,?,?)", (trader['wallet_address'],trader['rank'],trader['weekly_pnl'],trader['weekly_volume'], datetime.now(timezone.utc).timestamp() ))
    con.commit()
def insert_trade(trade):
    
    cur.execute("INSERT INTO trades (transaction_hash, wallet, timestamp, condition_id, title, outcome, side, size, usdc_size, price, inserted_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                (trade['transaction_hash'],trade['wallet'],trade['timestamp'],trade['condition_id'], trade['title'], trade["outcome"], trade["side"], trade['usdc_size'], trade['price'], datetime.now(timezone.utc).timestamp() )
                )
    con.commit()

