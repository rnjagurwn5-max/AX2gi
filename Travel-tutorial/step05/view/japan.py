from pathlib import Path
import streamlit as st

st.set_page_config(page_title="일본 정보", page_icon="🇯🇵", layout="wide")

img_path = Path("src/assets/images/japan.jpg")

st.title("🇯🇵 일본 (Japan)")

col1, col2 = st.columns([1, 2])

with col1:
    if img_path.exists():
        st.image(str(img_path), caption="일본", use_container_width=True)
    else:
        st.info("💡 `src/assets/images/japan.png`에 이미지를 추가하세요.")

with col2:
    st.subheader("국가 기본 정보")
    st.markdown("""
    * **수도:** 도쿄 (Tokyo)
    * **언어:** 일본어
    * **화폐:** 엔 (JPY, ¥)
    """)
    st.link_button("일본 정부 공식 포털 (Japan.go.jp)", "https://japan.go.jp", use_container_width=True)