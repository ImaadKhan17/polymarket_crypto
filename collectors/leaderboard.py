import sys
sys.path.append('.')
import requests
from utils.db import insert_trader
from utils.config import LEADERBOARD_URL, DB_PATH
import sqlite3 as sql3


def fetch_leaderboard():
    r = requests.get(f"{LEADERBOARD_URL}?category=CRYPTO&timePeriod=WEEK&orderBy=PNL&limit=50")
    data = r.json()
    
    fresh_wallets = [trader["proxyWallet"] for trader in data]
    
    con = sql3.connect(DB_PATH)
    cur = con.cursor()
    placeholders = ','.join(['?' for _ in fresh_wallets])
    cur.execute(f"DELETE FROM traders WHERE wallet_address NOT IN ({placeholders})", fresh_wallets)
    con.commit()
    con.close()
    
    for trader in data:
        insert_trader({"wallet_address": trader["proxyWallet"], "rank": trader["rank"], "weekly_pnl": trader["pnl"], "weekly_volume": trader["vol"]})

    print(f"Inserted {len(data)} traders")
