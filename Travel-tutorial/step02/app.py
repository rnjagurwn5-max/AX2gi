import streamlit as st

st.set_page_config(page_title="세계 여행 포털", page_icon="🌏", layout="centered")

# 사이드바 메뉴 구성
menu = st.sidebar.selectbox("메뉴", ["홈", "미국", "중국", "일본"])

# 1. 홈 (대한민국)
if menu == "홈":
    st.title("🇰🇷 대한민국 (Republic of Korea)")
    st.subheader("전통과 현대가 공존하는 동아시아의 중심")
    st.write(
        """
        - **수도:** 서울
        - **주요 명소:** 경복궁, 남산서울타워, 부산 해운대, 제주도
        - **특징:** 유구한 역사문화 유산과 세계적인 K-컬처, 첨단 IT 인프라가 어우러진 여행지입니다.
        """
    )
    st.link_button("대한민국 관광 공식 사이트 방문", "https://korean.visitkorea.or.kr")

# 2. 미국
elif menu == "미국":
    st.title("🇺🇸 미국 (United States of America)")
    st.subheader("광활한 대자연과 세계 문화의 중심")
    st.write(
        """
        - **수도:** 워싱턴 D.C.
        - **주요 명소:** 그랜드 캐니언, 뉴욕 타임스스퀘어, 옐로스톤 국립공원, 하와이
        - **특징:** 50개 주마다 각기 다른 기후와 자연경관, 다채로운 다문화적 매력을 지닌 대륙형 여행지입니다.
        """
    )
    st.link_button("미국 관광 공식 사이트 방문", "https://www.visittheusa.com")

# 3. 중국
elif menu == "중국":
    st.title("🇨🇳 중국 (People's Republic of China)")
    st.subheader("수천 년의 역사와 장엄한 대륙의 풍경")
    st.write(
        """
        - **수도:** 베이징
        - **주요 명소:** 만리장성, 자금성, 상하이 와이탄, 시안 병마용, 장자제(장가계)
        - **특징:** 거대한 영토에 걸친 풍부한 문화유산과 빼어난 자연비경, 다채로운 미식 문화를 자랑합니다.
        """
    )
    st.link_button("중국 문화여유부 공식 사이트 방문", "https://www.mct.gov.cn")

# 4. 일본
elif menu == "일본":
    st.title("🇯🇵 일본 (Japan)")
    st.subheader("아기자기한 감성과 전통 료칸, 미식의 나라")
    st.write(
        """
        - **수도:** 도쿄
        - **주요 명소:** 후지산, 교토 기요미즈데라, 오사카 도톤보리, 홋카이도
        - **특징:** 고즈넉한 신사와 온천, 정갈한 미식 문화 및 편리한 교통 인프라를 갖춘 대표적인 근거리 여행지입니다.
        """
    )
    st.link_button("일본 관광청 공식 사이트 방문", "https://www.japan.travel/ko/kr/")