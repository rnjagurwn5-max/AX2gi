# import requests
# import streamlit
# from dotenv import load_dotenv
# load_dotenv() # .env 파일을 읽어 환경 변수로 등록한다
# API_KEY = os.getenv("EXCHANGE_API_KEY")
# .env는 상위 폴더에 있어
# 서비스앱 코드 만들어줘, 반응형으로 

# 7. 환 위험 관리 정보
st.markdown("<div style='margin-top: 10vh;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="background-color: rgba(30, 34, 42, 0.85); padding: 30px; border-radius: 10px; color: white; line-height: 1.6;">
    <h3 style="color: #6C8EBF;">🌐 수입/수출 기업의 환 위험(Exchange Risk) 이해</h3>
    <p>환 위험이란 환율 변동으로 인해 기업의 영업이익이나 자산 가치가 변동할 수 있는 불확실성을 의미합니다.</p>
    <br>
    
    <h3 style="color: #6C8EBF;">📈 환율 절상/절하에 따른 위험과 기회</h3>
    <p><strong>1. 환율 절상 (자국 통화 가치 상승 / 환율 하락)</strong></p>
    <ul>
        <li><strong>수출 기업:</strong> (위험) 외화 대금 환전 시 환차손 발생, 가격 경쟁력 약화 / (기회) 원자재 수입 비중이 높을 경우 제조 원가 하락</li>
        <li><strong>수입 기업:</strong> (기회) 동일한 외화 결제 대금 대비 자국 통화 지출이 줄어들어 수입 원가 절감 및 마진 확대</li>
    </ul>
    <br>
    
    <p><strong>2. 환율 절하 (자국 통화 가치 하락 / 환율 상승)</strong></p>
    <ul>
        <li><strong>수출 기업:</strong> (기회) 외화 대금 환전 시 환차익 발생, 해외 시장에서의 가격 경쟁력 향상</li>
        <li><strong>수입 기업:</strong> (위험) 수입 결제 대금 부담이 급증하여 채산성 악화 및 원가 상승 압박</li>
    </ul>
    <br>

    <h3 style="color: #6C8EBF;">🛡️ 환 위험 헷지(Hedge) 및 대응 방안</h3>
    <p><strong>1. 대내적 관리 방안 (기업 내부 통제)</strong></p>
    <ul>
        <li><strong>매칭 (Matching):</strong> 외화의 유입(수출 대금)과 유출(수입 대금) 시기 및 금액을 일치시켜 외환 포지션을 최소화합니다.</li>
        <li><strong>리딩과 래깅 (Leading & Lagging):</strong> 환율 전망에 따라 외화 결제 시기를 의도적으로 앞당기거나(Leading) 늦추는(Lagging) 전략입니다.</li>
        <li><strong>결제 통화 다변화:</strong> 특정 국가의 통화에만 의존하지 않고 결제 통화를 분산시킵니다.</li>
    </ul>
    <br>
    
    <p><strong>2. 대외적 관리 방안 (금융 상품 활용)</strong></p>
    <ul>
        <li><strong>선물환 (Forward Contract):</strong> 미래의 특정 시점에 미리 약정한 환율로 외화를 사고팔기로 은행과 계약하여 환율 변동 위험을 차단합니다.</li>
        <li><strong>환변동보험:</strong> 한국무역보험공사(K-SURE) 등에서 제공하는 보험으로, 환율 하락으로 인한 손실은 보상받고 환율 상승 시의 이익은 반납하는 구조입니다. 중소기업의 접근성이 좋습니다.</li>
        <li><strong>통화 옵션 (Currency Option):</strong> 미래에 특정 환율로 외화를 매매할 수 있는 '권리'를 사는 것으로, 유리할 때만 권리를 행사할 수 있어 유연성이 높습니다.</li>
    </ul>
    
    <!-- KITA 무역협회 상담 서비스 바로가기 버튼 -->
    <a href="https://tradesos.kita.net/" target="_blank" class="kita-link-btn" style="display: block; width: 100%; text-align: center; background-color: #2E5BFF; color: #FFFFFF !important; padding: 15px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 1.1rem; margin-top: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
        📞 KITA 한국무역협회 수출/수입 상담 서비스 바로가기
    </a>
</div>
""", unsafe_allow_html=True)