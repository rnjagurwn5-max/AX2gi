# 날씨 API 실습 
# OpenWeatehrMap 현재 날씨 API로 특정 도시의 날씨를 가져와 출력한다.
# 사전준비 API 회원가입해서 발급 받기
# pip install requests python-dotenv
#.env 파일을 생성하고 이곳에 OPENWEATHER_API_KEY=발급받은_API_키 / 진짜 api키는 git에 올라가면 안됨.
#.env.example OPENWEATHER_API_KEY=your_key / 이 형태만 올라갔다 내려갔다 하는 것. 진짜 키 안넣고 니 키 넣으라고 알려주는 것
#.env.example 받아서 .env로 이름바꾸고 자기 API를 채운다.
#import os

# import requests
# import streamlit
# from dotenv import load_dotenv
# load_dotenv() # .env 파일을 읽어 환경 변수로 등록한다
# API_KEY = os.getenv("OPENWEATHER_API_KEY")
# .env는 상위 폴더에 있어
# 서비스앱 코드 만들어줘, 반응형으로 


import os
import requests
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# 1. 환경 변수 로드 (.env 파일)
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', '.env')
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

# 2. 페이지 기본 설정 (와이드 레이아웃)
st.set_page_config(page_title="글로벌 날씨 & 환율 서비스", page_icon="🌤️", layout="wide")

# --- 유틸리티 함수 ---
def get_bg_image(weather_main):
    if weather_main == "Clear":
        return "https://images.unsplash.com/photo-1601297183305-6df142704ea2?q=80&w=1920&auto=format&fit=crop"
    elif weather_main == "Clouds":
        return "https://images.unsplash.com/photo-1534088568595-a066f410cbda?q=80&w=1920&auto=format&fit=crop"
    elif weather_main in ["Rain", "Drizzle"]:
        return "https://images.unsplash.com/photo-1519692933481-e162a57d6721?q=80&w=1920&auto=format&fit=crop"
    elif weather_main == "Snow":
        return "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?q=80&w=1920&auto=format&fit=crop"
    elif weather_main == "Thunderstorm":
        return "https://images.unsplash.com/photo-1605727216801-e27ce1d0ce5b?q=80&w=1920&auto=format&fit=crop"
    else:
        return "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?q=80&w=1920&auto=format&fit=crop"

def get_outfit_recommendation(temp_c, wind_ms, weather_main):
    """기온(섭씨), 풍속(m/s), 날씨 상태에 따른 옷차림 추천"""
    if temp_c >= 28: outfit = "민소매, 반팔, 반바지, 린넨 소재 옷"
    elif temp_c >= 23: outfit = "반팔, 얇은 셔츠, 반바지, 면바지"
    elif temp_c >= 20: outfit = "얇은 가디건, 긴팔, 면바지, 청바지"
    elif temp_c >= 17: outfit = "얇은 니트, 맨투맨, 가디건, 청바지"
    elif temp_c >= 12: outfit = "자켓, 가디건, 야상, 두꺼운 바지"
    elif temp_c >= 9: outfit = "트렌치코트, 야상, 두꺼운 니트, 청바지"
    elif temp_c >= 5: outfit = "코트, 가죽자켓, 히트텍, 니트, 레깅스"
    else: outfit = "패딩, 두꺼운 코트, 목도리, 기모제품"
    
    advice = f"👕 **추천 옷차림:** {outfit}"
    
    if wind_ms >= 10: 
        advice += " (바람이 강하니 여밀 수 있는 겉옷을 챙기세요!)"
    if weather_main in ["Rain", "Drizzle", "Thunderstorm"]:
        advice += " ☔ **우산을 꼭 챙기세요!**"
    elif weather_main == "Snow":
        advice += " ❄️ **눈이 오니 미끄러지지 않는 신발을 신으세요!**"
        
    return advice

weather_explanations = {
    "맑음": "구름 없음",
    "약간의 구름": "구름 11~25%",
    "흩어진 구름": "구름 25~50%",
    "튼구름": "구름 51~84% (구름 사이로 틈이 있어 하늘이 보임)",
    "온흐림": "구름 85~100% (빈틈없이 잔뜩 흐림)"
}

country_to_currency = {
    "US": "USD", "JP": "JPY", "GB": "GBP", "CN": "CNY",
    "FR": "EUR", "DE": "EUR", "IT": "EUR", "ES": "EUR", "NL": "EUR",
    "AU": "AUD", "CA": "CAD", "CH": "CHF", "KR": "KRW", "TW": "TWD",
    "HK": "HKD", "SG": "SGD", "IN": "INR", "RU": "RUB", "AE": "AED",
    "VN": "VND", "TH": "THB", "PH": "PHP", "MY": "MYR", "ID": "IDR"
}

# 기본 변수 설정
bg_url = "https://images.unsplash.com/photo-1499346156599-71525b682666?q=80&w=1920&auto=format&fit=crop"
weather_data = None
exchange_rate = None
display_currency = None

# --- 동적 CSS 적용 ---
css = f"""
<style>
.stApp {{
    background-image: url("{bg_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.main .block-container {{
    background-color: rgba(255, 255, 255, 0.90); 
    padding: 3rem;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
    margin-top: 2rem;
    margin-bottom: 2rem;
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)


# --- 1. 왼쪽 사이드바 (입력 영역) ---
with st.sidebar:
    # 사이드바 폭에 맞춘 배너 디자인
    sidebar_header_html = """
    <div style="
        background: linear-gradient(135deg, rgba(240, 244, 255, 0.8) 0%, rgba(229, 235, 245, 0.8) 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #4A90E2;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    ">
        <h2 style="margin: 0; font-size: 1.4rem; color: #2C3E50; font-weight: 800;">
            🌤️ 글로벌 날씨 & 환율
        </h2>
        <p style="margin: 10px 0 0 0; font-size: 0.9rem; color: #34495E; line-height: 1.4;">
            도시를 검색하여 현지 날씨, 추천 옷차림, 실시간 환율을 한 번에 확인하세요.
        </p>
    </div>
    """
    st.markdown(sidebar_header_html, unsafe_allow_html=True)
    
    city_name = st.text_input("도시 이름", "Seoul", placeholder="예: Seoul, Tokyo, Paris")
    unit_choice = st.radio("온도 단위", ["섭씨 (°C)", "화씨 (°F)"])
    search_button = st.button("날씨 및 환율 검색", type="primary", use_container_width=True)

# API 단위 설정
api_unit = "metric" if unit_choice == "섭씨 (°C)" else "imperial"
temp_symbol = "°C" if api_unit == "metric" else "°F"
speed_symbol = "m/s" if api_unit == "metric" else "mph"


# --- 2. 데이터 호출 로직 ---
if search_button:
    if not API_KEY:
        st.sidebar.error("날씨 API 키를 찾을 수 없습니다.")
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units={api_unit}&lang=kr"
        
        try:
            response = requests.get(url)
            weather_data = response.json()
            
            if response.status_code == 200:
                weather_main = weather_data["weather"][0]["main"]
                bg_url = get_bg_image(weather_main)
                
                # 환율 데이터 호출
                country_code = weather_data["sys"]["country"]
                currency_code = country_to_currency.get(country_code)
                display_currency = "USD" if currency_code == "KRW" else currency_code
                
                if display_currency and EXCHANGE_API_KEY:
                    ex_url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{display_currency}"
                    ex_response = requests.get(ex_url)
                    if ex_response.status_code == 200:
                        ex_data = ex_response.json()
                        exchange_rate = ex_data["conversion_rates"].get("KRW")
                        
            elif response.status_code == 404:
                st.warning("입력하신 도시를 찾을 수 없습니다. 영문 철자를 확인해주세요.")
            else:
                st.error(f"오류가 발생했습니다: {weather_data.get('message', '알 수 없는 오류')}")
        except Exception as e:
            st.error(f"API 요청 중 문제가 발생했습니다: {e}")


# --- 3. 메인 화면 출력부 ---
if weather_data and weather_data.get("cod") == 200:
    weather_desc = weather_data["weather"][0]["description"]
    icon_code = weather_data["weather"][0]["icon"]
    weather_main = weather_data["weather"][0]["main"]
    
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    
    lat = weather_data["coord"]["lat"]
    lon = weather_data["coord"]["lon"]
    country_code = weather_data["sys"]["country"]
    
    # 옷차림 분석을 위한 내부 단위 통일(무조건 섭씨, m/s 기준으로 변환)
    temp_c = temp if api_unit == "metric" else (temp - 32) * 5.0/9.0
    wind_ms = wind_speed if api_unit == "metric" else wind_speed * 0.44704
    
    st.subheader(f"📍 {city_name.capitalize()} ({country_code}) 현재 상황")
    
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
    
    # 상단 지표 카드
    col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
    with col1:
        st.image(icon_url)
    with col2:
        st.write(f"## {weather_desc.capitalize()}")
        if weather_desc in weather_explanations:
            st.caption(f"💡 {weather_explanations[weather_desc]}")
        st.write(f"현재 온도: **{temp}{temp_symbol}** (체감: {feels_like}{temp_symbol})")
    with col3:
        st.metric(label="💧 습도", value=f"{humidity} %")
    with col4:
        st.metric(label=f"🌬️ 풍속 ({speed_symbol})", value=f"{wind_speed}")
    with col5:
        if exchange_rate:
            if display_currency == "JPY":
                st.metric(label=f"💱 환율 (100 {display_currency})", value=f"{exchange_rate * 100:,.2f} 원")
            else:
                st.metric(label=f"💱 환율 (1 {display_currency})", value=f"{exchange_rate:,.2f} 원")
        else:
            st.metric(label="💱 환율", value="정보 없음")
            
    # 맞춤형 옷차림 추천 박스
    outfit_text = get_outfit_recommendation(temp_c, wind_ms, weather_main)
    st.info(outfit_text)
    
    st.divider()
    
    # 지도 출력부
    st.subheader("🗺️ 상세 위치 정보")
    m = folium.Map(location=[lat, lon], zoom_start=11)
    
    popup_html = f"""
    <div style="font-family: Arial; min-width: 150px;">
        <h4 style="margin-bottom: 5px; color: #2c3e50;">{city_name.capitalize()}</h4>
        <p style="margin: 0; font-size: 14px;"><b>날씨:</b> {weather_desc}</p>
        <p style="margin: 0; font-size: 14px;"><b>온도:</b> {temp}{temp_symbol}</p>
    </div>
    """
    
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip="날씨 세부정보 보기",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    st_folium(m, width="100%", height=400, returned_objects=[]) 