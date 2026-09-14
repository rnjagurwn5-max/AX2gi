from pathlib import Path
import streamlit as st

st.set_page_config(page_title="미국 정보", page_icon="🇺🇸", layout="wide")

# view/usa.py 내부

img_path = Path("src/assets/images/usa.jpg")

st.title("🇺🇸 미합중국 (United States of America)")

col1, col2 = st.columns([1, 2])

with col1:
    if img_path.exists():
        st.image(str(img_path), caption="미국", use_container_width=True)
    else:
        st.info("💡 `src/assets/images/usa.png`에 이미지를 추가하세요.")

with col2:
    st.subheader("국가 기본 정보")
    st.markdown("""
    * **수도:** 워싱턴 D.C. (Washington, D.C.)
    * **언어:** 영어 (사실상 공용어)
    * **화폐:** 달러 (USD, $)
    """)
    st.link_button("미국 공식 정부 서비스 (USA.gov)", "https://www.usa.gov", use_container_width=True)