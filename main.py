import datetime
import os
import config

from notifier import send
from scheduler import market_time_status, wait_till_next_check
from data_feed import get_index_candles
from option_utils import select_option, build_option_key
from execution import execute_option_trade
from paper_wallet import check_exit, open_trade_data
from paper_wallet import is_daily_loss_locked
from upstox_api_client import get_option_ltp
from config import CAPITAL, RISK_PER_TRADE, MAX_TRADES_PER_DAY
import json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "runtime_state.json")

def write_state(state):
    state["last_update"] = datetime.datetime.now().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

trades_today = 0
current_day = datetime.date.today()
max_trade_logged = False


def reset_day():
    global trades_today, current_day, max_trade_logged
    if datetime.date.today() != current_day:
        trades_today = 0
        max_trade_logged = False
        current_day = datetime.date.today()
        send("🔄 New trading day (OPTIONS)")


def run():
    global trades_today, max_trade_logged

    send("🔥 NIFTY OPTIONS ALGO STARTED (PAPER TRADING)")

    while True:
        print(f"🕒 {datetime.datetime.now().strftime('%H:%M:%S')} | Checking market...")
        # 🛑 Emergency stop
        if os.path.exists("STOP"):
            send("🛑 STOP file detected. Exiting.")
            break

        write_state({
            "status": "RUNNING",
            "trades_today": trades_today,
            "open_trade": open_trade_data,
        })

        reset_day()
        status = market_time_status()

        if status == "MARKET_CLOSED":
            send("📴 Market closed. Options algo stopped.")
            break

        

        # 🔍 EXIT CHECK (VERY IMPORTANT)
        if open_trade_data:
            ltp = get_option_ltp(open_trade_data["key"])
            exited = check_exit(ltp)
            if exited:
                trades_today += 1
            wait_till_next_check()
            continue

        # 🔒 Max trades check
        if trades_today >= MAX_TRADES_PER_DAY:
            if not max_trade_logged:
                send("🔒 Max trades reached for today. Idling.")
                max_trade_logged = True
            wait_till_next_check()
            continue

        # 📊 Get market data
        df = get_index_candles()
        if df is None:
            wait_till_next_check()
            continue

        option = select_option(df, config)

        if not option:
            print("ℹ️ No valid setup found")
            send("ℹ️ No valid setup found")
            wait_till_next_check()
            continue

        # 📐 Position sizing
        risk_amount = CAPITAL * RISK_PER_TRADE
        sl_amount = option["price"] * config.SL_PERCENT
        qty = max(int(risk_amount / sl_amount), 1)

        # 🔑 Build real option key
        option_key = build_option_key(option["strike"], option["option_type"])

        if is_daily_loss_locked():
            wait_till_next_check()
            continue

        # 📄 PAPER ENTRY
        execute_option_trade(option_key, qty)

        wait_till_next_check()


if __name__ == "__main__":
    run()