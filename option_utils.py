import math


def select_option(df, config):
    """
    Simple momentum-based option selector
    Returns dict or None
    """

    if df is None or len(df) < 3:
        return None

    last = df.iloc[-1]

    open_p = float(last["open"])
    close_p = float(last["close"])
    high_p = float(last["high"])
    low_p = float(last["low"])

    body = abs(close_p - open_p)
    candle_range = max(high_p - low_p, 0.01)
    body_percent = body / candle_range

    # ❌ Weak candle
    if body_percent < config.MIN_BODY_PERCENT:
        return None

    # Direction
    if close_p > open_p:
        option_type = "CE"
    else:
        option_type = "PE"

    # Strike rounding (nearest 50)
    strike = int(round(close_p / 50) * 50)

    return {
        "strike": strike,
        "option_type": option_type,
        "price": max(body * 2, 10)  # mock premium
    }


def build_option_key(strike, option_type):
    """
    Build Upstox-style option key
    """
    expiry = "26FEB"  # change later dynamically
    return f"NSE_FO|NIFTY{expiry}{strike}{option_type}"