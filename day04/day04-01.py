# raw_trade_data.csv 파일 활용
# Hs코드가 
# 85로 시작하는 (반도체) + 국가명 미국 또는 베트남 + 수출금액 0 보다 큰 수(실제 수출실적이 있는) 행만
# 다중 조건 으로 필터링 한뒤, 수출금액 상위 10건 화면에 보여주고 report.csv로 저장
# streamlit 사용 streamlit run day04-01.py

import os
import pandas as pd
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(page_title="수출 데이터 분석", layout="wide")
st.title("반도체(HS 85) 대 미국·베트남 수출 실적 상위 10건")

file_path = "raw_trade_data.csv"

if not os.path.exists(file_path):
    st.error(f"파일을 찾을 수 없습니다: `{file_path}` 경로를 확인해주세요.")
else:
    # 2. 데이터 불러오기 (한글 인코딩 대응)
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="cp949")

    # 3. 데이터 전처리 및 다중 조건 필터링
    # - HS코드는 문자열 변환 후 공백 제거
    # - 수출금액은 수치형 변환
    df["HS코드"] = df["HS코드"].astype(str).str.strip()
    df["수출금액"] = pd.to_numeric(df["수출금액"], errors="coerce").fillna(0)
    df["국가명"] = df["국가명"].astype(str).str.strip()

    # 다중 조건 설정 (& 연산자 활용)
    cond_hs = df["HS코드"].str.startswith("85")
    cond_country = df["국가명"].isin(["미국", "베트남"])
    cond_amount = df["수출금액"] > 0

    filtered_df = df[cond_hs & cond_country & cond_amount]

    # 4. 수출금액 기준 내림차순 정렬 후 상위 10건 추출
    top10_df = (
        filtered_df.sort_values(by="수출금액", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    # 5. report.csv 자동 저장 (한글 깨짐 방지: utf-8-sig)
    top10_df.to_csv("report.csv", index=False, encoding="utf-8-sig")

    # 6. 화면 출력
    st.subheader("상위 10건 데이터 미리보기")
    st.dataframe(top10_df, width="stretch")

    # 7. 데이터 시각화 (막대 그래프)
    st.markdown("---")
    st.subheader("📊 품목별 수출금액 차트 (상위 10건)")
    st.bar_chart(
        data=top10_df,
        x="품목명",
        y="수출금액",
        color="국가명"
    )

    st.success("`report.csv` 파일 저장이 완료되었습니다.")

    # Streamlit 다운로드 버튼 제공 
    csv_data = top10_df.to_csv(index=False, encoding="utf-8-sig").encode(
        "utf-8-sig"
    )
    st.download_button(
        label="결과 CSV 다운로드",
        data=csv_data,
        file_name="report.csv",
        mime="text/csv",
    ) 
    