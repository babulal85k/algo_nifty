import math
import datetime


def round_to_atm(price):
    return int(round(price / 50) * 50)


def get_current_week_expiry():
    """
    Returns weekly expiry in Upstox format: YYMON
    Example: 24JAN
    """
    today = datetime.date.today()
    days_to_thursday = (3 - today.weekday()) % 7
    expiry_date = today + datetime.timedelta(days=days_to_thursday)
    return expiry_date.strftime("%y%b").upper()


def passes_volatility_filter(df, config):
    df = df.copy()

    df["range"] = df["high"] - df["low"]
    avg_range = df["range"].tail(config.VOL_LOOKBACK).mean()
    current_range = df.iloc[-1]["range"]

    if current_range < config.MIN_CANDLE_RANGE:
        return False

    if current_range < avg_range * config.VOL_MULTIPLIER:
        return False

    return True


def passes_momentum_filter(df, direction, config):
    last = df.iloc[-1]

    body = abs(last["close"] - last["open"])
    candle_range = last["high"] - last["low"]

    if candle_range == 0:
        return False

    body_ratio = body / candle_range

    if body_ratio < config.MIN_BODY_PERCENT:
        return False

    if direction == "CE" and last["close"] <= last["open"]:
        return False

    if direction == "PE" and last["close"] >= last["open"]:
        return False

    return True


def decide_direction(df):
    df = df.copy()
    df["ema20"] = df["close"].ewm(span=20).mean()
    last = df.iloc[-1]

    if last["close"] > last["ema20"] and last["close"] > last["open"]:
        return "CE"

    if last["close"] < last["ema20"] and last["close"] < last["open"]:
        return "PE"

    return None


def select_option(df, config):
    direction = decide_direction(df)
    if not direction:
        return None

    if not passes_volatility_filter(df, config):
        return None

    if not passes_momentum_filter(df, direction, config):
        return None

    nifty_price = df.iloc[-1]["close"]
    strike = round_to_atm(nifty_price)

    # Placeholder for sizing (real LTP fetched later)
    option_price = 100.0

    return {
        "symbol": "NIFTY",
        "strike": strike,
        "option_type": direction,
        "price": option_price
    }


def build_option_key(strike, option_type):
    expiry = get_current_week_expiry()
    return f"NSE_FO|NIFTY{expiry}{strike}{option_type}"