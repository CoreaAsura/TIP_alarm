import pandas as pd
import requests
from datetime import datetime, timedelta
import os

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
CSV_PATH = "data/tip_new.csv"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

def check_new_tip_msgs():
    if not os.path.exists(CSV_PATH):
        return

    df = pd.read_csv(CSV_PATH)
    if "MSG_EPOCH" not in df.columns:
        return

    df["MSG_EPOCH"] = pd.to_datetime(df["MSG_EPOCH"], errors="coerce")
    now = datetime.utcnow()
    recent_msgs = df[df["MSG_EPOCH"] >= now - timedelta(hours=2)]

    if not recent_msgs.empty:
        msg = f"🚨 *신규 TIP MSG 감지됨!*\n최근 2시간 이내 메시지 수: {len(recent_msgs)}\n\n"
        for _, row in recent_msgs.iterrows():
            msg += f"- Object ID: `{row.get('NORAD_CAT_ID', 'N/A')}`\n  Epoch: `{row['MSG_EPOCH']}`\n"
        send_telegram_message(msg)

# Streamlit Cloud에서는 이 스크립트를 별도로 실행해야 함
if __name__ == "__main__":
    check_new_tip_msgs()
