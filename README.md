📈 NIFTY Options Paper Trading Algo (Upstox)
A safe, disciplined, paper-trading algo for NIFTY weekly options, built with:

✅ Real market data (Upstox)
✅ Fake money (paper trading)
✅ Strict risk management
✅ Daily loss lock
✅ Telegram alerts & daily summary
❌ No real money trading (by default)

This project is designed for testing, learning, and validation before any live deployment.

⚠️ IMPORTANT DISCLAIMER

This project is for educational and testing purposes only.
There is no guarantee of profit.
Options trading is high risk.
The author is not responsible for any financial loss.


🧠 WHAT THIS ALGO DOES

Monitors NIFTY index (5-minute candles)
Trades weekly ATM options (CE / PE)
Uses:

EMA-20 trend
Volatility filter
Momentum (strong candle body)


Trades only in selected time windows
Uses paper money (virtual capital)
Enforces:

Max trades/day
Max risk/trade
Daily loss lock


Sends:

Trade alerts
Exit alerts
Daily Telegram summary




🗂️ PROJECT STRUCTURE
nifty_options_paper_trading/
│
├── main.py               # Main algo loop
├── config.py             # All settings & risk rules
├── option_utils.py       # Option selection & filters
├── data_feed.py          # Index candle processing
├── upstox_client.py      # Real market data (Upstox)
├── execution.py          # Trade execution (paper)
├── paper_wallet.py       # Virtual wallet, PnL, locks
├── scheduler.py          # Market time logic
├── notifier.py           # Telegram alerts
│
├── requirements.txt      # Python dependencies
├── .gitignore            # Git safety rules
├── README.md             # This file
│
├── .env                  # 🔒 API keys (NOT committed)
└── STOP                  # 🛑 Emergency kill switch


🔑 PREREQUISITES

Python 3.9+
Git
Upstox developer account
Telegram bot + chat ID
Windows / Linux / macOS


🧪 STEP 1: CREATE VIRTUAL ENVIRONMENT
python -m venv venv
venv\Scripts\activate


📦 STEP 2: INSTALL DEPENDENCIES
pip install -r requirements.txt


🔐 STEP 3: SET UP ENVIRONMENT VARIABLES
Create a file named .env (this file is ignored by Git):
UPSTOX_API_KEY=your_upstox_api_key
UPSTOX_ACCESS_TOKEN=your_upstox_access_token

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

⚠️ Never commit .env

⚙️ STEP 4: CONFIGURATION (config.py)
Key settings you can adjust:
PAPER_TRADING = True
DRY_RUN = True
LIVE_MODE = False

CAPITAL = 2000000          # Paper capital
VIRTUAL_CAPITAL = 2000000  # Must match CAPITAL

RISK_PER_TRADE = 0.01      # 1%
DAILY_MAX_LOSS = 0.02      # 2%
MAX_TRADES_PER_DAY = 2

SL_PERCENT = 0.25          # 25%
TARGET_PERCENT = 0.50      # 50%

📌 Do NOT enable LIVE_MODE unless fully tested

▶️ STEP 5: RUN THE ALGO
python main.py

You should see:

Algo start message
Telegram alerts
Paper trade logs (when conditions match)


🛑 EMERGENCY STOP
To immediately stop the algo:
type nul > STOP

The algo will exit safely on the next loop.

🔒 RISK MANAGEMENT (BUILT-IN)



Rule
Description




Risk per trade
Fixed % of capital


Max trades/day
Hard limit


Daily loss lock
Trading stops after max loss


Time windows
Avoids chop & expiry chaos


Paper trading
Zero real money risk




📊 DAILY TELEGRAM SUMMARY (AUTOMATIC)
Sent once after market close:
📊 DAILY TRADING SUMMARY (PAPER)

Trades Taken: 2
Winning Trades: 1
Losing Trades: 1
Daily PnL: +₹18,450
Status: ✅ Within Risk
Virtual Balance: ₹20,18,450


🧪 RECOMMENDED TESTING PLAN

Run for 20–30 trading days
Observe:

Win rate
Avg win vs loss
Max drawdown
Silent days (no trades)


Do NOT rush to live trading


🔐 GIT SAFETY RULES (VERY IMPORTANT)

.env is ignored via .gitignore
Secrets are never committed
If secrets leak:

Rotate keys
Delete repo
Create new repo (clean)




🚀 NEXT POSSIBLE EXTENSIONS

CSV trade journal
Equity curve chart
Monthly performance report
Slippage simulation
VPS auto-deployment
Live trading (advanced, risky)


🧠 FINAL NOTE

If this algo is not profitable on paper,
it will not magically work with real money.

Paper trading is not a demo — it’s validation.

✅ STATUS
✔ Clean repo
✔ Secrets protected
✔ Risk controlled
✔ Ready for long-term testing

MAKE IT EXECUTABLE
On VPS:

chmod +x setup_and_run.sh
./setup_and_run.sh


🧠 HOW TO RUN ALGO IN BACKGROUND (IMPORTANT)
Use tmux (recommended)
Copy code
Bash
tmux new -s nifty
source venv/bin/activate
python main.py
Detach:
Copy code

Ctrl + B → D
Reattach later:
Copy code
Bash
tmux attach -t nifty

