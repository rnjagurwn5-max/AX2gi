import streamlit as st

st.set_page_config(page_title="세계 여행 포털", page_icon="🌏", layout="centered")

# 1. 페이지 정의 (경로 따옴표 추가, title/icon 키워드 인자 적용)
home = st.Page("view/home.py", title="홈", icon="🏠", default=True)
usa = st.Page("view/usa.py", title="미국", icon="🇺🇸")
china = st.Page("view/china.py", title="중국", icon="🇨🇳")
japan = st.Page("view/japan.py", title="일본", icon="🇯🇵")

# 2. 네비게이션 메뉴 생성 (pg 변수에 할당)
pg = st.navigation([home, usa, china, japan])

# 3. 네비게이션 실행 (괄호 () 필수)
pg.run()
