import sys
sys.path.append('.')
from utils.db import get_wallets
from collectors.activity import fetch_activity
from collectors.leaderboard import fetch_leaderboard


fetch_leaderboard()

wallets = get_wallets()

for wallet in wallets: 
    fetch_activity(wallet)