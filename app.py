from datetime import datetime
import pandas as pd
import streamlit as st
import os

# ======================================================
# 기본 설정
# ======================================================

st.set_page_config(
    page_title="주식 매매일지",
    layout="wide"
)

TRADE_FILE = "trade_log.csv"

# ======================================================
# CSV 파일 생성
# ======================================================

if not os.path.exists(TRADE_FILE):

    empty_df = pd.DataFrame(columns=[
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

    empty_df.to_csv(
        TRADE_FILE,
        index=False,
        encoding="utf-8-sig"
    )

# ======================================================
# 제목
# ======================================================

st.title("📈 주식 매매일지")

# ======================================================
# 현재 시간 표시
# ======================================================

current_time = datetime.now()

st.caption(
    f"현재 시간 : {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
)

# ======================================================
# 저장 성공 메시지 상태
# ======================================================

if "save_message" not in st.session_state:
    st.session_state.save_message = False

# ======================================================
# 입력 Form
# ======================================================

with st.form("trade_form", clear_on_submit=True):

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

    submitted = st.form_submit_button("💾 저장하기")

    # ==================================================
    # 저장 처리
    # ==================================================

    if submitted:

        # 종목명 공백 방지

        if not stock.strip():

            st.error("종목명을 입력하세요.")

        else:

            new_data = pd.DataFrame(
                [
                    {
                        "저장시간": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "날짜": date.strftime("%Y-%m-%d"),
                        "종목명": stock,
                        "매매유형": trade_type,
                        "매수이유": buy_reason,
                        "매도이유": sell_reason,
                        "수익률": profit,
                        "실수": mistake,
                        "배운점": lesson,
                    }
                ]
            )

            # ==========================================
            # 기존 파일 읽기
            # ==========================================

            try:

                old_df = pd.read_csv(TRADE_FILE)

            except Exception:

                old_df = pd.DataFrame(
                    columns=[
                        "저장시간",
                        "날짜",
                        "종목명",
                        "매매유형",
                        "매수이유",
                        "매도이유",
                        "수익률",
                        "실수",
                        "배운점",
                    ]
                )

            # ==========================================
            # 데이터 저장
            # ==========================================

            updated_df = pd.concat(
                [old_df, new_data],
                ignore_index=True
            )

            updated_df.to_csv(
                TRADE_FILE,
                index=False,
                encoding="utf-8-sig"
            )

            st.session_state.save_message = True

# ======================================================
# 저장 완료 메시지
# ======================================================

if st.session_state.save_message:

    st.success("저장 완료되었습니다.")

    st.session_state.save_message = False

# ======================================================
# 매매 기록 보기
# ======================================================

st.divider()

st.subheader("📋 매매 기록")

try:

    df = pd.read_csv(TRADE_FILE)

    # ==================================================
    # 종목 검색
    # ==================================================

    search_stock = st.text_input("🔍 종목 검색")

    if search_stock:

        df = df[
            df["종목명"].astype(str).str.contains(
                search_stock,
                case=False,
                na=False
            )
        ]

    # index 초기화

    df = df.reset_index(drop=True)

    # ==================================================
    # 데이터 표시
    # ==================================================

    if len(df) > 0:

        st.dataframe(
            df,
            use_container_width=True
        )

        # ==============================================
        # 수정 기능
        # ==============================================

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

            st.success("수정 완료되었습니다.")

        # ==============================================
        # 삭제 기능
        # ==============================================

        st.subheader("🗑 기록 삭제")

        delete_index = st.number_input(
            "삭제할 행 번호",
            min_value=0,
            max_value=len(df)-1,
            step=1,
            key="delete_index"
        )

        if st.button("삭제하기"):

            df = df.drop(delete_index).reset_index(drop=True)

            df.to_csv(
                TRADE_FILE,
                index=False,
                encoding="utf-8-sig"
            )

            st.success("삭제 완료되었습니다.")

    else:

        st.warning("저장된 매매기록이 없습니다.")

except Exception:

    st.warning("저장된 데이터가 없습니다.")