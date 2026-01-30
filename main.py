from diagnostics import log, checkpoint

import datetime
import os
import json
import config

from notifier import send
from scheduler import market_time_status, wait_till_next_check
from data_feed import get_index_candles
from option_utils import select_option, build_option_key
from execution import execute_option_trade
from upstox_api_client import get_option_ltp

import paper_wallet
from config import CAPITAL, RISK_PER_TRADE, MAX_TRADES_PER_DAY


# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "runtime_state.json")


# =====================================================
# RUNTIME STATE
# =====================================================

trades_today = 0
current_day = datetime.date.today()
max_trade_logged = False


# =====================================================
# STATE WRITER (UI / API)
# =====================================================

def write_state():
    state = {
        "status": "RUNNING",
        "trades_today": trades_today,
        "open_trade": paper_wallet.open_trade_data,
        "last_update": datetime.datetime.now().isoformat(),
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# =====================================================
# DAILY RESET
# =====================================================

def reset_day():
    global trades_today, current_day, max_trade_logged

    if datetime.date.today() != current_day:
        trades_today = 0
        max_trade_logged = False
        current_day = datetime.date.today()
        send("🔄 New trading day (OPTIONS)")
        log("DAY", "New trading day detected, counters reset")


# =====================================================
# MAIN LOOP
# =====================================================

def run():
    global trades_today, max_trade_logged

    send("🔥 NIFTY OPTIONS ALGO STARTED (PAPER TRADING)")
    log("START", "Algo started in PAPER mode")

    while True:
        log("LOOP", "New loop iteration started")
        print(f"🕒 {datetime.datetime.now().strftime('%H:%M:%S')} | Checking market...")

        # -------------------------------------------------
        # Emergency STOP
        # -------------------------------------------------
        if os.path.exists("STOP"):
            send("🛑 STOP file detected. Exiting.")
            log("STOP", "STOP file detected, exiting")
            break

        write_state()
        reset_day()

        # -------------------------------------------------
        # Market time check
        # -------------------------------------------------
        status = market_time_status()
        log("MARKET", "Market status checked", {"status": status})

        if status == "MARKET_CLOSED":
            send("📴 Market closed. Options algo stopped.")
            log("MARKET", "Market closed, stopping algo")
            break

        # -------------------------------------------------
        # Exit check (if trade open)
        # -------------------------------------------------
        if paper_wallet.open_trade_data:
            log("EXIT", "Checking open trade for exit", paper_wallet.open_trade_data)

            ltp = get_option_ltp(paper_wallet.open_trade_data["key"])
            exited = paper_wallet.check_exit(ltp)

            if exited:
                trades_today += 1
                log("EXIT", "Trade exited", {"trades_today": trades_today})

            wait_till_next_check()
            continue

        # -------------------------------------------------
        # Max trades per day
        # -------------------------------------------------
        if trades_today >= MAX_TRADES_PER_DAY:
            if not max_trade_logged:
                send("🔒 Max trades reached for today. Idling.")
                log("RISK", "Max trades per day reached")
                max_trade_logged = True

            wait_till_next_check()
            continue

        # -------------------------------------------------
        # Fetch market data
        # -------------------------------------------------
        df = get_index_candles()

        if not checkpoint(
            "DATA",
            df is not None and len(df) > 0,
            "Index candles available",
            {"rows": 0 if df is None else len(df)}
        ):
            wait_till_next_check()
            continue

        # -------------------------------------------------
        # Strategy decision
        # -------------------------------------------------
        option = select_option(df, config)

        if not checkpoint(
            "STRATEGY",
            option is not None,
            "Valid option setup found",
            option
        ):
            wait_till_next_check()
            continue

        # -------------------------------------------------
        # Risk & position sizing
        # -------------------------------------------------
        risk_amount = CAPITAL * RISK_PER_TRADE
        sl_amount = option["price"] * config.SL_PERCENT
        qty = max(int(risk_amount / sl_amount), 1)

        log("RISK", "Position sizing calculated", {
            "risk_amount": risk_amount,
            "sl_amount": sl_amount,
            "qty": qty
        })

        # -------------------------------------------------
        # Daily loss lock
        # -------------------------------------------------
        if not checkpoint(
            "RISK",
            not paper_wallet.is_daily_loss_locked(),
            "Daily loss lock check"
        ):
            wait_till_next_check()
            continue

        # -------------------------------------------------
        # Build option key
        # -------------------------------------------------
        option_key = build_option_key(option["strike"], option["option_type"])

        log("TRADE", "Placing PAPER trade", {
            "option_key": option_key,
            "qty": qty
        })

        # -------------------------------------------------
        # Paper entry
        # -------------------------------------------------
        execute_option_trade(option_key, qty)

        wait_till_next_check()


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    run()