import streamlit as st
import pandas as pd
import os
from datetime import datetime
import calendar

# ======================================================
# 기본 설정
# ======================================================

st.set_page_config(
    page_title="주식 매매일지",
    layout="wide"
)

# ======================================================
# 파일명
# ======================================================

TRADE_FILE = "trades.csv"
WATCHLIST_FILE = "watchlist.csv"

# ======================================================
# CSV 생성
# ======================================================

if not os.path.exists(TRADE_FILE):

    trade_df = pd.DataFrame(columns=[
        "저장시간",
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

# ======================================================
# 사이드바
# ======================================================

st.sidebar.title("📌 메뉴")

page = st.sidebar.radio(
    "페이지 선택",
    [
        "매매일지 작성",
        "매매 기록",
        "관심종목 추가",
        "관심종목 보기",
        "통계",
        "매매 캘린더"
    ]
)

# ======================================================
# 매매일지 작성
# ======================================================

if page == "매매일지 작성":

    st.title("📈 주식 매매일지 작성")

    current_time = datetime.now()

    st.info(
        f"현재 저장 시간: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    date = st.date_input(
        "날짜",
        datetime.today(),
        key="date"
    )

    stock = st.text_input(
        "종목명",
        key="stock"
    )

    trade_type = st.selectbox(
        "매매유형",
        ["스윙", "단타", "중장기"],
        key="trade_type"
    )

    buy_reason = st.text_area(
        "매수 이유",
        key="buy_reason"
    )

    sell_reason = st.text_area(
        "매도 이유",
        key="sell_reason"
    )

    profit = st.number_input(
        "수익률 (%)",
        step=0.1,
        key="profit"
    )

    mistake = st.text_area(
        "실수",
        key="mistake"
    )

    lesson = st.text_area(
        "배운점",
        key="lesson"
    )

    # ==================================================
    # 저장 버튼
    # ==================================================

    if st.button("💾 저장하기"):

        new_data = pd.DataFrame([{
            "저장시간": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "날짜": date,
            "종목명": stock,
            "매매유형": trade_type,
            "매수이유": buy_reason,
            "매도이유": sell_reason,
            "수익률": profit,
            "실수": mistake,
            "배운점": lesson
        }])

        try:
            old_df = pd.read_csv(TRADE_FILE)

        except:
            old_df = pd.DataFrame(columns=[
                "저장시간",
                "날짜",
                "종목명",
                "매매유형",
                "매수이유",
                "매도이유",
                "수익률",
                "실수",
                "배운점"
            ])

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

        # 입력창 초기화

        st.rerun()

# ======================================================
# 매매 기록
# ======================================================

elif page == "매매 기록":

    st.title("📋 매매 기록")

    try:
        df = pd.read_csv(TRADE_FILE)

        if len(df) > 0:

            # ==========================================
            # 종목 검색
            # ==========================================

            search_stock = st.text_input(
                "🔍 종목 검색"
            )

            if search_stock:

                df = df[
                    df["종목명"].astype(str).str.contains(
                        search_stock,
                        case=False,
                        na=False
                    )
                ]

            st.dataframe(
                df,
                use_container_width=True
            )

            # ==========================================
            # 수정 기능
            # ==========================================

            st.subheader("✏ 기록 수정")

            row_index = st.number_input(
                "수정할 행 번호",
                min_value=0,
                max_value=len(df)-1,
                step=1
            )

            if st.button("수정 데이터 불러오기"):

                row = df.iloc[row_index]

                st.session_state.edit_stock = row["종목명"]
                st.session_state.edit_profit = row["수익률"]

            edit_stock = st.text_input(
                "종목명 수정",
                key="edit_stock"
            )

            edit_profit = st.number_input(
                "수익률 수정",
                key="edit_profit"
            )

            if st.button("수정 저장"):

                df.loc[row_index, "종목명"] = edit_stock
                df.loc[row_index, "수익률"] = edit_profit

                df.to_csv(
                    TRADE_FILE,
                    index=False,
                    encoding="utf-8-sig"
                )

                st.success("수정 완료!")
                st.rerun()

            # ==========================================
            # 삭제 기능
            # ==========================================

            st.subheader("🗑 기록 삭제")

            delete_index = st.number_input(
                "삭제할 행 번호",
                min_value=0,
                max_value=len(df)-1,
                step=1,
                key="delete_index"
            )

            if st.button("삭제하기"):

                df = df.drop(delete_index)

                df.to_csv(
                    TRADE_FILE,
                    index=False,
                    encoding="utf-8-sig"
                )

                st.success("삭제 완료!")
                st.rerun()

        else:
            st.warning("저장된 매매기록이 없습니다.")

    except:
        st.warning("저장된 매매기록이 없습니다.")

# ======================================================
# 관심종목 추가
# ======================================================

elif page == "관심종목 추가":

    st.title("⭐ 관심종목 추가")

    watch_stock = st.text_input(
        "종목명",
        key="watch_stock"
    )

    reason = st.text_area(
        "관심 이유",
        key="reason"
    )

    status = st.selectbox(
        "현재 상태",
        [
            "관찰중",
            "매수대기",
            "보유중",
            "매도완료"
        ],
        key="status"
    )

    memo = st.text_area(
        "메모",
        key="memo"
    )

    if st.button("➕ 관심종목 저장"):

        new_watch = pd.DataFrame([{
            "종목명": watch_stock,
            "관심이유": reason,
            "현재상태": status,
            "메모": memo
        }])

        try:
            old_watch = pd.read_csv(WATCHLIST_FILE)

        except:
            old_watch = pd.DataFrame(columns=[
                "종목명",
                "관심이유",
                "현재상태",
                "메모"
            ])

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

        st.session_state.watch_stock = ""
        st.session_state.reason = ""
        st.session_state.memo = ""

        st.rerun()

# ======================================================
# 관심종목 보기
# ======================================================

elif page == "관심종목 보기":

    st.title("📌 관심종목 리스트")

    try:

        watch_df = pd.read_csv(WATCHLIST_FILE)

        if len(watch_df) > 0:

            st.dataframe(
                watch_df,
                use_container_width=True
            )

        else:
            st.warning("관심종목이 없습니다.")

    except:
        st.warning("관심종목이 없습니다.")

# ======================================================
# 통계
# ======================================================

elif page == "통계":

    st.title("📊 매매 통계")

    try:

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

            st.subheader("📈 최근 매매")

            st.dataframe(
                df.tail(5),
                use_container_width=True
            )

        else:
            st.warning("저장된 데이터가 없습니다.")

    except:
        st.warning("저장된 데이터가 없습니다.")

# ======================================================
# 매매 캘린더
# ======================================================

elif page == "매매 캘린더":

    st.title("📅 매매 캘린더")

    now = datetime.now()

    year = st.selectbox(
        "연도",
        range(2024, 2031),
        index=2
    )

    month = st.selectbox(
        "월",
        range(1, 13),
        index=now.month - 1
    )

    cal = calendar.month(year, month)

    st.text(cal)

    try:

        df = pd.read_csv(TRADE_FILE)

        if len(df) > 0:

            st.subheader("📌 해당 월 매매기록")

            df["날짜"] = pd.to_datetime(df["날짜"])

            filtered = df[
                (df["날짜"].dt.year == year) &
                (df["날짜"].dt.month == month)
            ]

            st.dataframe(
                filtered,
                use_container_width=True
            )

    except:
        st.warning("매매 데이터가 없습니다.")