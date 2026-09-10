import streamlit as st

# 페이지 설정
st.set_page_config(page_title="간단한 계산기", page_icon="🧮")

st.title("🧮 초간단 계산기")
st.caption("두 숫자와 연산자를 선택하여 간단하게 계산 결과를 확인하세요.")

st.markdown("---")

# 입력 필드 구성을 위한 레이아웃 분할
col1, col2, col3 = st.columns([3, 2, 3])

with col1:
    num1 = st.number_input("첫 번째 숫자 (Num 1)", value=0.0, step=1.0, format="%f")

with col2:
    operator = st.selectbox("연산자", ["+", "-", "×", "÷"])

with col3:
    num2 = st.number_input("두 번째 숫자 (Num 2)", value=0.0, step=1.0, format="%f")

# 세션 상태(session_state)를 이용한 계산 기록 저장
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("<br>", unsafe_allow_html=True)

# 계산 실행 버튼
if st.button("계산하기", use_container_width=True):
    result = None
    error_msg = None
    
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "×":
        result = num1 * num2
    elif operator == "÷":
        if num2 == 0:
            error_msg = "❌ 0으로 나눌 수 없습니다."
        else:
            result = num1 / num2

    if error_msg:
        st.error(error_msg)
    else:
        # 결과를 깔끔하게 포맷팅 (소수점 아래가 없으면 정수로 표시)
        num1_str = int(num1) if num1.is_integer() else num1
        num2_str = int(num2) if num2.is_integer() else num2
        result_str = int(result) if result.is_integer() else round(result, 6)
        
        calc_formula = f"{num1_str} {operator} {num2_str} = {result_str}"
        
        # 계산 결과 출력
        st.success(f"계산 완료!")
        st.metric(label="결과값 (Result)", value=str(result_str))
        
        # 계산 기록에 추가 (가장 최신 것이 위로 가도록 insert 0)
        st.session_state.history.insert(0, calc_formula)

# 계산 기록 리스트 보여주기
st.markdown("---")
st.subheader("📜 최근 계산 기록")

if st.session_state.history:
    for record in st.session_state.history[:5]:  # 최근 5개까지 출력
        st.write(f"- {record}")
    
    if st.button("기록 초기화"):
        st.session_state.history = []
        st.rerun()
else:
    st.caption("아직 계산 기록이 없습니다.")
