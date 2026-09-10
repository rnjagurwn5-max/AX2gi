#무역 직무 MBTI
#직무 6개
#질문 20개
#스트림릿

import streamlit as st
import streamlit.components.v1 as components
import math
import os
import urllib.parse

# 페이지 기본 설정
st.set_page_config(page_title="무역 직무 MBTI 매칭", page_icon="🚢", layout="centered")

# --- 전체 배경 톤 및 버튼 스타일링 (CSS) ---
st.markdown(
    """
    <style>
    /* 전체 배경 톤을 은은한 파스텔 블루/그레이로 변경 */
    .stApp {
        background: linear-gradient(180deg, #edf2f9 0%, #e5ecf6 100%);
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 기본 버튼 디자인 다듬기 */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 스크립트 파일이 위치한 절대 경로 (이미지 자동 추적)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- 1. 직무별 기준 데이터, 이미지, 맞춤 슬로건 및 리포트 매핑 ---
JOBS = {
    "해외영업": {
        "vector": (0.8, -0.1, -0.4, -0.7),
        "mbti": "ENTP / ESTP",
        "image": "01_해외영업.png",
        "catchphrase": "글로벌 시장의 빗장을 열고 대륙을 넘나드는 무역의 프론티어",
        "report": "시차와 문화가 다른 글로벌 바이어 앞에서도 주눅 들지 않고 능동적으로 대화를 이끄는 강한 추진력을 지니셨습니다. 예상치 못한 계약 변수나 클레임 상황에서도 유연한 순발력과 기민한 대처로 돌파구를 찾아내는 데 최적화된 성향입니다.",
        "strengths": ["대외 교섭력과 사교성", "위기 상황에서의 순발력", "도전적인 목표 달성 의지"],
        "search_kw": "해외영업"
    },
    "무역사무 및 영업관리": {
        "vector": (-0.7, -0.9, -0.2, 0.9),
        "mbti": "ISTJ / ISFJ",
        "image": "02_무역사무_영업관리.png",
        "catchphrase": "인코텀즈와 무역 서류의 정밀한 통제로 무결점 수출입을 보장하는 컨트롤 타워",
        "report": "B/L, C/I, P/L 등 방대하고 복잡한 선적 서류의 철자 하나, 수치 하나도 놓치지 않는 정밀함과 높은 책임감을 갖추셨습니다. 정해진 내규와 프로세스를 묵묵하고 정확하게 완수하여 무역 리스크를 사전에 예방하는 핵심 앵커 역할을 수행합니다.",
        "strengths": ["무결점 서류 작성 및 검증", "데이터 꼼꼼함과 체계성", "높은 업무 안정감"],
        "search_kw": "무역사무 영업관리"
    },
    "포워딩 및 국제물류/SCM": {
        "vector": (0.5, -0.3, -0.8, 0.8),
        "mbti": "ESTJ / ENTJ",
        "image": "03_포워딩_국제물류_SCM.png",
        "catchphrase": "대양과 하늘의 공급망을 실시간으로 지휘하는 글로벌 물류의 사령관",
        "report": "선박 지연, 항만 적체, 반품 등 꼬리를 무는 돌발 이슈 속에서도 냉철하게 우선순위를 정하고 리드하는 결단력을 갖추셨습니다. 복잡한 글로벌 공급망(SCM)을 한눈에 파악하고 스케줄을 철저하게 통제·관리하는 실행력이 돋보입니다.",
        "strengths": ["신속한 이슈 해결 능력", "강력한 일정 및 공정 통제력", "파트너 조율 및 주도력"],
        "search_kw": "포워딩 SCM 국제물류"
    },
    "해외소싱 및 바이어": {
        "vector": (-0.5, 0.2, -0.9, 0.4),
        "mbti": "INTJ / ISTP",
        "image": "04_해외소싱_바이어.png",
        "catchphrase": "철저한 원가 분석과 날카로운 네고로 최상의 가치를 발굴하는 전략 헌터",
        "report": "제조사와의 단가 협상에서 감정에 휘둘리지 않고 철저히 객관적인 원가 구조와 시장 데이터를 바탕으로 실리를 챙기는 분석가형입니다. 잠재적 공급망 리스크를 사전에 내다보고 장기적 관점에서 안정적인 소싱 전략을 구축합니다.",
        "strengths": ["데이터 기반 원가 분석", "냉철한 손익 계산 및 네고", "글로벌 공급망 리스크 예측"],
        "search_kw": "해외소싱 바이어"
    },
    "글로벌 마케팅": {
        "vector": (0.8, 0.9, 0.6, -0.3),
        "mbti": "ENFP / ENFJ",
        "image": "05_글로벌마케팅_e커머스.png",
        "catchphrase": "국경을 넘어 전 세계 소비자의 감성을 사로잡는 글로벌 브랜드 빌더",
        "report": "진출 국가 타깃 고객의 소비 심리와 문화적 코드를 빠르게 포착하여 매력적인 스토리로 제품을 브랜딩하는 감각을 지니셨습니다. 급변하는 e커머스 트렌드에 기민하게 반응하며 유연하고 창의적인 프로모션을 설계합니다.",
        "strengths": ["글로벌 트렌드 센싱", "문화적 공감대와 스토리텔링", "창의적인 캠페인 기획력"],
        "search_kw": "글로벌마케팅 해외마케팅"
    },
    "통관 및 무역 컴플라이언스": {
        "vector": (-0.8, -0.7, -0.9, 0.7),
        "mbti": "ISTJ / INTP",
        "image": "06_통관_무역컴플라이언스.png",
        "catchphrase": "복잡한 관세법과 무역 규범을 철통 방어하는 무역 질서의 수호자",
        "report": "HS 품목분류, FTA 원산지 규정, 국가별 관세 법규를 깊이 파고들어 구조적인 논리로 해석해 내는 능력이 탁월합니다. 법적 오차나 규정 위반을 철저히 차단하는 엄격한 원칙 준수 마인드로 회사의 통관 안정성을 수호합니다.",
        "strengths": ["정밀한 무역 법규 분석", "원칙 기반의 논리적 사고", "리스크 컴플라이언스 통제"],
        "search_kw": "수출입통관 관세 컴플라이언스"
    }
}

# --- 2. 20개 진단 문항 리스트 ---
QUESTIONS = [
    # [E/I 성향 축]
    {"q": "Q1. 신규 바이어 발굴을 위해 대형 무역 박람회에 참석했다. 나는?", "axis": "E_I", "opts": [("먼저 다가가 명함을 건네고 적극적으로 말을 건다", 1), ("우리 부스에 찾아오는 사람들을 위주로 친절하게 응대한다", -1)]},
    {"q": "Q2. 업무 중 한 번도 본 적 없는 무역 용어가 나왔을 때 나는?", "axis": "E_I", "opts": [("주변 동료나 사수에게 바로 물어보며 대화로 파악한다", 1), ("혼자서 구글링이나 무역 실무 매뉴얼을 찾아본다", -1)]},
    {"q": "Q3. 해외 거래처에서 갑자기 회사로 방문하겠다고 연락이 왔다. 나는?", "axis": "E_I", "opts": [("새로운 사람들과의 직접적인 미팅이 기대되고 에너지가 생긴다", 1), ("비대면으로 처리할 수 있는 일인데 대면 미팅을 해야 해서 피곤하다", -1)]},
    {"q": "Q4. 팀 회의에서 새로운 분기별 소싱 전략을 논의할 때 나는?", "axis": "E_I", "opts": [("내 의견을 적극적으로 말하며 회의 흐름을 주도한다", 1), ("다른 사람들의 의견을 경청하고 조용히 내용을 정리한다", -1)]},
    {"q": "Q5. 거래처와의 갈등이 발생했을 때 선호하는 해결 방식은?", "axis": "E_I", "opts": [("직접 전화를 걸어 대화로 빠르게 오해를 푼다", 1), ("이메일로 상황을 조목조목 정리하여 신중하게 회신한다", -1)]},
    
    # [N/S 성향 축]
    {"q": "Q6. 새로운 무역 자동화 시스템을 도입한다고 할 때 나는?", "axis": "N_S", "opts": [("새로운 시스템이 가져올 혁신적인 변화와 효율성이 기대된다", 1), ("기존 방식이 이미 익숙하고 정확한데 굳이 바꿔야 하나 싶다", -1)]},
    {"q": "Q7. 복잡한 선적 서류(B/L)와 인보이스를 검토할 때 나는?", "axis": "N_S", "opts": [("전체적인 무역 흐름상 내용이 논리적으로 맞는지 큰 그림을 본다", 1), ("품명, 수량, 오탈자, 숫자 하나까지 세세하게 대조하고 확인한다", -1)]},
    {"q": "Q8. 신제품 글로벌 마케팅 기획안을 작성할 때 나는?", "axis": "N_S", "opts": [("트렌드에 맞는 새롭고 독창적인 브랜딩 아이디어를 중시한다", 1), ("과거의 성공 데이터와 현실적인 예산 분배를 중시한다", -1)]},
    {"q": "Q9. 업무 매뉴얼을 처음 읽게 되었을 때 나는?", "axis": "N_S", "opts": [("전체적인 챕터 흐름과 핵심 목표 위주로 빠르게 훑어 파악한다", 1), ("1페이지부터 순서대로, 절차와 세부 지침을 꼼꼼히 읽어본다", -1)]},
    {"q": "Q10. 바이어의 컴플레인을 처리할 때 나는?", "axis": "N_S", "opts": [("현재 상황에 맞춰 직관적이고 새로운 타협점을 찾아 제시한다", 1), ("과거 비슷한 클레임 사례를 찾아 회사 규정과 절차대로 처리한다", -1)]},

    # [F/T 성향 축]
    {"q": "Q11. 중요한 계약을 앞두고 바이어가 감정적으로 무리한 요구를 할 때 나는?", "axis": "F_T", "opts": [("향후 우호적인 파트너십을 고려해 적절히 양보하며 타협점을 찾는다", 1), ("회사의 이익과 내규를 객관적으로 따져보고 단호하게 거절한다", -1)]},
    {"q": "Q12. 동료가 '이번 통관 프로젝트 서류 준비하느라 너무 힘들었어'라고 할 때 나는?", "axis": "F_T", "opts": [("'진짜 고생 많았어. 커피라도 한잔하면서 쉬자!' (공감 우선)", 1), ("'어떤 서류가 제일 문제였어? 내가 검토 도와줄까?' (해결 우선)", -1)]},
    {"q": "Q13. 신입 사원의 치명적인 B/L 오타 실수를 발견했을 때 나는?", "axis": "F_T", "opts": [("신입이 상처받지 않게 상황을 부드럽게 돌려서 조심스럽게 알려준다", 1), ("실수한 부분을 명확히 지적하고 향후 재발 방지 대책을 묻는다", -1)]},
    {"q": "Q14. 공급처가 원자재 가격 상승을 이유로 단가 인상을 통보했을 때 나는?", "axis": "F_T", "opts": [("그들의 어려운 상황을 이해하며 어느 정도 인상안을 수용해 준다", 1), ("시장 데이터와 원가 구조를 분석하여 인상률이 합당한지 따진다", -1)]},
    {"q": "Q15. 상사에게 인사 평가를 받을 때 내가 더 원하는 것은?", "axis": "F_T", "opts": [("팀 분위기에 헌신하고 열심히 노력한 '과정'을 인정받고 싶다", 1), ("정확한 데이터와 영업 실적이라는 '결과'로 평가받고 싶다", -1)]},

    # [J/P 성향 축]
    {"q": "Q16. 수많은 매장의 반품 등록 리스트를 엑셀로 비교·감사(Audit)할 때 나는?", "axis": "J_P", "opts": [("시트별로 데이터를 나누고, 함수를 써서 체계적이고 완벽하게 정리한다", 1), ("일단 눈에 띄는 누락이나 오류부터 직관적으로 찾아내며 유연하게 수정한다", -1)]},
    {"q": "Q17. 일주일 동안의 무역 스케줄과 업무 계획을 세울 때 나는?", "axis": "J_P", "opts": [("요일별, 시간 단위로 상세하게 To-Do 리스트를 세팅한다", 1), ("큼직한 마감일만 정해두고 매일 상황에 맞게 유동적으로 일한다", -1)]},
    {"q": "Q18. 갑작스러운 선박 지연으로 한 달짜리 물류 스케줄이 꼬였을 때 나는?", "axis": "J_P", "opts": [("즉시 새로운 플랜 B를 짜서 모든 스케줄을 다시 완벽하게 세팅해야 안심된다", 1), ("당황하지 않고 진행 상황을 지켜보며 그때그때 융통성 있게 대처한다", -1)]},
    {"q": "Q19. 회사 컴퓨터 바탕화면이나 이메일 수신함 상태는?", "axis": "J_P", "opts": [("폴더별, 날짜별로 각이 잡혀서 깔끔하게 분류되어 있다", 1), ("나만의 규칙은 있지만 남들이 보기엔 여기저기 흩어져 있는 편이다", -1)]},
    {"q": "Q20. 퇴근 30분 전, 거래처에서 갑자기 긴급 요청이 들어왔다. 나는?", "axis": "J_P", "opts": [("원래 오늘 계획했던 일을 다 마친 후, 내일 아침 1순위로 처리한다", 1), ("오늘 세워둔 계획을 유연하게 미루고 당장 급한 불부터 끄고 본다", -1)]}
]

def calculate_distance(user_vector, job_vector):
    dist = math.sqrt(sum((u - j) ** 2 for u, j in zip(user_vector, job_vector)))
    max_dist = 4.0
    fit_percentage = round((1 - (dist / max_dist)) * 100)
    return fit_percentage

# --- 3. 세션 상태 초기화 ---
if "current_step" not in st.session_state:
    st.session_state.current_step = "intro"
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(QUESTIONS)

# ==========================================
# 화면 1: 인트로 화면
# ==========================================
if st.session_state.current_step == "intro":
    st.markdown("<h1 style='text-align: center; color: #1e293b; margin-top: 20px;'>🚢 무역 실무 직무 적합도 테스트</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 16px; margin-bottom: 35px;'>20개의 실무 질문을 풀고 나의 성향과 딱 맞는 무역 커리어를 발견해보세요.</p>", unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
    with col_s2:
        if st.button("🚀 테스트 시작하기", use_container_width=True, type="primary"):
            st.session_state.current_step = 0
            st.session_state.answers = [None] * len(QUESTIONS)
            st.rerun()

# ==========================================
# 화면 2: 질문 카드 화면 (1문항씩 카드 형태 넘기기)
# ==========================================
elif isinstance(st.session_state.current_step, int):
    step = st.session_state.current_step
    q_data = QUESTIONS[step]

    # 상단 진행 상태
    progress_val = (step + 1) / len(QUESTIONS)
    st.progress(progress_val)
    st.markdown(f"<p style='text-align: right; color: #64748b; font-size: 13px; font-weight: 600; margin-top: 5px;'>문항 {step + 1} / {len(QUESTIONS)}</p>", unsafe_allow_html=True)

    # 질문 카드 UI
    st.markdown(
        f"""
        <div style='background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 18px; padding: 32px 24px; margin: 10px 0 25px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.03);'>
            <h3 style='color: #1e293b; margin: 0; font-size: 19px; line-height: 1.55; text-align: center;'>{q_data['q']}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    opt1_text, opt1_val = q_data['opts'][0]
    opt2_text, opt2_val = q_data['opts'][1]

    if st.button(f"A. {opt1_text}", key=f"btn_opt1_{step}", use_container_width=True):
        st.session_state.answers[step] = opt1_val
        if step + 1 < len(QUESTIONS):
            st.session_state.current_step += 1
        else:
            st.session_state.current_step = "result"
        st.rerun()

    st.write("")
    if st.button(f"B. {opt2_text}", key=f"btn_opt2_{step}", use_container_width=True):
        st.session_state.answers[step] = opt2_val
        if step + 1 < len(QUESTIONS):
            st.session_state.current_step += 1
        else:
            st.session_state.current_step = "result"
        st.rerun()

    if step > 0:
        st.write("")
        if st.button("⬅ 이전 질문으로 돌아가기"):
            st.session_state.current_step -= 1
            st.rerun()

# ==========================================
# 화면 3: 최종 결과 화면 (요청하신 박스 톤 적용)
# ==========================================
elif st.session_state.current_step == "result":
    # 4개 성향 축 점수 계산
    scores = {"E_I": 0, "N_S": 0, "F_T": 0, "J_P": 0}
    for i, q_data in enumerate(QUESTIONS):
        val = st.session_state.answers[i] if st.session_state.answers[i] is not None else 0
        scores[q_data['axis']] += val

    user_mbti = ""
    user_mbti += "E" if scores["E_I"] >= 0 else "I"
    user_mbti += "N" if scores["N_S"] >= 0 else "S"
    user_mbti += "F" if scores["F_T"] >= 0 else "T"
    user_mbti += "J" if scores["J_P"] >= 0 else "P"

    u_vector = (scores["E_I"] / 5, scores["N_S"] / 5, scores["F_T"] / 5, scores["J_P"] / 5)

    results = []
    for job_name, data in JOBS.items():
        fit_score = calculate_distance(u_vector, data["vector"])
        results.append({
            "job": job_name, 
            "score": fit_score, 
            "mbti": data["mbti"], 
            "image": data["image"],
            "catchphrase": data["catchphrase"],
            "report": data["report"],
            "strengths": data["strengths"],
            "search_kw": data["search_kw"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    best_job = results[0]
    worst_job = results[-1]

    # 폭죽 효과
    st.balloons()
    components.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.2/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 150,
                spread: 90,
                origin: { y: 0.6 }
            });
        </script>
        """,
        height=0
    )

    # 1. 캐릭터 이미지 출력
    img_path = os.path.join(BASE_DIR, best_job["image"])
    if os.path.exists(img_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(img_path, use_container_width=True)
    else:
        st.warning(f"이미지 파일을 찾을 수 없습니다: {best_job['image']}")

    # 2. 요청하신 스타일의 'BEST CAREER MATCH' 다크 네이비 그라데이션 박스
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1b1c57 0%, #151642 100%);
            border-radius: 24px;
            padding: 38px 25px;
            text-align: center;
            box-shadow: 0 14px 35px rgba(21, 22, 66, 0.28);
            margin: 15px 0 25px 0;
        ">
            <div style="
                color: #5c8df6;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 2.5px;
                margin-bottom: 12px;
            ">BEST CAREER MATCH</div>
            <div style="
                font-size: 32px;
                font-weight: 800;
                background: linear-gradient(90deg, #c7d2fe 0%, #e879f9 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 12px;
                letter-spacing: -0.5px;
            ">{best_job['job']}</div>
            <div style="
                color: #ffffff;
                font-size: 15px;
                font-weight: 500;
                line-height: 1.5;
                opacity: 0.95;
                margin-bottom: 18px;
            ">"{best_job['catchphrase']}"</div>
            <div style="
                display: inline-block;
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.16);
                border-radius: 20px;
                padding: 6px 18px;
                color: #cbd5e1;
                font-size: 13.5px;
                margin-bottom: 8px;
            ">
                직무 대표 MBTI: <strong style="color: #fff;">{best_job['mbti']}</strong> &nbsp;|&nbsp; 매칭 적합도: <strong style="color: #67e8f9;">{best_job['score']}%</strong>
            </div>
            <hr style="border: none; border-top: 1px solid rgba(255, 255, 255, 0.12); margin: 18px 0 12px 0;">
            <p style="color: #94a3b8; font-size: 12.5px; margin: 0;">
                ⚠️ 성향상 가장 거리가 먼 직업: <span style="color: #cbd5e1; font-weight: 600;">{worst_job['job']}</span> ({worst_job['mbti']} · 적합도 {worst_job['score']}%)
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 3. 성향 분석 리포트 & 설문자 MBTI 카드
    st.markdown("### 📊 설문자 성향 분석 리포트")
    st.markdown(
        f"""
        <div style='background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);'>
            <p style='font-size: 17px; margin-bottom: 12px;'>
                🎯 <strong>설문자 분석 MBTI:</strong> <span style='color: #2563EB; font-weight: bold;'>{user_mbti}</span>
            </p>
            <p style='color: #334155; line-height: 1.7; margin-bottom: 15px;'>
                {best_job['report']}
            </p>
            <p style='margin-bottom: 8px; font-weight: bold; color: #1E293B;'>💡 주요 핵심 강점 키워드</p>
            <ul style='color: #475569; margin: 0; padding-left: 20px;'>
                {''.join([f"<li style='margin-bottom: 4px;'>{s}</li>" for s in best_job['strengths']])}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4. 실시간 채용 공고 링크
    encoded_kw = urllib.parse.quote(best_job["search_kw"])
    saramin_url = f"https://www.saramin.co.kr/zf_user/search?searchword={encoded_kw}"
    jobkorea_url = f"https://www.jobkorea.co.kr/Search/?stext={encoded_kw}"
    wanted_url = f"https://www.wanted.co.kr/search?query={encoded_kw}"

    st.markdown(f"### 🔍 '{best_job['job']}' 실시간 채용 공고")
    st.caption("클릭 시 주요 채용 플랫폼의 최신 공고 검색 페이지로 바로 연결됩니다.")
    
    col_link1, col_link2, col_link3 = st.columns(3)
    with col_link1:
        st.link_button("사람인 공고 보기", saramin_url, use_container_width=True)
    with col_link2:
        st.link_button("잡코리아 공고 보기", jobkorea_url, use_container_width=True)
    with col_link3:
        st.link_button("원티드 공고 보기", wanted_url, use_container_width=True)

    # 5. 다시 하기 버튼
    st.write("")
    st.write("")
    if st.button("🔄 테스트 다시 하기", use_container_width=True):
        st.session_state.current_step = "intro"
        st.session_state.answers = [None] * len(QUESTIONS)
        st.rerun()