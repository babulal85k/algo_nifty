from logging import config
from config import DRY_RUN, LIVE_MODE
from notifier import send
from paper_wallet import open_trade

import config
from paper_wallet import open_trade
from upstox_api_client import get_option_ltp

def execute_option_trade(option_key, qty):
    price = get_option_ltp(option_key)

    sl = price * (1 - config.SL_PERCENT)
    target = price * (1 + config.TARGET_PERCENT)

    open_trade(option_key, price, qty, sl, target)

def execute_option_trade(symbol, option_type, strike, qty, price):
    option = {
        "symbol": symbol,
        "option_type": option_type,
        "strike": strike,
        "price": price
    }

    if DRY_RUN and config.PAPER_TRADING:
        return open_trade(option, qty)

    send("🚫 Live trading disabled")
    return False