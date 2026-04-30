# main.py
import sys
sys.path.append('.')
from utils.db import init_db, get_wallets
from collectors.activity import fetch_activity
from collectors.leaderboard import fetch_leaderboard
from collectors.closed_positions import fetch_closed_positions

init_db()
fetch_leaderboard()
wallets = get_wallets()

for wallet in wallets:  # removed the [3:] slice
    print(f'[{wallet[:8]}] fetching closed positions...')
    fetch_closed_positions(wallet)
    print(f'[{wallet[:8]}] fetching activity...')
    fetch_activity(wallet)