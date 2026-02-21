import sys
sys.path.append('.')
from utils.db import init_db
init_db()
from utils.db import get_wallets
from collectors.activity import fetch_activity
from collectors.leaderboard import fetch_leaderboard
from collectors.closed_positions import fetch_closed_positions

fetch_leaderboard()

wallets = get_wallets()

for wallet in wallets[3:]: 
    
    fetch_closed_positions(wallet)
    # fetch_activity(wallet)