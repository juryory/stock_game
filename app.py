from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_tables():
    conn = sqlite3.connect('stock_game.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS game_settings (
            setting_name TEXT PRIMARY KEY,
            value REAL NOT NULL
        )
    ''')

    # 为初始金额和单笔交易设定默认值
    c.execute('INSERT OR IGNORE INTO game_settings (setting_name, value) VALUES (?, ?)', ('initial_amount', 1000000))
    c.execute('INSERT OR IGNORE INTO game_settings (setting_name, value) VALUES (?, ?)', ('single_trade_amount', 100))

    c.execute('''
        CREATE TABLE IF NOT EXISTS player_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            trade_amount REAL DEFAULT 0,
            balance REAL DEFAULT 1000000,  -- 初始余额
            remaining_funds REAL DEFAULT 1000000,  -- 初始剩余资金
            total_balance REAL DEFAULT 1000000  -- 初始总余额
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect('stock_game.db')
    c = conn.cursor()

    if request.method == 'POST':
        for i in range(1, 11):
            price = request.form.get(f'price_{i}')
            if price:
                c.execute('INSERT OR REPLACE INTO stock_price (round, price) VALUES (?, ?)', (i, float(price)))
        conn.commit()

    c.execute('SELECT * FROM stock_price WHERE round BETWEEN 1 AND 10 ORDER BY round')
    raw_data = c.fetchall()

    # 计算涨幅
    all_rounds = []
    prev_price = None
    for i in range(1, 11):
        price = next((x[1] for x in raw_data if x[0] == i), None)
        if price and prev_price:
            increase = ((price - prev_price) / prev_price) * 100
        else:
            increase = None
        all_rounds.append((i, price, increase))
        prev_price = price

    c.execute('SELECT * FROM game_settings WHERE setting_name IN ("initial_amount", "single_trade_amount")')
    settings = c.fetchall()
    initial_amount = next((x[2] for x in settings if x[1] == "initial_amount"), None)
    single_trade_amount = next((x[2] for x in settings if x[1] == "single_trade_amount"), None)

    conn.close()
    return render_template('admin.html', all_rounds=all_rounds, initial_amount=initial_amount, single_trade_amount=single_trade_amount)

@app.route('/player')
def player():
    return render_template('player.html')

@app.route('/set_stock_prices', methods=['POST'])
def set_stock_prices():
    conn = sqlite3.connect('stock_game.db')
    c = conn.cursor()

    for i in range(1, 11):  # 假设你有10个回合
        price = request.form.get(f'price_{i}')
        if price:
            c.execute('INSERT OR REPLACE INTO stock_price (round, price) VALUES (?, ?)', (i, float(price)))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))


# @app.route('/set_stock_price', methods=['POST'])
# def set_stock_price():
#     round_number = request.form.get('round')
#     price = request.form.get('price')

#     conn = sqlite3.connect('stock_game.db')
#     c = conn.cursor()
    
#     c.execute('INSERT OR REPLACE INTO stock_price (round, price) VALUES (?, ?)', (round_number, price))
#     conn.commit()
#     conn.close()

#     return redirect(url_for('admin'))

@app.route('/trade', methods=['POST'])
def trade():
    player_name = request.form.get('player_name')
    trade_amount = request.form.get('trade_amount')
    # TODO: 这里我们需要进一步的逻辑来处理交易，如更新余额等。
    # 目前我们先简单地保存交易数据

    conn = sqlite3.connect('stock_game.db')
    c = conn.cursor()

    c.execute('INSERT INTO player_data (player_name, trade_amount) VALUES (?, ?)', (player_name, trade_amount))
    conn.commit()
    conn.close()

    return redirect(url_for('player'))

@app.route('/screen')
def screen():
    conn = sqlite3.connect('stock_game.db')
    c = conn.cursor()

    c.execute('SELECT * FROM player_data')
    players_data = c.fetchall()
    conn.close()

    return render_template('screen.html', players_data=players_data)

@app.route('/set_game_settings', methods=['POST'])
def set_game_settings():
    initial_amount = request.form.get('initial_amount')
    single_trade_amount = request.form.get('single_trade_amount')

    conn = sqlite3.connect('stock_game.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO game_settings (setting_name, value) VALUES (?, ?)', ("initial_amount", initial_amount))
    c.execute('INSERT OR REPLACE INTO game_settings (setting_name, value) VALUES (?, ?)', ("single_trade_amount", single_trade_amount))
    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
