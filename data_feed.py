import pandas as pd
from upstox_api_client import get_candles
import pandas as pd

INSTRUMENT_KEY = "NSE_INDEX|Nifty 50"

def get_index_candles():
    candles = get_candles("NSE_INDEX|Nifty 50")

    if not candles:
        return None

    df = pd.DataFrame(
        candles,
        columns=["time", "open", "high", "low", "close", "volume", "oi"]
    )

    return df