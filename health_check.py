"""
FULL SYSTEM HEALTH CHECK
Run this BEFORE market or deployment
"""

import os
import sys
import json
import datetime
import traceback

print("\n🔍 STARTING SYSTEM HEALTH CHECK\n")

FAILED = False

def ok(msg):
    print(f"✅ {msg}")

def fail(msg):
    global FAILED
    FAILED = True
    print(f"❌ {msg}")

# --------------------------------------------------
# 1️⃣ CONFIG CHECK
# --------------------------------------------------
try:
    import config
    ok("config.py loaded")

    required = [
        "CAPITAL", "RISK_PER_TRADE", "MAX_TRADES_PER_DAY",
        "SL_PERCENT", "TARGET_PERCENT"
    ]

    for k in required:
        if not hasattr(config, k):
            fail(f"Missing config value: {k}")
    ok("config values validated")
except Exception:
    fail("config.py error")
    traceback.print_exc()

# --------------------------------------------------
# 2️⃣ MARKET TIME CHECK
# --------------------------------------------------
try:
    from scheduler import market_time_status
    status = market_time_status()
    ok(f"market_time_status() → {status}")
except Exception:
    fail("scheduler.py error")
    traceback.print_exc()

# --------------------------------------------------
# 3️⃣ DATA FEED CHECK
# --------------------------------------------------
try:
    from data_feed import get_index_candles
    df = get_index_candles()

    if df is None or len(df) == 0:
        fail("No candle data returned")
    else:
        required_cols = {"open", "high", "low", "close"}
        if not required_cols.issubset(df.columns):
            fail("Candle dataframe missing columns")
        else:
            ok(f"Candles OK ({len(df)} rows)")
except Exception:
    fail("data_feed.py error")
    traceback.print_exc()

# --------------------------------------------------
# 4️⃣ OPTION SELECTION CHECK
# --------------------------------------------------
try:
    from option_utils import select_option
    opt = select_option(df, config)

    if opt is None:
        ok("No option selected (this can be valid)")
    else:
        for k in ["strike", "option_type", "price"]:
            if k not in opt:
                fail(f"Option missing field: {k}")
        ok("Option selection pipeline OK")
except Exception:
    fail("option_utils.py error")
    traceback.print_exc()

# --------------------------------------------------
# 5️⃣ PAPER WALLET CHECK
# --------------------------------------------------
try:
    from paper_wallet import open_trade, check_exit, open_trade_data

    test_key = "TEST|NIFTY26000CE"
    entry = 100
    qty = 10
    sl = 75
    target = 150

    opened = open_trade(test_key, entry, qty, sl, target)
    if not opened:
        fail("Paper trade did not open")
    else:
        ok("Paper trade opened")

    # simulate exit
    exited = check_exit(160)
    if not exited:
        fail("Paper trade did not exit on target")
    else:
        ok("Paper trade exit logic OK")
except Exception:
    fail("paper_wallet.py error")
    traceback.print_exc()

# --------------------------------------------------
# 6️⃣ RUNTIME STATE FILE CHECK
# --------------------------------------------------
try:
    STATE_FILE = "runtime_state.json"
    state = {
        "status": "TEST",
        "trades_today": 0,
        "open_trade": None,
        "last_update": datetime.datetime.now().isoformat()
    }

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

    with open(STATE_FILE) as f:
        loaded = json.load(f)

    if "status" not in loaded:
        fail("runtime_state.json invalid")
    else:
        ok("runtime_state.json write/read OK")
except Exception:
    fail("Runtime state error")
    traceback.print_exc()

# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------
print("\n==============================")
if FAILED:
    print("❌ SYSTEM HEALTH CHECK FAILED")
    print("Fix the above issues BEFORE running the algo.")
else:
    print("🟢 SYSTEM HEALTH CHECK PASSED")
    print("Safe to run PAPER trading.")
print("==============================\n")