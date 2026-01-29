import pandas as pd
from upstox_client import get_candles

INSTRUMENT_KEY = "NSE_INDEX|Nifty 50"

def get_index_candles():
    candles = get_candles(INSTRUMENT_KEY)

    df = pd.DataFrame(
        candles,
        columns=["time", "open", "high", "low", "close", "volume", "_"]
    )

    df = df.astype({
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float
    })

    return df.tail(60)