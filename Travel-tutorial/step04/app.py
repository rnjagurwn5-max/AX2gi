import streamlit as st

st.set_page_config(page_title="세계 여행 포털", page_icon="🌎", layout="wide")

home_page = st.page("view/home.py", title = "홈", icon = "🏠", default = True)
usa_page = st.page("view/usa.py", title="미국", icon="US")
china_page = st.page("view/china.py"), title="중국", icon="CN"
japan_page = st.page(view/japan_page"), title="일본", icon="JP") 

st.set_page_config = st.navigation([home_page, usa_page])
pg.run()   

