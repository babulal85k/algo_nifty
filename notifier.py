import os
import requests
from dotenv import load_dotenv

# LOAD .env FILE
load_dotenv()

def send(msg):
    print(msg)

    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("❌ Telegram token or chat id not set")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={
        "chat_id": chat_id,
        "text": msg
    })