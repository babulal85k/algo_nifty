from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, sys, json
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
STATE_FILE = os.path.join(BASE_DIR, "runtime_state.json")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/candles")
def get_candles():
    from data_feed import get_index_candles

    df = get_index_candles()
    if df is None:
        return []

    candles = []
    for _, row in df.tail(100).iterrows():
        ts = row["time"]
        epoch = int(datetime.fromisoformat(ts).timestamp()) if isinstance(ts, str) else int(ts)

        candles.append({
            "time": epoch,
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
        })

    return candles

@app.get("/status")
def get_status():
    # File does not exist yet
    if not os.path.exists(STATE_FILE):
        return {
            "status": "NOT_RUNNING",
            "message": "State file not found"
        }

    # File exists but empty
    if os.path.getsize(STATE_FILE) == 0:
        return {
            "status": "STARTING",
            "message": "State file empty"
        }

    # Read state safely
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }