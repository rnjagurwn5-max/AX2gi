import os
import webbrowser
import folium

# 1. 서울 시내 명소 4곳 샘플 데이터
places = [
    {"name": "서울시청", "lat": 37.5665, "lon": 126.9780},
    {"name": "경복궁", "lat": 37.5796, "lon": 126.9770},
    {"name": "남산서울타워", "lat": 37.5512, "lon": 126.9882},
    {"name": "여의도 한강공원", "lat": 37.5284, "lon": 126.9328},
]

# 2. 국토교통부 브이월드(Vworld) 타일 URL 및 출처(attr) 설정
# (개인 인증키 발급 전 테스트용 오픈키가 적용되어 있습니다. 장기 사용 시 vworld.kr에서 무료 키 발급 권장)
VWORLD_KEY = "CEB52025-E065-364C-9DBA-44880E3B02B8"
vworld_tiles = f"https://api.vworld.kr/req/wmts/1.0.0/{VWORLD_KEY}/Base/{{z}}/{{y}}/{{x}}.png"
attribution = "국토교통부 브이월드(Vworld)"

# 3. 지도 객체 생성 (서울시청 기준, 국토교통부 지도 타일 적용)
seoul_city_hall = [37.5665, 126.9780]
m = folium.Map(
    location=seoul_city_hall,
    zoom_start=13,
    tiles=vworld_tiles,  # 국토부 브이월드 지도 연결
    attr=attribution     # 지도 출처 표기 (필수)
)

# 4. 마커 일괄 추가
for place in places:
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=place["name"],
        tooltip=place["name"],
        icon=folium.Icon(color="red", icon="star")
    ).add_to(m)

# 5. HTML 파일 저장 및 브라우저 실행
file_name = "basic_map.html"
m.save(file_name)
webbrowser.open(os.path.abspath(file_name))