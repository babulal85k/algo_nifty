import os
import datetime
from upstox_api.api import Upstox
from dotenv import load_dotenv

load_dotenv()

# ===== AUTH =====
API_KEY = os.getenv("UPSTOX_API_KEY")
ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

if not API_KEY or not ACCESS_TOKEN:
    raise RuntimeError("❌ Upstox API credentials not found in environment")

u = Upstox(API_KEY, ACCESS_TOKEN)
u.get_master_contract('NSE_EQ')
u.get_master_contract('NSE_FO')


# ======================================================
# 📊 FETCH INDEX CANDLES (REAL DATA)
# ======================================================
def get_candles(instrument_key, interval="5minute"):
    """
    Returns last 60 candles in format:
    [time, open, high, low, close, volume, oi]
    """

    now = datetime.datetime.now()
    from_date = now - datetime.timedelta(minutes=60 * 5)

    # Upstox expects instrument token, not key string
    # Example token for NIFTY index:
    # NSE_INDEX|Nifty 50 → token is resolved internally

    candles = u.get_ohlc(
        instrument_key,
        interval,
        from_date,
        now
    )

    formatted = []
    for c in candles:
        formatted.append([
            c['timestamp'],
            float(c['open']),
            float(c['high']),
            float(c['low']),
            float(c['close']),
            float(c['volume']),
            0
        ])

    return formatted


# ======================================================
# 💰 FETCH REAL OPTION LTP
# ======================================================
def get_option_ltp(instrument_key):
    """
    Returns real option last traded price
    """

    quote = u.get_live_feed(instrument_key, 'LTP')

    if not quote or 'ltp' not in quote:
        raise RuntimeError(f"❌ Failed to fetch LTP for {instrument_key}")

    return float(quote['ltp'])