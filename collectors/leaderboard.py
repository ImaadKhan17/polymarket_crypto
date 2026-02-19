import sys
sys.path.append('.')
import requests
from utils.db import insert_trader
from utils.config import LEADERBOARD_URL

def fetch_leaderboard():
    r = requests.get(f"{LEADERBOARD_URL}?category=CRYPTO&timePeriod=WEEK&orderBy=PNL&limit=50")
    data = r.json()
    for trader in data:
        insert_trader({"wallet_address": trader["proxyWallet"], "rank": trader["rank"], "weekly_pnl":trader["pnl"], "weekly_volume":trader["vol"]})

    print(f"Inserted {len(data)} traders")

