import datetime
import config
from notifier import send

balance = config.VIRTUAL_CAPITAL
open_trade_data = None

daily_pnl = 0.0
current_day = datetime.date.today()
daily_lock = False
winning_trades = 0
losing_trades = 0


def reset_day_if_needed():
    global daily_pnl, daily_lock, current_day
    global winning_trades, losing_trades

    if datetime.date.today() != current_day:
        daily_pnl = 0.0
        daily_lock = False
        winning_trades = 0
        losing_trades = 0
        current_day = datetime.date.today()
        send("🔄 Paper wallet reset for new trading day")


def is_daily_loss_locked():
    max_loss = config.CAPITAL * config.DAILY_MAX_LOSS
    return daily_pnl <= -max_loss


def open_trade(option_key, entry_price, qty, sl, target):
    global open_trade_data, daily_lock

    reset_day_if_needed()

    if is_daily_loss_locked():
        if not daily_lock:
            send("🛑 DAILY LOSS LIMIT HIT — Trading locked for today")
            daily_lock = True
        return False

    open_trade_data = {
        "key": option_key,
        "entry": entry_price,
        "qty": qty,
        "sl": sl,
        "target": target,
    }

    send(
        f"📄 PAPER BUY {option_key} @ {entry_price} | "
        f"Qty {qty} | SL {sl:.2f} | Target {target:.2f}"
    )
    return True


def check_exit(current_price):
    global open_trade_data, balance, daily_pnl
    global winning_trades, losing_trades

    if not open_trade_data:
        return False

    entry = open_trade_data["entry"]
    qty = open_trade_data["qty"]

    if current_price <= open_trade_data["sl"]:
        pnl = (current_price - entry) * qty
        _exit_trade(current_price, pnl, "SL")
        return True

    if current_price >= open_trade_data["target"]:
        pnl = (current_price - entry) * qty
        _exit_trade(current_price, pnl, "TARGET")
        return True

    return False


def _exit_trade(exit_price, pnl, reason):
    global balance, daily_pnl, open_trade_data
    global winning_trades, losing_trades

    balance += pnl
    daily_pnl += pnl

    if pnl >= 0:
        winning_trades += 1
    else:
        losing_trades += 1

    send(
        f"📄 PAPER EXIT ({reason}) @ {exit_price} | "
        f"PnL {pnl:.2f} | Daily {daily_pnl:.2f} | Balance {balance:.2f}"
    )

    open_trade_data = None