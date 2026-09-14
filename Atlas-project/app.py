import math
import feedparser
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 1. 항구 및 해상 관문 샘플 데이터 (위도/경도)
PORTS = [
    {"id": "KRBUS", "name": "Busan", "lat": 35.1016, "lon": 129.0300},
    {"id": "SGSIN", "name": "Singapore", "lat": 1.2743, "lon": 103.8024},
    {"id": "EGSUZ", "name": "Suez Canal", "lat": 30.5852, "lon": 32.2654},
    {"id": "ZACPT", "name": "Cape of Good Hope", "lat": -34.3568, "lon": 18.4710},
    {"id": "NLRTM", "name": "Rotterdam", "lat": 51.9496, "lon": 4.1450}
]

# 위험 키워드 사전
RISK_KEYWORDS = ["지연", "파업", "혼잡", "체선", "사고", "delay", "strike", "congestion"]

# 2. 두 지점 간 거리 계산 함수 (대체 항구 탐색용, Haversine 공식)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (km)
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ports')
def get_ports():
    return jsonify(PORTS)

# 3. 공개 RSS 수집 및 위험/거점 키워드 추출
@app.route('/api/news/<port_name>')
def get_news(port_name):
    # 실제 RSS URL (예: 로이드 리스트 등)을 입력하세요. 아래는 가상의 테스트 데이터입니다.
    # rss_url = "https://example.com/logistics/rss"
    # feed = feedparser.parse(rss_url)
    
    mock_rss_entries = [
        {"title": f"{port_name} 터미널 파업으로 인해 선박 하역 지연", "link": "#", "published": "2026-09-14"},
        {"title": "글로벌 해운사, 운임 인상 발표", "link": "#", "published": "2026-09-13"}
    ]
    
    filtered_news = []
    for entry in mock_rss_entries:
        title = entry['title']
        # 기사 제목에 선택한 항구 이름이 있거나, 위험 키워드가 포함된 경우 추출
        has_port = port_name.lower() in title.lower()
        has_risk = any(risk in title for risk in RISK_KEYWORDS)
        
        if has_port or has_risk:
            filtered_news.append({
                "title": title, "link": entry['link'], "date": entry['published']
            })
            
    return jsonify(filtered_news)

# 4. 가까운 대체 거점 찾기
@app.route('/api/alternatives/<port_id>')
def get_alternatives(port_id):
    target = next((p for p in PORTS if p['id'] == port_id), None)
    if not target: return jsonify([])
    
    alts = []
    for p in PORTS:
        if p['id'] != port_id:
            dist = calculate_distance(target['lat'], target['lon'], p['lat'], p['lon'])
            alts.append({"name": p['name'], "dist_km": round(dist, 1)})
            
    # 거리순 정렬 후 가장 가까운 2개 추천
    alts.sort(key=lambda x: x['dist_km'])
    return jsonify(alts[:2])

if __name__ == '__main__':
    # use_reloader=False를 추가하여 시그널 충돌 방지
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)