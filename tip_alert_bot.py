import pandas as pd
import smtplib
import os
from datetime import datetime, timedelta
from email.mime.text import MIMEText

CSV_PATH = "data/tip_new.csv"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")         # 보내는 이메일 주소
EMAIL_PASS = os.getenv("EMAIL_PASS")         # 앱 비밀번호 또는 SMTP 비밀번호
EMAIL_TO = os.getenv("EMAIL_TO")             # 받는 이메일 주소

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

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
        body = f"🚨 신규 TIP MSG 감지됨!\n최근 2시간 이내 메시지 수: {len(recent_msgs)}\n\n"
        for _, row in recent_msgs.iterrows():
            body += f"- Object ID: {row.get('NORAD_CAT_ID', 'N/A')}\n  Epoch: {row['MSG_EPOCH']}\n"
        send_email("🚨 TIP MSG 알림", body)

if __name__ == "__main__":
    check_new_tip_msgs()
