import pandas as pd
import smtplib
import os
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

CSV_PATH = "data/tip_new.csv"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

def send_email_with_attachment(subject, body, attachment_df):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    # 본문 추가
    msg.attach(MIMEText(body, "plain"))

    # CSV 파일 생성 및 첨부
    csv_bytes = attachment_df.to_csv(index=False).encode("utf-8")
    part = MIMEApplication(csv_bytes, Name="recent_tip_msg.csv")
    part["Content-Disposition"] = 'attachment; filename="recent_tip_msg.csv"'
    msg.attach(part)

    # 이메일 전송
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
        send_email_with_attachment("🚨 TIP MSG 알림", body, recent_msgs)

if __name__ == "__main__":
    check_new_tip_msgs()
