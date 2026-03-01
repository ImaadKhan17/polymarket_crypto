import sys
sys.path.append('.')
import sqlite3 as sql3
from utils.config import DB_PATH

def get_win_rates():
    con = sql3.connect(DB_PATH)
    con.row_factory = sql3.Row
    cur = con.cursor()

    cur.execute("SELECT wallet, COUNT(*) as total, SUM(CASE WHEN realized_pnl>0 THEN 1 ELSE 0 END) as wins, ROUND(SUM(CASE WHEN  realized_pnl > 0 THEN 1 ELSE 0 END)*100/COUNT(*), 2) as win_rate FROM closed_positions GROUP BY wallet ORDER BY win_rate DESC")
    rows = cur.fetchall()
    
    results = [dict(row) for row in rows]

    con.close()
    
    return results

