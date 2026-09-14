# 기존 Python 파일의 내용을 이 파일 전체로 교체하세요. 파일명/폴더/.env 위치는 그대로 둡니다.
# 기존 설치 패키지: streamlit, requests, python-dotenv, folium, streamlit-folium
import html
import math
import os
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import requests
import streamlit as st

try:
    import folium
    from streamlit_folium import st_folium
except ImportError:
    folium = None
try:
    from dotenv import load_dotenv
    load_dotenv()  # 원본과 동일: 기존 .env 탐색 방식과 경로를 유지합니다.
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

KAKAO_REST_KEY = os.getenv("KAKAO_REST_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") or os.getenv("WEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
SEOUL_PHOTO = "https://images.unsplash.com/photo-1662300835077-73c417630ff5?auto=format&fit=crop&w=2200&q=85"
PHOTO_SOURCE = "https://unsplash.com/photos/YqgOH-ewy6Q"

st.set_page_config(page_title="오모먹 | 오늘의 맛있는 발견", page_icon="🍽️", layout="wide", initial_sidebar_state="collapsed")

def esc(value):
    return html.escape(str(value or ""), quote=True)

def safe_url(value):
    value = str(value or "")
    parsed = urlparse(value)
    return value if parsed.scheme in ("https", "http") and parsed.netloc else ""

def markup(value):
    st.markdown(value, unsafe_allow_html=True)

markup("""<style>
:root {color-scheme:light; --ink:#17191d; --muted:#777e86; --green:#268349;}
.stApp {background:#fff; color:var(--ink);}
[data-testid="stHeader"] {background:rgba(255,255,255,.95);}
.block-container {max-width:1440px; padding:2.2rem 3rem 3rem;}
html {scroll-behavior:smooth;}
h1,h2,h3,p,button,input {font-family:Inter,"Pretendard","Noto Sans KR",Arial,sans-serif;}
.notice {background:#f5f7f9; border-radius:12px; padding:13px 20px; text-align:center; font-size:13px; color:#555e67;}
.notice b {color:#268349; margin-right:14px;}
.nav {display:flex; justify-content:space-between; align-items:center; gap:24px; padding:27px 0 29px;}
.logo {font-size:29px; font-weight:900; letter-spacing:-2px; color:#17191d!important; text-decoration:none!important;}
.logo small {font-size:10px; letter-spacing:2px; margin-left:12px; font-weight:600; color:#81878c;}
.nav-links {display:flex; align-items:center; gap:32px; font-size:14px;}
.nav a {color:#333; text-decoration:none;}
.nav a:hover {color:#268349;}
.nav .nav-cta {background:#17191d; color:white; border-radius:8px; padding:12px 19px;}
.hero {position:relative; isolation:isolate; min-height:410px; border-radius:20px; overflow:hidden; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; color:white; padding:50px 22px; background:#344d57;}
.hero:before {content:""; position:absolute; inset:0; z-index:-2; background-image:var(--seoul); background-position:center 54%; background-size:cover;}
.hero:after {content:""; position:absolute; inset:0; z-index:-1; background:linear-gradient(90deg,rgba(12,25,32,.48),rgba(12,25,32,.32));}
.hero .eyebrow {font-size:12px; font-weight:600; letter-spacing:4px; color:#e2f6df; margin-bottom:18px;}
.hero h1 {color:white; font-size:clamp(34px,4vw,58px); line-height:1.25; letter-spacing:-2.5px; font-weight:800; padding:0; margin:0 0 21px;}
.hero p {font-size:16px; line-height:1.8; color:#f3f5f5; margin:0;}
.hero .location {position:absolute; bottom:19px; left:25px; font-size:11px; letter-spacing:2px; color:#fff;}
.hero .photo-credit {position:absolute; bottom:18px; right:24px; color:#fff; font-size:10px; text-decoration:none;}
.intro {text-align:center; padding:40px 0 18px;}
.intro .green {color:#268349; font-size:14px; font-weight:700;}
.intro h2 {font-size:30px; letter-spacing:-1.3px; padding:7px 0; margin:0;}
.intro p {color:#82878d; font-size:14px;}
[data-testid="stForm"] {background:#f8f9fa; border:1px solid #eef0f2; border-radius:14px; padding:20px 22px;}
[data-testid="stTextInput"] input {background:white; color:#17191d;}
[data-baseweb="select"] > div {background:white; color:#17191d;}
[data-testid="stWidgetLabel"] p {color:#505760; font-size:13px;}
[data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button {border-radius:9px; min-height:42px; border:1px solid #e7e9ed; background:white; color:#363b41; box-shadow:none;}
[data-testid="stButton"] button:hover, [data-testid="stFormSubmitButton"] button:hover {border-color:#268349; color:#268349;}
button[kind="primary"], [data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"] {background:#17191d!important; border-color:#17191d!important; color:white!important;}
.section-head {display:flex; align-items:flex-end; justify-content:space-between; gap:12px; margin:34px 0 20px;}
.section-head h2 {font-size:23px; padding:0; margin:0; letter-spacing:-.7px;}
.section-head span {font-size:12px; color:#838991;}
.collection {border:1px solid #ebedf0; border-radius:13px; overflow:hidden; margin:0 0 12px;}
.collection-art {height:148px; display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;}
.collection-art:before {content:""; width:170px; height:170px; border:1px solid currentColor; opacity:.16; border-radius:50%; position:absolute; right:-20px; top:-50px;}
.collection-art strong {font-family:Georgia,serif; font-size:33px; font-weight:400; letter-spacing:-1px;}
.collection-body {padding:17px 18px; background:white;}
.collection-body h3 {font-size:16px; padding:0; margin:0 0 7px;}
.collection-body p {font-size:12px; color:#7b8189; margin:0;}
.weather {background:#f2f7f2; padding:21px 24px; border-radius:13px; margin:25px 0 12px; color:#284b35;}
.weather {background:#f2f7f2; padding:21px 24px; border-radius:13px; margin:25px 0 12px; color:#284b35; display:flex; align-items:center; justify-content:space-between; gap:32px;}
.weather-menu {flex:1; min-width:0;}
.weather-today {flex:1.2; display:flex; align-items:center; justify-content:center; gap:24px; border-left:1px solid #d7e4d9; padding:8px 20px 8px 32px; min-width:0;}
.weather-icon {font-size:52px; line-height:1;}
.weather-temperature {font-size:46px; font-weight:800; line-height:1.15; letter-spacing:-2px; margin:6px 0; color:#284b35;}
.weather-condition {font-size:15px; font-weight:600; color:#42634c; overflow-wrap:anywhere;}
.weather small {font-size:11px; color:#62796a; letter-spacing:.5px;}
.weather strong {display:block; margin:6px 0; font-size:19px;}
.weather p {margin:0; color:#62796a; font-size:13px;}
.place {border:1px solid #e8ebee; border-radius:13px; overflow:hidden; background:white; margin-bottom:14px; transition:transform .2s,box-shadow .2s;}
.place:hover {transform:translateY(-3px); box-shadow:0 10px 30px #182b3910;}
.place-photo {height:178px; background:#eef1ed; overflow:hidden; position:relative;}
.place-photo img {width:100%; height:100%; object-fit:cover;}
.no-photo {height:100%; display:flex; align-items:center; justify-content:center; color:#8b948e; font-size:13px;}
.place-number {position:absolute; left:12px; top:12px; background:#fff; border-radius:6px; padding:4px 9px; font-size:12px; color:#24292d;}
.place-body {padding:19px;}
.tag {font-size:10px; color:#268349; letter-spacing:.5px; margin-bottom:6px;}
.place h3 {font-size:18px; padding:0; margin:0 0 9px; color:#17191d;}
.address {font-size:12px; color:#838991; min-height:35px; margin-bottom:10px;}
.review {font-size:12px; line-height:1.7; color:#626970; background:#f8f9fa; padding:11px; border-radius:7px; min-height:76px;}
.place-link {display:block; color:#20262b!important; font-size:12px; text-decoration:none!important; padding-top:14px;}
.empty {text-align:center; border:1px dashed #dae0e4; border-radius:14px; background:#fafbfc; padding:45px 20px; color:#737c85;}
.empty b {display:block; color:#30373d; font-size:18px; margin-bottom:10px;}
.footer {border-top:1px solid #eceef1; margin-top:50px; padding-top:26px; display:flex; justify-content:space-between; gap:20px; font-size:12px; color:#8a9097;}
.footer b {font-size:20px; color:#17191d; letter-spacing:-1px;}
@media(max-width:760px) {
 .weather {flex-direction:column; align-items:stretch; gap:20px;}
 .weather-today {border-left:0; border-top:1px solid #d7e4d9; padding:20px 0 0; justify-content:flex-start;}
 .weather-temperature {font-size:38px;}.weather-icon {font-size:44px;}
 .block-container {padding:1.3rem 1rem 2rem;}
 .nav {padding:22px 0;}.nav-links {gap:14px; font-size:12px;}.nav-links .optional,.logo small {display:none;}
 .nav .nav-cta {padding:10px 12px;}.hero {min-height:370px; border-radius:14px;}
 .hero h1 {letter-spacing:-1.6px;}.hero p {font-size:13px;}.hero .eyebrow {font-size:10px; letter-spacing:2px;}
 .hero .photo-credit {font-size:8px;}.intro h2 {font-size:25px;}.section-head {align-items:start;flex-direction:column;}
 .footer {flex-direction:column;}.notice {font-size:11px;}.notice b {margin-right:5px;}
}
</style>""")

# 사용자가 제공한 기존 목록을 그대로 유지합니다. 출연/방문 여부를 새로 검증한 목록은 아닙니다.
CELEB_RESTAURANTS = {
    "성시경 먹을텐데": ["여의도 화목순대국", "남영동 남영돈", "논현동 우정양곱창", "구의동 서북면옥", "약수역 약수순대국", "신당동 하니칼국수"],
    "이영자 맛집": ["한남동 한방통닭", "역삼동 돝고기506", "도화동 코끼리분식", "명동교자 본점", "청담동 진대감"],
    "카리나 맛집": ["성수 소문난성수감자탕", "압구정 보보식당", "부산 톤쇼우 광안리점", "청담 다운타우너", "건대 호야초밥"],
}
for key, default in {"app_started": False, "search_mode": "keyword", "search_query": "강남역 맛집", "region_input": "강남역", "active_theme": "전체"}.items():
    st.session_state.setdefault(key, default)

def request_json(url, **kwargs):
    try:
        response = requests.get(url, timeout=6, **kwargs)
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, dict) else {}
    except (requests.RequestException, ValueError):
        return None

@st.cache_data(ttl=600, show_spinner=False)
def get_current_weather(api_key, lat=37.5665, lon=126.9780):
    if not api_key:
        return None, "날씨 정보를 연결하면 맞춤 메뉴를 추천해 드려요."
    data = request_json("https://api.openweathermap.org/data/2.5/weather", params={"lat":lat,"lon":lon,"appid":api_key,"units":"metric","lang":"kr"})
    if not data or not isinstance(data.get("main", {}).get("temp"), (int, float)):
        return None, "지금은 날씨 정보를 불러올 수 없어요."
    weather = data.get("weather") or [{}]
    return data["main"]["temp"], weather[0].get("description", "")

def recommend_menu_by_weather(temp, description):
    if temp is None: return "오늘의 메뉴 아이디어", "바삭한 돈까스, 든든한 솥밥은 어떠세요?", "돈까스"
    if "비" in description or "소나기" in description: return "비 오는 날의 한 끼", "바삭한 해물파전과 따뜻한 칼국수", "파전"
    if temp >= 27: return "시원한 한 그릇이 필요한 날", "냉면, 콩국수, 시원한 물회", "냉면"
    if temp >= 22: return "가볍고 시원하게 즐겨요", "막국수와 여유로운 브런치", "막국수"
    if temp >= 12: return "맛있는 나들이를 떠나볼까요", "돈까스, 파스타, 정갈한 솥밥", "돈까스"
    if temp >= 5: return "따뜻한 한 끼가 생각나는 날", "칼국수, 샤브샤브, 보글보글 전골", "칼국수"
    return "뜨끈하게 속을 채워요", "순대국과 뚝배기 해장국", "순대국"

@st.cache_data(ttl=3600, show_spinner=False)
def get_exchange_rate(api_key, base="USD"):
    if not api_key: return None
    data = request_json(f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}")
    return data.get("conversion_rates") if data else None

@st.cache_data(ttl=600, show_spinner=False)
def search_places(query, rest_key):
    data = request_json("https://dapi.kakao.com/v2/local/search/keyword.json", headers={"Authorization":f"KakaoAK {rest_key}"}, params={"query":query,"size":8})
    return (data.get("documents", []), None) if data is not None else ([], "장소 검색에 실패했어요. API 키와 연결 상태를 확인한 후 다시 검색해 주세요.")

@st.cache_data(ttl=3600, show_spinner=False)
def get_place_details(place_name, location_hint, rest_key):
    headers = {"Authorization":f"KakaoAK {rest_key}"}
    query = f"{location_hint} {place_name}"
    images = request_json("https://dapi.kakao.com/v2/search/image", headers=headers, params={"query":query,"size":1,"sort":"accuracy"})
    blogs = request_json("https://dapi.kakao.com/v2/search/blog", headers=headers, params={"query":f"{query} 후기","size":1,"sort":"accuracy"})
    image_docs = (images or {}).get("documents") or []
    blog_docs = (blogs or {}).get("documents") or []
    image_url = safe_url(image_docs[0].get("thumbnail_url")) if image_docs else ""
    review, review_url = "관련 블로그 글이 아직 없어요.", ""
    if blog_docs:
        raw = html.unescape(re.sub(r"<[^>]+>", "", blog_docs[0].get("contents", ""))).strip()
        review = raw[:100] + ("…" if len(raw) > 100 else "") if raw else review
        review_url = safe_url(blog_docs[0].get("url"))
    return image_url, review, review_url

def select_theme(theme):
    state = st.session_state
    state.active_theme = theme
    state.app_started = True
    if theme in CELEB_RESTAURANTS:
        state.search_mode, state.search_query = "celeb", theme
    else:
        keyword = {"전체":"맛집", "카페":"카페", "날씨별 추천":quick_keyword, "지역별 명소":"가볼만한곳 명소"}.get(theme, "맛집")
        state.search_mode, state.search_query = "keyword", f"{state.region_input.strip() or '강남역'} {keyword}"

current_temp, weather_desc = get_current_weather(WEATHER_API_KEY)
weather_title, food_desc, quick_keyword = recommend_menu_by_weather(current_temp, weather_desc)

markup('<div id="top"></div><div class="notice"><b>오늘의 작은 여행</b> 익숙한 동네에서 발견하는 새로운 한 끼</div>')
markup('''<nav class="nav"><a class="logo" href="#top">오모먹<span style="color:#268349">.</span><small>OH! MORE TASTE</small></a><div class="nav-links"><a href="#discover">맛집 찾기</a><a class="optional" href="#collections">테마 컬렉션</a><a class="optional" href="#travel">여행 도구</a><a class="nav-cta" href="#discover">오늘의 맛집 찾기 ↗</a></div></nav>''')
markup(f'''<section class="hero" style="--seoul:url('{SEOUL_PHOTO}')"><div class="eyebrow">A TASTE OF SEOUL</div><h1>오늘 뭐 먹지?<br>서울에서 맛있는 답을 찾다.</h1><p>골목 속 작은 식당부터, 한 번쯤 가보고 싶은 맛집까지.<br>당신의 다음 한 끼를 오모먹과 함께 발견해 보세요.</p><div class="location">SEOUL, SOUTH KOREA</div><a class="photo-credit" href="{PHOTO_SOURCE}" target="_blank" rel="noopener noreferrer">Photo · Minku Kang / Unsplash</a></section>''')
markup('<section class="intro" id="discover"><div class="green">취향에 맞게, 맛있게</div><h2>어떤 맛집을 찾고 있나요?</h2><p>지역과 테마를 고르면, 오늘의 목적지가 정해져요.</p></section>')

with st.form("main_search"):
    col_region, col_query, col_submit = st.columns([1.2, 2.7, 1])
    with col_region:
        region = st.text_input("지역", key="region_input", placeholder="예: 성수동, 강남역, 제주")
    with col_query:
        free_query = st.text_input("먹고 싶은 메뉴 또는 장소", placeholder="예: 파스타, 분위기 좋은 카페 · 비우면 지역 맛집 검색")
    with col_submit:
        st.markdown('<div style="height:27px"></div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("맛집 찾기 ↗", type="primary", use_container_width=True)
    if submitted:
        if not region.strip() and not free_query.strip():
            st.warning("지역이나 메뉴를 입력해 주세요.")
        else:
            st.session_state.search_query = " ".join(s for s in [region.strip(), free_query.strip() or "맛집"] if s)
            st.session_state.search_mode = "keyword"
            st.session_state.active_theme = "전체"
            st.session_state.app_started = True
st.caption("장소 검색은 국내 지역을 지원합니다. 지역을 비우면 입력한 검색어만으로 자유 검색합니다.")

themes = ["전체", "카페", "성시경 먹을텐데", "이영자 맛집", "카리나 맛집", "날씨별 추천", "지역별 명소"]
for column, theme in zip(st.columns(len(themes)), themes):
    with column:
        st.button(theme, key=f"theme_{theme}", type="primary" if st.session_state.active_theme == theme else "secondary", on_click=select_theme, args=(theme,), use_container_width=True)

if not st.session_state.app_started:
    markup('<div class="section-head" id="collections"><h2>취향을 발견하는 테마 컬렉션</h2><span>마음에 드는 테마로 시작해 보세요</span></div>')
    collections = [
        ("성시경 먹을텐데", "한 끼에 진심인 당신에게", "A good meal.", "#eee9df", "#635441"),
        ("이영자 맛집", "든든하고 맛있는 한 상", "Comfort food.", "#e9eee6", "#486044"),
        ("카리나 맛집", "오늘은 조금 새로운 취향", "Find your taste.", "#f1e7e4", "#835951"),
        ("카페", "커피 한 잔, 잠깐의 여유", "Slow moments.", "#e6edf0", "#4b6470"),
    ]
    for column, (theme, subtitle, title, background, color) in zip(st.columns(4), collections):
        with column:
            markup(f'<article class="collection"><div class="collection-art" style="background:{background};color:{color}"><strong>{title}</strong></div><div class="collection-body"><h3>{theme}</h3><p>{subtitle}</p></div></article>')
            st.button(f"{theme} 둘러보기 ↗", key=f"collection_{theme}", on_click=select_theme, args=(theme,), use_container_width=True)

weather_label = f"서울 기준 · {current_temp:.1f}°C · {weather_desc}" if current_temp is not None else weather_desc
markup(f'<div class="weather"><small>{esc(weather_label)}</small><strong>{esc(weather_title)}</strong><p>{esc(food_desc)}</p></div>')
if current_temp is not None:
    weather_icon = "🌤️"
    for keyword, icon in [("맑", "☀️"), ("구름", "⛅"), ("흐", "☁️"), ("안개", "🌫️"), ("비", "🌧️"), ("소나기", "🌧️"), ("눈", "🌨️"), ("천둥", "⛈️")]:
        if keyword in weather_desc:
            weather_icon = icon
    temperature_text = f"{current_temp:.1f}°C"
    condition_text = weather_desc or "날씨 설명 없음"
else:
    weather_icon = "🌡️"
    temperature_text = "— °C"
    condition_text = "날씨 연결 대기" if not WEATHER_API_KEY else "날씨 조회 실패"
weather_note = "서울 날씨에 맞춘 메뉴 추천" if current_temp is not None else weather_desc
weather_meta = "OpenWeather 제공 · 서울 기준" if current_temp is not None else "날씨 정보가 연결되면 표시됩니다"
markup(f'<div class="weather"><div class="weather-menu"><small>{esc(weather_note)}</small><strong>{esc(weather_title)}</strong><p>{esc(food_desc)}</p></div><div class="weather-today"><span class="weather-icon" aria-hidden="true">{weather_icon}</span><div><small>오늘의 서울 날씨 · 현재 기온</small><div class="weather-temperature">{temperature_text}</div><div class="weather-condition">{esc(condition_text)}</div><small>{weather_meta}</small></div></div></div>')
st.button(f"{st.session_state.region_input.strip() or '강남역'} {quick_keyword} 찾아보기 →", on_click=select_theme, args=("날씨별 추천",))

if not DOTENV_AVAILABLE:
    st.warning("기존 .env를 읽으려면 python-dotenv 패키지가 필요합니다. 터미널에서 pip install python-dotenv를 실행해 주세요.")

if st.session_state.app_started:
    markup(f'<div class="section-head" id="collections"><h2>{esc(st.session_state.search_query)}</h2><span>오늘의 맛있는 발견</span></div>')
    places, errors = [], []
    if not KAKAO_REST_KEY:
        st.info("기존 .env 파일의 KAKAO_REST_API_KEY를 설정하면 실제 검색 결과와 지도가 표시됩니다.")
    else:
        with st.spinner("가보고 싶은 곳들을 찾고 있어요..."):
            if st.session_state.search_mode == "celeb":
                for query in CELEB_RESTAURANTS.get(st.session_state.search_query, []):
                    found, error = search_places(query, KAKAO_REST_KEY)
                    if error: errors.append(error)
                    if found: places.append(found[0])
            else:
                places, error = search_places(st.session_state.search_query, KAKAO_REST_KEY)
                if error: errors.append(error)
        places = list({p.get("id", p.get("place_url", str(i))): p for i, p in enumerate(places)}.values())
    if st.session_state.search_mode == "celeb":
        st.caption("지역과 무관한 기존 전국 목록입니다. 이름별 검색의 첫 결과를 사용하므로 방문 전 주소와 해당 매장을 확인해 주세요.")
    for error in set(errors): st.warning(error)
    if errors and st.button("검색 다시 시도"):
        search_places.clear()
        st.rerun()

    if not places:
        markup('<div class="empty"><b>다음 맛있는 발견을 기다리고 있어요.</b>지역이나 메뉴를 바꿔 검색해 보세요.</div>')
    else:
        def enrich(place):
            address = place.get("road_address_name") or place.get("address_name", "")
            details = get_place_details(place.get("place_name", ""), address.split()[0] if address else "", KAKAO_REST_KEY)
            return {**place, "address":address, "image":details[0], "review":details[1], "review_url":details[2]}
        with st.spinner("장소 사진과 관련 글을 준비하고 있어요..."):
            with ThreadPoolExecutor(max_workers=4) as executor:
                enriched = list(executor.map(enrich, places))
        st.caption(f"{len(enriched)}곳 · 사진과 글은 관련 검색 결과로 실제 매장 정보와 다를 수 있습니다.")
        for start in range(0, len(enriched), 4):
            for index, (column, place) in enumerate(zip(st.columns(4), enriched[start:start+4]), start+1):
                with column:
                    photo = f'<img src="{esc(place["image"])}" alt="{esc(place.get("place_name"))} 관련 검색 사진" loading="lazy" referrerpolicy="no-referrer">' if place["image"] else '<div class="no-photo">등록된 사진이 없어요</div>'
                    url = safe_url(place.get("place_url"))
                    link = f'<a class="place-link" href="{esc(url)}" target="_blank" rel="noopener noreferrer">카카오맵에서 자세히 보기 ↗</a>' if url else ""
                    blog_link = f'<a class="place-link" href="{esc(place["review_url"])}" target="_blank" rel="noopener noreferrer">블로그 원문 ↗</a>' if place["review_url"] else ""
                    category = place.get("category_group_name") or "장소"
                    markup(f'<article class="place"><div class="place-photo">{photo}<span class="place-number">{index:02d}</span></div><div class="place-body"><div class="tag">{esc(category)}</div><h3>{esc(place.get("place_name"))}</h3><div class="address">{esc(place["address"])}</div><div class="review">{esc(place["review"])}</div>{blog_link}{link}</div></article>')

        markup('<div class="section-head"><h2>지도에서 한눈에 둘러보기</h2><span>번호는 위 장소 카드와 같아요</span></div>')
        if folium is None:
            st.info("지도를 표시하려면 기존 패키지가 필요합니다: pip install folium streamlit-folium")
        else:
            points = []
            m = folium.Map(location=[37.5665,126.9780], zoom_start=12, tiles="CartoDB positron")
            for index, place in enumerate(enriched, 1):
                try:
                    lat, lng = float(place["y"]), float(place["x"])
                    if not (math.isfinite(lat) and math.isfinite(lng) and -90 <= lat <= 90 and -180 <= lng <= 180): continue
                except (KeyError, ValueError, TypeError): continue
                points.append([lat, lng])
                url = safe_url(place.get("place_url"))
                popup_link = f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">카카오맵 열기 ↗</a>' if url else ""
                popup = f'<div style="width:220px;font-family:sans-serif;line-height:1.6"><b>{index}. {esc(place.get("place_name"))}</b><p>{esc(place["address"])}</p><p>{esc(place["review"])}</p>{popup_link}</div>'
                color = "#b67c3b" if "카페" in place.get("category_name", "") else "#268349"
                icon = folium.DivIcon(html=f'<div style="background:{color};color:white;width:30px;height:30px;border-radius:50%;border:2px solid white;box-shadow:0 2px 6px #0003;display:flex;align-items:center;justify-content:center;font-weight:bold">{index}</div>', icon_size=(30,30), icon_anchor=(15,15))
                folium.Marker([lat,lng], tooltip=esc(place.get("place_name")), popup=folium.Popup(popup, max_width=260), icon=icon).add_to(m)
            if points: m.fit_bounds(points, padding=(35,35), max_zoom=15)
            st_folium(m, use_container_width=True, height=520, returned_objects=[], key=f"map_{st.session_state.search_query}")

markup('<div id="travel"></div>')
with st.expander("여행을 준비한다면 · 환율 계산기", expanded=False):
    if not EXCHANGE_API_KEY:
        st.caption("기존 .env 파일에 EXCHANGE_API_KEY를 설정하면 이용할 수 있습니다.")
    else:
        a, b, c = st.columns(3)
        with a: base_cur = st.selectbox("기준 통화", ["USD", "EUR", "JPY", "KRW"])
        with b: amount = st.number_input("금액", min_value=0.0, value=100.0, step=10.0)
        with c: target_cur = st.selectbox("변환 통화", ["KRW", "USD", "EUR", "JPY"])
        rates = get_exchange_rate(EXCHANGE_API_KEY, base_cur)
        if rates and target_cur in rates:
            st.success(f"{amount:,.2f} {base_cur} = {amount * rates[target_cur]:,.2f} {target_cur}")
            st.caption("환율은 최대 1시간 캐시됩니다. 실제 환전 시 적용되는 금액은 수수료 등에 따라 달라질 수 있습니다.")