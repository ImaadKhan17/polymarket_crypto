# collectors/closed_positions.py
import sys
sys.path.append('.')
import requests
from utils.db import insert_closed_position
from utils.config import CLOSED_POSITIONS_URL
import time

def fetch_closed_positions(wallet):
    closed_positions = []
    offset = 0
    while True:
        try:
            r = requests.get(
                f"{CLOSED_POSITIONS_URL}?user={wallet}&sortDirection=DESC&sortBy=TIMESTAMP&offset={offset}&limit=50"
            )
        except Exception as e:
            print(f"Request error: {e}, retrying...")
            time.sleep(2)
            continue

        if r.status_code == 429:
            print("Rate limited, sleeping...")
            time.sleep(5)
            continue

        if r.status_code != 200:
            print(f"[{wallet[:8]}] closed_positions error {r.status_code} at offset {offset}: {r.text[:200]}")
            break

        results = r.json()
        if not results:
            break

        closed_positions += results

        if len(results) < 50:
            break

        offset += 50

    print(f"[{wallet[:8]}] {len(closed_positions)} closed positions")

    for trade in closed_positions:
        if "Up or Down" in trade.get('title', ''):
            insert_closed_position({
                'wallet': trade['proxyWallet'],
                'timestamp': trade['timestamp'],
                'condition_id': trade['conditionId'],
                'title': trade['title'],
                'outcome': trade['outcome'],
                'avg_price': trade['avgPrice'],
                'realized_pnl': trade['realizedPnl']
            })