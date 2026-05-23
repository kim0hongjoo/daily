import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --------------------------
# 기본 설정
# --------------------------
st.set_page_config(
    page_title="주식 매매일지",
    layout="wide"
)

# 파일명
TRADE_FILE = "trades.csv"
WATCHLIST_FILE = "watchlist.csv"

# --------------------------
# CSV 파일 생성
# --------------------------

if not os.path.exists(TRADE_FILE):
    trade_df = pd.DataFrame(columns=[
        "날짜",
        "종목명",
        "매매유형",
        "매수이유",
        "매도이유",
        "수익률",
        "실수",
        "배운점"
    ])

    trade_df.to_csv(
        TRADE_FILE,
        index=False,
        encoding="utf-8-sig"
    )

if not os.path.exists(WATCHLIST_FILE):
    watch_df = pd.DataFrame(columns=[
        "종목명",
        "관심이유",
        "현재상태",
        "메모"
    ])

    watch_df.to_csv(
        WATCHLIST_FILE,
        index=False,
        encoding="utf-8-sig"
    )

# --------------------------
# 사이드바 메뉴
# --------------------------

st.sidebar.title("📌 메뉴")

page = st.sidebar.radio(
    "페이지 선택",
    [
        "매매일지 작성",
        "매매 기록",
        "관심종목 추가",
        "관심종목 보기",
        "통계"
    ]
)

# ====================================================
# 1. 매매일지 작성
# ====================================================

st.warning("저장된 매매기록이 없습니다.")