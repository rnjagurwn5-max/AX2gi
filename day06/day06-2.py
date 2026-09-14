import html
import os
import re
import folium
import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_folium import st_folium

# 1. 환경변수 로드
load_dotenv()
KAKAO_REST_KEY = os.getenv("KAKAO_REST_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

st.set_page_config(
    page_title="오모먹 🚗✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 커스텀 CSS
st.markdown(
    """
<style>
    .place-box {
        background-color: rgba(128, 128, 128, 0.08);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .place-thumb {
        width: 100%;
        height: 85px;
        object-fit: cover;
        border-radius: 6px;
    }
    .no-thumb {
        width: 100%;
        height: 85px;
        background-color: #eee;
        color: #888;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        border-radius: 6px;
    }
    .place-review {
        background: rgba(255, 75, 75, 0.08);
        border-left: 3px solid #ff4b4b;
        padding: 4px 6px;
        font-size: 11px;
        border-radius: 0 4px 4px 0;
        margin-top: 5px;
        line-height: 1.3;
    }
    .weather-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .landing-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 65vh;
        text-align: center;
    }
    .landing-title {
        font-size: 5rem;
        font-weight: 900;
        margin-bottom: 10px;
        color: #2b56f5;
    }
    .landing-subtitle {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 50px;
        color: #555;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# 실제 연예인 찐 맛집 하드코딩 DB
# -------------------------------------------------------------
CELEB_RESTAURANTS = {
    "성시경 먹을텐데": [
        "여의도 화목순대국", "남영동 남영돈", "논현동 우정양곱창", 
        "구의동 서북면옥", "약수역 약수순대국", "신당동 하니칼국수"
    ],
    "이영자 맛집": [
        "한남동 한방통닭", "역삼동 돝고기506", "도화동 코끼리분식", 
        "명동교자 본점", "청담동 진대감"
    ],
    "카리나 맛집": [
        "성수 소문난성수감자탕", "압구정 보보식당", "부산 톤쇼우 광안리점", 
        "청담 다운타우너", "건대 호야초밥"
    ]
}

# -------------------------------------------------------------
# 세션 상태 초기화
# -------------------------------------------------------------
if "app_started" not in st.session_state:
    st.session_state.app_started = False
if "search_mode" not in st.session_state:
    st.session_state.search_mode = "keyword" # "keyword" 또는 "celeb"
if "search_query" not in st.session_state:
    st.session_state.search_query = "강남역 맛집"
if "region_input" not in st.session_state:
    st.session_state.region_input = "강남역"

# ==========================================
# 랜딩 페이지 (시작 화면)
# ==========================================
if not st.session_state.app_started:
    st.markdown(
        """
        <div class="landing-container">
            <div class="landing-title">🍽️ 오모먹</div>
            <div class="landing-subtitle">(🚗 오늘 ✈️ 뭐 먹지?)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("냠냠 😋", use_container_width=True, type="primary"):
            st.session_state.app_started = True
            st.rerun()
            
    st.stop()


# ==========================================
# 메인 앱 로직 (API 및 함수 정의)
# ==========================================
if not KAKAO_REST_KEY:
    st.error("`.env` 파일에 KAKAO_REST_API_KEY가 설정되어 있지 않습니다.")
    st.stop()

@st.cache_data(ttl=600)
def get_current_weather(api_key: str, lat: float = 37.5665, lon: float = 126.9780):
    if not api_key:
        return 20.0, "기본 안내"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": "kr"}
    try:
        res = requests.get(url, params=params, timeout=5)
        if res.status_code == 200:
            data = res.json()
            temp = data.get("main", {}).get("temp", 20.0)
            desc = data.get("weather", [{}])[0].get("description", "맑음")
            return temp, desc
    except Exception:
        pass
    return 20.0, "날씨 정보 로딩 실패"

def recommend_menu_by_weather(temp: float, weather_desc: str):
    if "비" in weather_desc or "소나기" in weather_desc:
        return "🌧️ 비 오는 날", "바삭한 해물파전, 칼국수", "파전"
    elif temp >= 27.0:
        return "❄️ 폭염주의!", "살얼음 동동 냉면, 콩국수, 시원한 물회", "냉면"
    elif temp >= 22.0:
        return "☀️ 맑고 더운 날씨", "시원한 막국수, 가벼운 브런치", "막국수"
    elif temp >= 12.0:
        return "🍂 선선한 나들이 날씨", "바삭한 돈까스, 파스타, 솥밥", "돈까스"
    elif temp >= 5.0:
        return "🧥 쌀쌀한 바람", "뜨끈한 칼국수, 샤브샤브, 전골 요리", "칼국수"
    else:
        return "🧊 추운 겨울 날씨", "보글보글 순대국, 뚝배기 해장국", "순대국"

@st.cache_data(ttl=3600)
def get_exchange_rate(api_key: str, base: str = "USD"):
    if not api_key:
        return None
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json().get("conversion_rates", {})
    except Exception:
        pass
    return None

def search_places(query: str, rest_key: str):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {rest_key}"}
    params = {"query": query, "size": 8}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        res.raise_for_status()
        return res.json().get("documents", [])
    except Exception as e:
        st.sidebar.error(f"장소 검색 실패: {e}")
        return []

@st.cache_data(show_spinner=False)
def get_place_image(place_name: str, location_hint: str, rest_key: str):
    url = "https://dapi.kakao.com/v2/search/image"
    headers = {"Authorization": f"KakaoAK {rest_key}"}
    query = f"{location_hint} {place_name}"
    params = {"query": query, "size": 1, "sort": "accuracy"}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=4)
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            if docs:
                return docs[0].get("thumbnail_url")
    except Exception:
        pass
    return None

@st.cache_data(show_spinner=False)
def get_place_review(place_name: str, location_hint: str, rest_key: str):
    url = "https://dapi.kakao.com/v2/search/blog"
    headers = {"Authorization": f"KakaoAK {rest_key}"}
    query = f"{location_hint} {place_name} 후기"
    params = {"query": query, "size": 1, "sort": "accuracy"}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=4)
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            if docs:
                clean_text = re.sub(r"<[^>]+>", "", docs[0].get("contents", ""))
                clean_text = html.unescape(clean_text).strip()
                if clean_text:
                    return clean_text[:65] + "..." if len(clean_text) > 65 else clean_text
    except Exception:
        pass
    return "방문자 후기 정보가 아직 없습니다."


# -------------------------------------------------------------
# 사전 데이터 연산
# -------------------------------------------------------------
current_temp, weather_desc = get_current_weather(WEATHER_API_KEY)
weather_title, food_desc, quick_keyword = recommend_menu_by_weather(current_temp, weather_desc)


# -------------------------------------------------------------
# [사이드바] UI 구성
# -------------------------------------------------------------
with st.sidebar:
    st.header("✈️ 어디로 떠날까요?")

    # 1. 날씨 배너
    st.markdown(
        f"""
        <div class="weather-banner">
            <div style="font-size: 11px; opacity: 0.85;">현재 날씨 ({current_temp:.1f}°C / {weather_desc})</div>
            <div style="font-weight: bold; font-size: 14px; margin-top: 2px;">{weather_title}</div>
            <div style="font-size: 12px; margin-top: 4px; color: #ffeb3b;">추천: {food_desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(f"💡 오늘 날씨 맞춤 '{quick_keyword}' 검색", use_container_width=True):
        st.session_state.search_mode = "keyword"
        st.session_state.search_query = f"{st.session_state.region_input} {quick_keyword}"

    st.divider()

    # 2. 지역 및 테마 맞춤 검색 영역 (연예인 리스트 분기 처리)
    st.subheader("🔍 테마 맞춤 검색")
    region = st.text_input("📍 지역/국가명", value=st.session_state.region_input, placeholder="예: 강남역, 제주도, 오사카")
    
    # 드롭다운 메뉴 업데이트
    theme_options = ["기본 맛집 검색", "성시경 먹을텐데", "이영자 맛집", "카리나 맛집", "날씨별 추천", "지역별 명소"]
    theme = st.selectbox("💡 추천 테마", theme_options)
    
    search_btn = st.button("테마 맛집 찾기 🚗", use_container_width=True, type="primary")

    if search_btn:
        if theme in CELEB_RESTAURANTS:
            # 연예인 맛집 선택 시 -> 지역 무시하고 실제 전국 리스트 로드 모드로 변경
            st.session_state.search_mode = "celeb"
            st.session_state.search_query = theme
            st.success(f"'{theme}'은(는) 지역과 무관하게 실제 검증된 전국 리스트를 불러옵니다!")
        else:
            if region.strip():
                st.session_state.region_input = region
                st.session_state.search_mode = "keyword"
                if theme == "기본 맛집 검색":
                    st.session_state.search_query = f"{region} 맛집"
                elif theme == "날씨별 추천":
                    st.session_state.search_query = f"{region} {quick_keyword}"
                elif theme == "지역별 명소":
                    st.session_state.search_query = f"{region} 가볼만한곳 명소"
            else:
                st.warning("지역을 먼저 입력해주세요!")

    st.divider()

    # 3. 자유 검색창
    st.subheader("🔎 자유 검색")
    free_query = st.text_input("자유롭게 맛집이나 키워드를 입력하세요", placeholder="예: 성수동 분위기 좋은 카페")
    if st.button("자유 검색 실행 🚀", use_container_width=True):
        if free_query.strip():
            st.session_state.search_mode = "keyword"
            st.session_state.search_query = free_query
        else:
            st.warning("검색어를 입력해주세요!")

    st.divider()

    # 4. 환율 계산기
    with st.expander("💱 실시간 환율 계산기", expanded=False):
        if not EXCHANGE_API_KEY:
            st.warning("`.env`에 EXCHANGE_API_KEY를 입력해주세요.")
        else:
            base_cur = st.selectbox("기준 통화", ["USD", "EUR", "JPY", "KRW"])
            amount = st.number_input("금액 입력", min_value=0.0, value=100.0, step=10.0)
            target_cur = st.selectbox("변환 통화", ["KRW", "USD", "EUR", "JPY"])
            
            rates = get_exchange_rate(EXCHANGE_API_KEY, base_cur)
            if rates and target_cur in rates:
                converted = amount * rates[target_cur]
                st.success(f"**{amount:,.2f} {base_cur}**\n\n= **{converted:,.2f} {target_cur}**")
            else:
                st.error("환율 정보를 불러올 수 없습니다.")


    # 5. 장소 데이터 수집 로직 (모드에 따라 다르게 작동)
    places = []
    
    if st.session_state.search_mode == "celeb":
        # 연예인 맛집: 하드코딩된 특정 가게 이름을 각각 API로 검색하여 취합
        celeb_name = st.session_state.search_query
        with st.spinner(f"실제 {celeb_name} 찐 맛집 리스트를 불러오는 중..."):
            for exact_rest_name in CELEB_RESTAURANTS.get(celeb_name, []):
                res = search_places(exact_rest_name, KAKAO_REST_KEY)
                if res:
                    places.append(res[0]) # 정확도 1위인 첫 번째 장소만 취합
    else:
        # 일반 키워드 검색
        if st.session_state.search_query:
            with st.spinner("맛집 데이터 및 후기를 로딩 중..."):
                places = search_places(st.session_state.search_query, KAKAO_REST_KEY)

    st.divider()

    # 사이드바 리스트 렌더링
    st.subheader(f"📋 맛집 목록 ({len(places)}곳)")
    if not places:
        st.info("검색 결과가 없습니다.")
    else:
        for idx, p in enumerate(places, 1):
            name = p["place_name"]
            addr = p.get("road_address_name") or p.get("address_name", "")
            region_hint = addr.split()[0] if addr else ""

            img_url = get_place_image(name, region_hint, KAKAO_REST_KEY)
            review = get_place_review(name, region_hint, KAKAO_REST_KEY)

            st.markdown('<div class="place-box">', unsafe_allow_html=True)
            col_img, col_info = st.columns([1, 2])

            with col_img:
                if img_url:
                    st.markdown(f'<img src="{img_url}" class="place-thumb" alt="{name}">', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="no-thumb">이미지 없음</div>', unsafe_allow_html=True)

            with col_info:
                st.markdown(f"**{idx}. [{name}]({p.get('place_url')})**")
                st.caption(f"📍 {addr}")

            st.markdown(f'<div class="place-review">💬 <b>후기:</b> {review}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------------
# [메인 화면] 지도 렌더링
# -------------------------------------------------------------
st.title("🍽️ 오모먹 (🚗 오늘 ✈️ 뭐 먹지?)")
st.caption(f"현재 검색어: **{st.session_state.search_query}** | 음식점을 클릭하면 후기는 덤!")

default_lat, default_lng = 37.566826, 126.9786567

if places:
    # 맵 마커들의 위경도를 수집하여 맵의 중앙값 계산
    lats = [float(p["y"]) for p in places]
    lngs = [float(p["x"]) for p in places]
    center_lat = sum(lats) / len(lats)
    center_lng = sum(lngs) / len(lngs)
    
    m = folium.Map(location=[center_lat, center_lng], zoom_start=12)

    for idx, p in enumerate(places, 1):
        lat = float(p["y"])
        lng = float(p["x"])
        name = p["place_name"]
        addr = p.get("road_address_name") or p.get("address_name", "")
        region_hint = addr.split()[0] if addr else ""
        
        # 카테고리 정보 확인 (카페 vs 일반 음식점 분기 처리)
        cat_group = p.get("category_group_name", "")
        cat_name = p.get("category_name", "")
        
        if "카페" in cat_group or "카페" in cat_name:
            marker_color = "orange"
            marker_icon = "coffee"
        else:
            marker_color = "red"
            marker_icon = "cutlery"

        img_url = get_place_image(name, region_hint, KAKAO_REST_KEY)
        review = get_place_review(name, region_hint, KAKAO_REST_KEY)

        img_html = (
            f'<img src="{img_url}" style="width:100%; height:95px;'
            ' object-fit:cover; border-radius:4px; margin-bottom:6px;">'
            if img_url else ""
        )
        popup_html = f"""
            <div style="width: 210px; font-family: sans-serif;">
                {img_html}
                <div style="font-size: 13px; font-weight: bold; margin-bottom: 4px;">
                    <a href="{p.get('place_url')}" target="_blank" style="text-decoration:none; color:#1a73e8;">{idx}. {name}</a>
                </div>
                <div style="font-size: 11px; color: #555; margin-bottom: 6px;">📍 {addr}</div>
                <div style="font-size: 11px; color: #333; background: #f3f3f3; padding: 5px; border-radius: 4px; line-height: 1.35;">
                    💬 <b>후기:</b> {review}
                </div>
            </div>
            """

        folium.Marker(
            location=[lat, lng],
            popup=folium.Popup(popup_html, max_width=240),
            tooltip=f"{idx}. {name}",
            icon=folium.Icon(color=marker_color, icon=marker_icon, prefix="fa"),
        ).add_to(m)
        
    # 전국구 맛집인 경우 마커가 모두 화면에 들어오도록 자동 바운드 조절
    if len(places) > 1:
        sw = [min(lats), min(lngs)]
        ne = [max(lats), max(lngs)]
        m.fit_bounds([sw, ne])

else:
    m = folium.Map(location=[default_lat, default_lng], zoom_start=12)

st_folium(m, use_container_width=True, height=720)