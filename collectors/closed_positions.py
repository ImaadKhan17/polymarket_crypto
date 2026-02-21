import sys
sys.path.append('.')
import requests
from utils.db import insert_closed_position, get_wallets
from utils.config import CLOSED_POSITIONS_URL
import time 


def fetch_closed_positions(wallet):
    closed_positions = []
    offset = 0
    while True:
        try:
            r = requests.get(f"{CLOSED_POSITIONS_URL}?user={wallet}&title=Up%20or%20Down&sortDirection=DESC&offset={offset}&limit=50&sortBy=TIMESTAMP")
        except: 
            time.sleep(5)
            continue
        results = r.json()
        closed_positions += results
        if r.status_code != 200:
            time.sleep(5)
            continue
        if len(results)<50:
            break
      
        offset+=50
    
    print(len(closed_positions))
    
    for trade in closed_positions:
        insert_closed_position({'wallet':trade['proxyWallet'],
                        'timestamp':trade['timestamp'],'condition_id':trade['conditionId'],
                        'title':trade['title'],'outcome':trade['outcome'],
                        'avg_price':trade['avgPrice'],'realized_pnl':trade['realizedPnl']})

