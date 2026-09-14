import streamlit as st

# 1. 전체 브라우저 탭 기본 설정
st.set_page_config(
    page_title="세계 여행 포털",
    page_icon="🌍",
    layout="wide"
)

# 2. 각 국가별 화면(view 폴더 안의 파일들) 등록
# (주의: st.Page의 'P'는 대문자여야 합니다)
home_page  = st.Page("view/home.py",  title="대한민국 (홈)", icon="🇰🇷", default=True)
china_page = st.Page("view/china.py", title="중국",         icon="🇨🇳")
japan_page = st.Page("view/japan.py", title="일본",         icon="🇯🇵")
usa_page   = st.Page("view/usa.py",   title="미국",         icon="🇺🇸")

# 3. 사이드바 메뉴 네비게이션 생성
pg = st.navigation([home_page, china_page, japan_page, usa_page])

# 4. 사용자가 선택한 페이지 렌더링
pg.run()