from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="국가 정보 서비스 - 대한민국",
    page_icon="🇰🇷",
    layout="wide"
)

# 이미지 경로 설정
IMAGE_DIR = Path("src/assets/images")
korea_img = IMAGE_DIR / "korea.jpg"

st.title("🇰🇷 대한민국 (Republic of Korea)")
st.caption("공식 국가 정보 및 주요 포털 가이드")

col1, col2 = st.columns([1, 2])

with col1:
    if korea_img.exists():
        st.image(str(korea_img), caption="대한민국", use_container_width=True)
    else:
        st.info("💡 `src/assets/images/korea.png`에 이미지를 추가하세요.")

with col2:
    st.subheader("국가 기본 정보")
    st.markdown("""
    * **수도:** 서울특별시
    * **언어:** 한국어
    * **화폐:** 원 (KRW, ₩)
    * **설명:** 동아시아의 한반도 남부에 위치한 민주공화국입니다.
    """)
    st.link_button("대한민국 정부 공식 포털 이동", "https://www.korea.go.kr", use_container_width=True)

st.divider()
st.info("👉 좌측 사이드바 메뉴를 통해 **중국, 일본, 미국**의 상세 페이지로 이동할 수 있습니다.")