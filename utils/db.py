import sys
sys.path.append('.')
import sqlite3 as sql3
from datetime import datetime, timezone
from utils.config import DB_PATH




def init_db():

    con = sql3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS traders (wallet_address TEXT PRIMARY KEY, rank INTEGER, weekly_pnl REAL, weekly_volume REAL, last_updated TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS trades (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_hash TEXT UNIQUE, wallet TEXT, timestamp TEXT, condition_id TEXT,title TEXT, outcome TEXT,  side TEXT, size REAL, usdc_size REAL, price REAL, inserted_at TEXT)")

    con.commit()
    
    con.close()

init_db()

def insert_trader(trader):

    con = sql3.connect(DB_PATH)
    cur = con.cursor()
    
    cur.execute("INSERT OR IGNORE INTO traders (wallet_address, rank, weekly_pnl, weekly_volume, last_updated) VALUES (?,?,?,?,?)", (trader['wallet_address'],trader['rank'],trader['weekly_pnl'],trader['weekly_volume'], datetime.now(timezone.utc).timestamp() ))
    con.commit()
    con.close()
def insert_trade(trade):

    con = sql3.connect(DB_PATH)
    cur = con.cursor()
    
    cur.execute("INSERT OR IGNORE INTO trades (transaction_hash, wallet, timestamp, condition_id, title, outcome, side, size, usdc_size, price, inserted_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                (trade['transaction_hash'],trade['wallet'],trade['timestamp'],trade['condition_id'], trade['title'], trade["outcome"], trade["side"],trade["size"], trade['usdc_size'], trade['price'], datetime.now(timezone.utc).timestamp() )
                )
    con.commit()
    con.close()

def get_wallets():
    con = sql3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT wallet_address FROM traders")
    rows = cur.fetchall()

    wallets = [row[0] for row in rows]

    con.close()

    return wallets

