import sys
sys.path.append('.')
import requests
from utils.db import insert_trade
from utils.config import ACTIVITY_URL


def fetch_activity(wallet):
    activity = []
    offset = 0
    while True:
        r = requests.get(f"{ACTIVITY_URL}?user={wallet}&type=TRADE&sortDirection=ASC&offset={offset}&limit=500")
        if r.status_code != 200:
            print(f"Error: {r.status_code}")
            break
        results = r.json()
        activity += results
        if len(results)<500:
            break
      
        offset+=500
    
    for trade in activity:
        if "Up or Down" in trade['title']:
            insert_trade({'transaction_hash':trade['transactionHash'],'wallet':trade['proxyWallet'],
                          'timestamp':trade['timestamp'],'condition_id':trade['conditionId'],
                          'title':trade['title'],'outcome':trade['outcome'],
                          'side':trade['side'],'size':trade['size'],
                          'usdc_size':trade['usdcSize'],'price':trade['price'],})



