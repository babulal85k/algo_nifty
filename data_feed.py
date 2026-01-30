import pandas as pd
from upstox_api_client import get_candles
import pandas as pd

def get_index_candles():
    candles = get_candles("NSE_INDEX|Nifty 50")

    if not candles:
        return None   # 🔒 SAFE EXIT

    df = pd.DataFrame(
        candles,
        columns=["time", "open", "high", "low", "close", "volume", "oi"]
    )

    return df