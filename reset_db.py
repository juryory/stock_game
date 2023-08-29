# reset_db.py
import sqlite3

def reset_database():
    conn = sqlite3.connect('stock_game.db')
    c = conn.cursor()

    c.execute('DELETE FROM player_data')
    c.execute('DELETE FROM stock_price')


    conn.close()

if __name__ == "__main__":
    reset_database()
