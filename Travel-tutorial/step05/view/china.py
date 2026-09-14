from pathlib import Path
import streamlit as st

st.set_page_config(page_title="중국 정보", page_icon="🇨🇳", layout="wide")

img_path = Path("src/assets/images/china.jpg")

st.title("🇨🇳 중화인민공화국 (China)")

col1, col2 = st.columns([1, 2])

with col1:
    if img_path.exists():
        st.image(str(img_path), caption="중국", use_container_width=True)
    else:
        st.info("💡 `src/assets/images/china.png`에 이미지를 추가하세요.")

with col2:
    st.subheader("국가 기본 정보")
    st.markdown("""
    * **수도:** 베이징 (Beijing)
    * **언어:** 중국어 (표준중국어)
    * **화폐:** 위안 (CNY, ¥)
    """) 
    st.link_button("중국 정부 공식 포털 (Gov.cn)", "http://english.www.gov.cn", use_container_width=True)