import sqlite3

def setup_database():
    conn = sqlite3.connect('stock_game.db')
    c = conn.cursor()

    # 创建股票价格表
    c.execute('''
    CREATE TABLE IF NOT EXISTS stock_price (
        round INTEGER PRIMARY KEY,
        price FLOAT
    )
    ''')

    # 创建选手交易数据表
    c.execute('''
    CREATE TABLE IF NOT EXISTS player_data (
        player_name TEXT NOT NULL,
        round INTEGER,
        trade_amount FLOAT,
        balance FLOAT,
        remaining_money FLOAT,
        total_balance FLOAT,
        PRIMARY KEY (player_name, round)
    )
    ''')

    conn.commit()
    conn.close()

setup_database()
