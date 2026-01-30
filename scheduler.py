import datetime
import config
import time


def market_time_status():
    now = datetime.datetime.now().time()
    if now < config.TRADE_START or now > config.FORCE_EXIT:
        return "MARKET_CLOSED"
    return "MARKET_OPEN"


def wait_till_next_check():
    time.sleep(config.CHECK_INTERVAL_SECONDS)