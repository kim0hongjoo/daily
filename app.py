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
# 사이드바
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
# 매매일지 작성
# ====================================================

if page == "매매일지 작성":

    st.title("📈 주식 매매일지 작성")

    date = st.date_input(
        "날짜",
        datetime.today()
    )

    stock = st.text_input("종목명")

    trade_type = st.selectbox(
        "매매유형",
        ["스윙", "단타", "중장기"]
    )

    buy_reason = st.text_area("매수 이유")

    sell_reason = st.text_area("매도 이유")

    profit = st.number_input(
        "수익률 (%)",
        step=0.1
    )

    mistake = st.text_area("실수")

    lesson = st.text_area("배운점")

    if st.button("💾 저장하기"):

        new_data = pd.DataFrame([{
            "날짜": date,
            "종목명": stock,
            "매매유형": trade_type,
            "매수이유": buy_reason,
            "매도이유": sell_reason,
            "수익률": profit,
            "실수": mistake,
            "배운점": lesson
        }])

        old_df = pd.read_csv(TRADE_FILE)

        updated_df = pd.concat(
            [old_df, new_data],
            ignore_index=True
        )

        updated_df.to_csv(
            TRADE_FILE,
            index=False,
            encoding="utf-8-sig"
        )

        st.success("저장 완료!")

# ====================================================
# 매매 기록
# ====================================================

elif page == "매매 기록":

    st.title("📋 매매 기록")

    df = pd.read_csv(TRADE_FILE)

    if len(df) > 0:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("저장된 매매기록이 없습니다.")

# ====================================================
# 관심종목 추가
# ====================================================

elif page == "관심종목 추가":

    st.title("⭐ 관심종목 추가")

    watch_stock = st.text_input("종목명")

    reason = st.text_area("관심 이유")

    status = st.selectbox(
        "현재 상태",
        [
            "관찰중",
            "매수대기",
            "보유중",
            "매도완료"
        ]
    )

    memo = st.text_area("메모")

    if st.button("➕ 관심종목 저장"):

        new_watch = pd.DataFrame([{
            "종목명": watch_stock,
            "관심이유": reason,
            "현재상태": status,
            "메모": memo
        }])

        old_watch = pd.read_csv(WATCHLIST_FILE)

        updated_watch = pd.concat(
            [old_watch, new_watch],
            ignore_index=True
        )

        updated_watch.to_csv(
            WATCHLIST_FILE,
            index=False,
            encoding="utf-8-sig"
        )

        st.success("관심종목 저장 완료!")

# ====================================================
# 관심종목 보기
# ====================================================

elif page == "관심종목 보기":

    st.title("📌 관심종목 리스트")

    watch_df = pd.read_csv(WATCHLIST_FILE)

    if len(watch_df) > 0:
        st.dataframe(
            watch_df,
            use_container_width=True
        )
    else:
        st.warning("관심종목이 없습니다.")

# ====================================================
# 통계
# ====================================================

elif page == "통계":

    st.title("📊 통계")

    df = pd.read_csv(TRADE_FILE)

    if len(df) > 0:

        avg_profit = df["수익률"].mean()

        st.metric(
            "평균 수익률",
            f"{avg_profit:.2f}%"
        )

        win_rate = (df["수익률"] > 0).mean() * 100

        st.metric(
            "승률",
            f"{win_rate:.1f}%"
        )

    else:
        st.warning("저장된 데이터가 없습니다.")