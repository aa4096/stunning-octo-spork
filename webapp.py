import redis, sqlite3, time
from flask import Flask, render_template, request, g, current_app

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0)

conn = sqlite3.connect('trades.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals (
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
        ticker,
        order_action,
        order_contracts,
        order_price
    )
""")
conn.commit()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('trades.db')
        g.db.row_factory = sqlite3.Row

    return g.db

@app.route('/', methods=['GET'])
def dashboard():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM signals
    """)
    signals = cursor.fetchall()

    # Test Signals
    # signals = [
    #     {
    #         "timestamp": None,
    #         "ticker": "Test1",
    #         "order_action": None,
    #         "order_contracts": None,
    #         "order_price": None,
    #     },
    #     {
    #         "timestamp": None,
    #         "ticker": "Test2",
    #         "order_action": None,
    #         "order_contracts": None,
    #         "order_price": None,
    #     },
    # ]

    return render_template('dashboard.html', signals=signals)


@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.data

    if data:

        # Redis connection to TradingView
        # r.publish('tradingview', data)

        data_dict = request.json

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO signals (ticker, order_action, order_contracts, order_price) 
            VALUES (?, ?, ?, ?)
        """, (data_dict['ticker'], 
                data_dict['order_action'], 
                data_dict['order_contracts'],
                data_dict['order_price']))

        db.commit()

        return data

    return {
        "code": "success",
        "signal": {
            "ticker": data_dict['ticker'],
            "order_action": data_dict['order_action'],
            "order_contracts": data_dict['order_contracts'],
            "order_price": data_dict['order_price'],
        }
    }