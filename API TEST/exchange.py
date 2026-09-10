# import requests
# import streamlit
# from dotenv import load_dotenv
# load_dotenv() # .env 파일을 읽어 환경 변수로 등록한다
# API_KEY = os.getenv("EXCHANGE_API_KEY")
# .env는 상위 폴더에 있어
# 서비스앱 코드 만들어줘, 반응형으로 

import os
import requests
import streamlit as st
import yfinance as yf
import plotly.express as px
from dotenv import load_dotenv

# 1. 환경 변수 로드 (.env 파일이 exchange.py와 같은 폴더에 있을 때)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
API_KEY = os.getenv("EXCHANGE_API_KEY")

# 2. 페이지 설정
st.set_page_config(page_title="실시간 환율 계산기", layout="wide")

# 3. 디자인: CSS 업데이트 (반응형 미디어 쿼리 추가)
page_bg_img = """
<style>
/* 심플한 그래픽/도트 스타일의 모던한 세계 지도 배경 */
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(15, 23, 42, 0.7), rgba(15, 23, 42, 0.7)), url("https://images.unsplash.com/photo-1589519160732-57fc498494f8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }

/* 데스크탑 기본 텍스트 스타일 */
.title-text { color: white; font-size: 4rem; font-weight: 800; margin-top: 15vh; line-height: 1.2; }
.sub-text { color: #e0e0e0; font-size: 1.2rem; margin-top: 20px; margin-bottom: 40px; }

/* 버튼 색상 */
div.stButton > button:first-child { background-color: #6C8EBF !important; color: white !important; border: none !important; border-radius: 8px !important; }
div.stButton > button:first-child:hover { background-color: #5A7CA6 !important; }

/* 오른쪽 계산기 팝업 배경 (반응형을 위해 클래스로 분리) */
.calc-container {
    background-color: rgba(30, 34, 42, 0.85); 
    padding: 2.5rem;
    border-radius: 15px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(8px);
    margin-top: 10vh;
}

/* 위젯 라벨 및 입력창 */
label { color: #FFFFFF !important; font-weight: bold; }
div[data-baseweb="select"] > div, input[type="number"] { background-color: #F0F2F6 !important; color: #111111 !important; }

/* 조회 기간 라디오 버튼의 텍스트를 확실한 흰색으로 강제 지정 */
.stRadio [data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* ★ 추가: 모바일 반응형 미디어 쿼리 (화면 폭이 768px 이하일 때 적용) ★ */
@media (max-width: 768px) {
    .title-text {
        font-size: 2.5rem !important; /* 모바일에서 글자 크기 축소 */
        margin-top: 5vh !important;   /* 모바일에서 상단 여백 축소 */
    }
    .sub-text {
        font-size: 1rem !important;
    }
    .calc-container {
        margin-top: 2vh !important;   /* 모바일에서 팝업 여백 축소 */
        padding: 1.5rem !important;   /* 모바일에서 내부 여백 축소 */
    }
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 4. 세션 상태 초기화
if 'show_calc' not in st.session_state:
    st.session_state.show_calc = False

def toggle_calculator():
    st.session_state.show_calc = not st.session_state.show_calc

# 5. 메인 레이아웃 구성
col1, col2 = st.columns([1.2, 1])

base_currency = "USD"
target_currency = "KRW"

with col1:
    st.markdown('<div class="title-text">실시간<br>환율 계산기</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">전 세계의 실시간 환율을 빠르고 정확하게 확인하고 비즈니스 경쟁력을 높이세요.</div>', unsafe_allow_html=True)
    st.button("환율 계산하기", on_click=toggle_calculator, type="primary")

with col2:
    if st.session_state.show_calc:
        # ★ 수정: 반응형 CSS(calc-container)가 적용되도록 div로 계산기 영역을 감쌈
        st.markdown('<div class="calc-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #FFFFFF; margin-bottom: 15px;">💱 환율 변환</h3>', unsafe_allow_html=True)
        
        base_currency = st.selectbox("보유 통화 (Base)", ["KRW", "USD", "EUR", "JPY", "CNY", "GBP"], index=1)
        target_currency = st.selectbox("변경 통화 (Target)", ["USD", "KRW", "EUR", "JPY", "CNY", "GBP"], index=1)
        amount = st.number_input("금액", min_value=0.0, value=1000.0, step=100.0)
        
        if st.button("계산 실행", use_container_width=True):
            if not API_KEY:
                st.error("API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
            else:
                with st.spinner("환율 정보를 가져오는 중..."):
                    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base_currency}/{target_currency}/{amount}"
                    try:
                        response = requests.get(url)
                        response.raise_for_status()
                        data = response.json()
                        if data.get('result') == 'success':
                            converted = data['conversion_result']
                            rate = data['conversion_rate']
                            result_html = f"""
                            <div style="background-color: #FFFFFF; color: #000000; padding: 15px; border-radius: 8px; text-align: center; font-size: 1.1rem; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                <strong>{amount:,.2f} {base_currency}</strong> = <strong style="color: #2E5BFF; font-size: 1.3rem;">{converted:,.2f} {target_currency}</strong>
                                <hr style="margin: 10px 0; border: 0; border-top: 1px solid #E0E0E0;">
                                <span style="font-size: 0.9rem; color: #555555;">적용 환율: 1 {base_currency} = {rate} {target_currency}</span>
                            </div>
                            """
                            st.markdown(result_html, unsafe_allow_html=True)
                        else:
                            st.error("환율 정보를 가져오는데 실패했습니다. API 키를 확인해주세요.")
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {e}")
        
        # div 태그 닫기
        st.markdown('</div>', unsafe_allow_html=True)

# 6. 하단: 환율 변동 그래프 섹션
if st.session_state.show_calc:
    st.markdown("<div style='margin-top: 5vh;'></div>", unsafe_allow_html=True)
    st.markdown('<h3 style="color: white; border-bottom: 2px solid #6C8EBF; padding-bottom: 10px;">📈 환율 변동 추이</h3>', unsafe_allow_html=True)
    
    period_options = {
        "1일 (시간별)": ("1d", "1h"),
        "1개월 (일별)": ("1mo", "1d"),
        "1년 (주별)": ("1y", "1wk"),
        "5년 (월별)": ("5y", "1mo")
    }
    
    selected_period = st.radio("조회 기간 선택", list(period_options.keys()), horizontal=True)
    period, interval = period_options[selected_period]
    
    ticker_symbol = f"{base_currency}{target_currency}=X"
    
    with st.spinner("그래프 데이터를 불러오는 중..."):
        try:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if not hist.empty:
                fig = px.line(
                    hist, 
                    x=hist.index, 
                    y='Close',
                    labels={'Close': f'환율 ({target_currency})', 'index': '날짜/시간'}
                )
                
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(255,255,255,0.95)",
                    font=dict(color="black"),
                    xaxis=dict(
                        showgrid=True, 
                        gridcolor="rgba(200,200,200,0.4)",
                        showline=True,
                        linecolor="gray"
                    ),
                    yaxis=dict(
                        showgrid=True, 
                        gridcolor="rgba(200,200,200,0.6)",
                        showline=True,
                        linecolor="gray"
                    ),
                    hovermode="x unified"
                )
                fig.update_traces(line_color='#2E5BFF', line_width=2.5)
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"선택하신 통화쌍({base_currency}/{target_currency})의 과거 데이터를 불러올 수 없습니다.")
        except Exception as e:
            st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")

# 7. 환 위험 관리 정보
st.markdown("<div style='margin-top: 10vh;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="background-color: rgba(30, 34, 42, 0.85); padding: 30px; border-radius: 10px; color: white; line-height: 1.6;">
    <h3 style="color: #6C8EBF;">🌐 수입/수출 기업의 환 위험(Exchange Risk) 이해</h3>
    <p>환 위험이란 환율 변동으로 인해 기업의 영업이익이나 자산 가치가 변동할 수 있는 불확실성을 의미합니다.</p>
    <ul>
        <li><strong>수출 기업 (외화 수취):</strong> 환율 하락(원화 가치 상승) 시 타격을 받습니다. 제품을 팔고 받은 외화를 원화로 환전할 때 수령 금액이 줄어들기 때문입니다.</li>
        <li><strong>수입 기업 (외화 지급):</strong> 환율 상승(원화 가치 하락) 시 타격을 받습니다. 물건을 사오기 위해 지불해야 하는 원화 금액이 늘어나 원가 부담이 커지기 때문입니다.</li>
    </ul>
    <br>
    <h3 style="color: #6C8EBF;">🛡️ 환 위험 헷지(Hedge) 및 대응 방안</h3>
    <p><strong>1. 대내적 관리 방안 (기업 내부 통제)</strong></p>
    <ul>
        <li><strong>매칭 (Matching):</strong> 외화의 유입(수출 대금)과 유출(수입 대금) 시기 및 금액을 일치시켜 외환 포지션을 최소화합니다.</li>
        <li><strong>리딩과 래깅 (Leading & Lagging):</strong> 환율 전망에 따라 외화 결제 시기를 의도적으로 앞당기거나(Leading) 늦추는(Lagging) 전략입니다.</li>
        <li><strong>결제 통화 다변화:</strong> 특정 국가의 통화에만 의존하지 않고 결제 통화를 분산시킵니다.</li>
    </ul>
    <p><strong>2. 대외적 관리 방안 (금융 상품 활용)</strong></p>
    <ul>
        <li><strong>선물환 (Forward Contract):</strong> 미래의 특정 시점에 미리 약정한 환율로 외화를 사고팔기로 은행과 계약하여 환율 변동 위험을 차단합니다.</li>
        <li><strong>환변동보험:</strong> 한국무역보험공사(K-SURE) 등에서 제공하는 보험으로, 환율 하락으로 인한 손실은 보상받고 환율 상승 시의 이익은 반납하는 구조입니다. 중소기업의 접근성이 좋습니다.</li>
        <li><strong>통화 옵션 (Currency Option):</strong> 미래에 특정 환율로 외화를 매매할 수 있는 '권리'를 사는 것으로, 유리할 때만 권리를 행사할 수 있어 유연성이 높습니다.</li>
    </ul>
</div>
""", unsafe_allow_html=True)