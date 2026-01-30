import datetime

# ===== FORCE TEST MODE =====
FORCE_TEST_MODE = False

# ===== MODE =====
DRY_RUN = True
LIVE_MODE = False

# ===== PAPER TRADING =====
PAPER_TRADING = True
VIRTUAL_CAPITAL = 2000000   # ₹20L paper money

# ===== CAPITAL (MUST MATCH VIRTUAL_CAPITAL) =====
CAPITAL = 2000000

# ===== INSTRUMENT =====
INDEX_SYMBOL = "NIFTY"
EXCHANGE = "NSE_FO"

# ===== OPTIONS SETTINGS =====
OPTION_TYPE_CALL = "CE"
OPTION_TYPE_PUT = "PE"

# ===== RISK RULES =====
RISK_PER_TRADE = 0.01
DAILY_MAX_LOSS = 0.02
MAX_TRADES_PER_DAY = 2

# ===== SL / TARGET =====
SL_PERCENT = 0.25
TARGET_PERCENT = 0.50

# ===== TIME WINDOWS =====
WINDOW_1_START = datetime.time(9, 20)
WINDOW_1_END   = datetime.time(10, 30)

WINDOW_2_START = datetime.time(13, 45)
WINDOW_2_END   = datetime.time(14, 30)

# ===== SCHEDULER =====
CHECK_INTERVAL_SECONDS = 30

# ===== STRATEGY TUNING (TEMP / TESTING) =====

MIN_BODY_PERCENT = 0.4     # candle body strength (was 0.6)
VOL_MULTIPLIER = 1.0       # volume / volatility filter (was 1.2)

# ===== FORCE EXIT =====
FORCE_EXIT = datetime.time(15, 15)

# ===== FILTERS =====
MIN_CANDLE_RANGE = 15
VOL_LOOKBACK = 10
VOL_MULTIPLIER = 1.2
MIN_BODY_PERCENT = 0.6


TRADE_START = datetime.time(9, 20)   # Market entry allowed from 9:20 AM
FORCE_EXIT  = datetime.time(15, 15)  # Force stop at 3:15 PM