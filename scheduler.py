import time
import datetime
from notifier import send
from config import (
    WINDOW_1_START,
    WINDOW_1_END,
    WINDOW_2_START,
    WINDOW_2_END,
    FORCE_EXIT
)

def is_within_trade_window(now):
    return (
        WINDOW_1_START <= now <= WINDOW_1_END
        or WINDOW_2_START <= now <= WINDOW_2_END
    )

def market_time_status():
    now = datetime.datetime.now().time()

    if now >= FORCE_EXIT:
        return "MARKET_CLOSED"

    if is_within_trade_window(now):
        return "TRADE_TIME"

    return "NO_TRADE_WINDOW"


def wait_till_next_check():
    time.sleep(300)  # 5 minutes