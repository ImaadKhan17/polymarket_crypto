import sys
sys.path.append('.')
import requests
import time
import sqlite3 as sql3
from datetime import datetime, timezone
from utils.config import DB_PATH, ACTIVITY_URL
from backtest.win_rates import get_win_rates
from utils.db import insert_paper_trade
import pytz
import re
import threading 


def parse_end_time(title):
    ET = pytz.timezone('US/Eastern')
    
    if 'on ' in title.lower() and '?' in title:
        return None
    
    try:
        date_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d+),\s+', title)
        if not date_match:
            return None
        month_str = date_match.group(1)
        day = int(date_match.group(2))
        year = 2026
        month = datetime.strptime(month_str, '%B').month

        range_match = re.search(r'(\d+:\d+(?:AM|PM))-(\d+:\d+(?:AM|PM))', title)
        single_match = re.search(r'(\d+(?::\d+)?(?:AM|PM))\s+ET', title)

        if range_match:
            end_str = range_match.group(2)
        elif single_match:
            end_str = single_match.group(1)
        else:
            return None

        if ':' in end_str:
            end_dt = datetime.strptime(f"{month}/{day}/{year} {end_str}", '%m/%d/%Y %I:%M%p')
        else:
            end_dt = datetime.strptime(f"{month}/{day}/{year} {end_str}", '%m/%d/%Y %I%p')

        end_dt = ET.localize(end_dt)
        return int(end_dt.timestamp())

    except:
        return None

good_wallets = [w['wallet'] for w in get_win_rates() if w['total'] > 100 and w['win_rate'] > 50]

seen_hashes = set()
seen_hashes_lock = threading.Lock()

COIN_MAP = {
    "Bitcoin": ("XBTUSD", "XXBTZUSD"),
    "Ethereum": ("ETHUSD", "XETHZUSD"),
    "Solana": ("SOLUSD", "SOLUSD"),
    "XRP": ("XRPUSD", "XXRPZUSD")
}

TRADE_SIZE = 100

con = sql3.connect(DB_PATH)
con.execute("PRAGMA journal_mode=WAL")
cur = con.cursor()
cur.execute("SELECT condition_id, outcome FROM paper_trades")
rows = cur.fetchall()
con.close()

for row in rows:
    seen_hashes.add(row[0] + row[1])

print(f"Loaded {len(seen_hashes)} seen hashes")

def check_expiries():
    now = int(datetime.now(timezone.utc).timestamp())
    con = sql3.connect(DB_PATH)
    con.execute("PRAGMA journal_mode=WAL")
    con.row_factory = sql3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM paper_trades WHERE end_ts < ? AND status = 'open'", (now,))
    rows = cur.fetchall()

    for row in rows:
        coin_name = row['symbol']
        if coin_name not in COIN_MAP:
            continue
        pair, result_key = COIN_MAP[coin_name]
        kraken_response = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={pair}')
        data = kraken_response.json()
        if data['error']:
            continue

        exit_price = float(data['result'][result_key]['c'][0])
        entry_price = row['entry_price']

        if row['outcome'] == 'Up':
            pnl = (exit_price - entry_price) / entry_price * TRADE_SIZE
        else:
            pnl = (entry_price - exit_price) / entry_price * TRADE_SIZE

        cur.execute("""UPDATE paper_trades 
            SET exit_price=?, exit_ts=?, pnl=?, status='closed'
            WHERE id=?""",
            (exit_price, now, pnl, row['id']))
        
        print(f"[CLOSED] {row['wallet'][:8]} | {row['title']} | {row['outcome']} | entry: {entry_price} | exit: {exit_price} | pnl: ${pnl:.2f}")

    con.commit()
    con.close()

 
def poll_signals():
    while True:
        for wallet in good_wallets:
            try:
                response = requests.get(f'{ACTIVITY_URL}?user={wallet}&type=TRADE&sortDirection=DESC&limit=10')
                new_activity = response.json()
                for trade in new_activity:
                    if "Up or Down" not in trade.get('title', ''):
                        continue
                    if trade['side'] != 'BUY':
                        continue

                    key = trade['conditionId'] + trade['outcome']
                    
                    with seen_hashes_lock:
                        if key in seen_hashes:
                            continue
                        seen_hashes.add(key)

                    end_ts = parse_end_time(trade['title'])
                    if not end_ts or end_ts < int(datetime.now(timezone.utc).timestamp()):
                        continue

                    coin_type = re.search(r'^(.*?)\s+Up or Down', trade['title'])
                    coin_name = coin_type.group(1) if coin_type else None

                    if coin_name not in COIN_MAP:
                        continue

                    pair, result_key = COIN_MAP[coin_name]
                    kraken_response = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={pair}')
                    data = kraken_response.json()
                    if data['error']:
                        continue

                    price = float(data['result'][result_key]['c'][0])
                    insert_paper_trade({
                        'wallet': trade['proxyWallet'],
                        'title': trade['title'],
                        'symbol': coin_name,
                        'conditionId': trade['conditionId'],
                        'outcome': trade['outcome'],
                        'entry_price': price,
                        'entry_ts': int(datetime.now(timezone.utc).timestamp()),
                        'end_ts': end_ts
                    })
                    print(f"[SIGNAL] {trade['proxyWallet'][:8]} | {trade['title']} | {trade['outcome']} | {price}")
            except Exception as e:
                print(f"Error polling {wallet[:8]}: {e}")
        time.sleep(5)

def run_expiry_checker():
    while True:
        try:
            check_expiries()
        except Exception as e:
            print(f"Error in expiry checker: {e}")
        time.sleep(5)

signal_thread = threading.Thread(target=poll_signals, daemon=True)
expiry_thread = threading.Thread(target=run_expiry_checker, daemon=True)

signal_thread.start()
expiry_thread.start()

signal_thread.join()
expiry_thread.join()