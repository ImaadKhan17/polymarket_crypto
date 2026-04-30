# collectors/activity.py
import sys
sys.path.append('.')
import requests
from utils.db import insert_trade
from utils.config import ACTIVITY_URL
import time

def fetch_activity(wallet):
    activity = []
    offset = 0
    while True:
        try:
            r = requests.get(
                f"{ACTIVITY_URL}?user={wallet}&type=TRADE&sortDirection=DESC&offset={offset}&limit=500"
            )
            print(r.url)
        except Exception as e:
            print(f"Request error: {e}, retrying...")
            time.sleep(2)
            continue

        if r.status_code == 429:
            print("Rate limited, sleeping...")
            time.sleep(5)
            continue

        if r.status_code != 200:
            print(f"[{wallet[:8]}] activity error {r.status_code} at offset {offset}: {r.text[:200]}")
            break

        results = r.json()
        if not results:
            break

        activity += results

        if len(results) < 500:
            break

        offset += 500
        if offset >= 3000:  # API hard cap
            break

    print(f"[{wallet[:8]}] {len(activity)} activity records")

    for trade in activity:
        if "Up or Down" in trade.get('title', ''):
            insert_trade({
                'transaction_hash': trade['transactionHash'],
                'wallet': trade['proxyWallet'],
                'timestamp': trade['timestamp'],
                'condition_id': trade['conditionId'],
                'title': trade['title'],
                'outcome': trade['outcome'],
                'side': trade['side'],
                'size': trade['size'],
                'usdc_size': trade['usdcSize'],
                'price': trade['price'],
            })