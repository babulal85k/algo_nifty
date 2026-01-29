import os
import datetime
from dotenv import load_dotenv

import upstox_client
from upstox_client.rest import ApiException

load_dotenv()

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise RuntimeError("❌ UPSTOX_ACCESS_TOKEN missing in .env")


# ===== API CONFIG (UPSTOX V2 SDK) =====
configuration = upstox_client.Configuration()
configuration.access_token = ACCESS_TOKEN

api_client = upstox_client.ApiClient(configuration)

market_api = upstox_client.MarketQuoteApi(api_client)
history_api = upstox_client.HistoryApi(api_client)


# =====================================================
# 📊 GET INDEX CANDLES (REAL DATA)
# =====================================================
def get_candles(instrument_key, interval="5minute"):
    to_date = datetime.datetime.now()
    from_date = to_date - datetime.timedelta(minutes=300)

    try:
        response = history_api.get_historical_candle_data(
            instrument_key=instrument_key,
            interval=interval,
            from_date=from_date.strftime("%Y-%m-%d"),
            to_date=to_date.strftime("%Y-%m-%d")
        )
        return response.data.candles
    except ApiException as e:
        print("❌ Candle fetch error:", e)
        return []


# =====================================================
# 💰 GET OPTION LTP (REAL PRICE)
# =====================================================
def get_option_ltp(instrument_key):
    try:
        response = market_api.ltp(instrument_key)
        return float(response.data[instrument_key].last_price)
    except ApiException as e:
        raise RuntimeError(f"❌ LTP fetch failed for {instrument_key}: {e}")