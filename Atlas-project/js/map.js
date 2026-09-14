// 지도 초기화 (중심 좌표와 줌 레벨 설정)
const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 백엔드에서 항구 좌표를 불러와 마커 생성
fetch('/api/ports')
    .then(res => res.json())
    .then(ports => {
        ports.forEach(port => {
            const marker = L.marker([port.lat, port.lon]).addTo(map);
            marker.bindPopup(`<b>${port.name}</b><br>클릭하여 분석 보기`);
            marker.on('click', () => analyzePort(port));
        });
    });

// 거점 선택 시 뉴스 및 대체항로 조회
function analyzePort(port) {
    const panel = document.getElementById('info-panel');
    panel.innerHTML = `<p><b>${port.name}</b> 데이터 수집 중...</p>`;
    
    Promise.all([
        fetch(`/api/news/${port.name}`).then(r => r.json()),
        fetch(`/api/alternatives/${port.id}`).then(r => r.json())
    ]).then(([news, alts]) => {
        let html = `<h3>이슈 뉴스 (키워드 추출)</h3>`;
        if(news.length === 0) html += `<p>검출된 위험/이슈 기사가 없습니다.</p>`;
        
        news.forEach(n => {
            html += `<div class="card risk">
                        <a href="${n.link}" target="_blank">${n.title}</a><br>
                        <small>${n.date}</small>
                     </div>`;
        });

        html += `<h3>인근 대체 거점 후보</h3>`;
        alts.forEach(a => {
            html += `<p>⚓ ${a.name} (약 ${a.dist_km}km)</p>`;
        });
        
        panel.innerHTML = html;
    });
}

// 우회 시나리오 비교 로직
function compareScenario() {
    const panel = document.getElementById('scenario-panel');
    panel.innerHTML = `
        <div class="card">
            <h4>[기본] 수에즈 운하</h4>
            <p>거리: 약 18,520 km (아시아-유럽)<br>소요: 약 25.5일</p>
        </div>
        <div class="card risk">
            <h4>[우회] 희망봉 (Cape of Good Hope)</h4>
            <p>거리: 약 24,000 km<br>소요: 약 34일 <b>(+8.5일 지연)</b><br>이슈: 운임 상승, 벙커유 추가 소모</p>
        </div>
    `;
}