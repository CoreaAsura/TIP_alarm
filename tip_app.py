import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="TIP MSG Viewer", layout="wide")
st.title("위성추락경보 for MSSB")

CSV_PATH = "data/tip_new.csv"

TIP_COLUMNS = [
    "NORAD_CAT_ID", "MSG_EPOCH", "INSERT_EPOCH", "DECAY_EPOCH", "WINDOW", "REV",
    "DIRECTION", "LAT", "LON", "INCL", "NEXT_REPORT", "ID", "HIGH_INTEREST", "OBJECT_NUMBER"
]

# 데이터 로드 및 필터링
if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)

    # 누락 컬럼 채우기
    for col in TIP_COLUMNS:
        if col not in df.columns:
            df[col] = None
    df = df[TIP_COLUMNS]

    # MSG_EPOCH을 datetime으로 변환
    df["MSG_EPOCH"] = pd.to_datetime(df["MSG_EPOCH"], errors="coerce")

    # 현재 시간 기준으로 24시간 이내 데이터 필터링
    now = datetime.utcnow()
    recent_df = df[df["MSG_EPOCH"] >= now - timedelta(hours=24)]

    if not recent_df.empty:
        st.subheader("🕒 최근 24시간 이내 TIP MSG")
        st.dataframe(recent_df, use_container_width=True)

        # 📥 CSV 다운로드 버튼
        st.download_button(
            label="📥 최근 TIP MSG CSV 다운로드",
            data=recent_df.to_csv(index=False).encode("utf-8"),
            file_name="recent_tip_msg.csv",
            mime="text/csv"
        )
    else:
        st.info("✅ 최근 24시간 이내 TIP MSG는 없습니다.")
else:
    st.warning("TIP MSG 데이터 파일이 없습니다.")
