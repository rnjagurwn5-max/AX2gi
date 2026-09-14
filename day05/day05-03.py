import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(page_title="기억하는 챗봇", page_icon="💬") 
st.title("💬 예제2) 기억하는 멀티턴 챗봇")
st.caption("대화 기록을 기억하고, 실시간으로 타이핑되는 스트리밍 챗봇입니다.")

# ----------------사이드바 설정(설정, 시스템 메시지, 초기화)------------------
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("OpenAI API Key", type="password", help="sk-로 시작하는 OpenAI API Key를 입력하세요.")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)
    
    st.divider()
    
    # 시스템 메시지 사용자 설정
    st.header("🧠 봇 역할 설정")
    system_prompt = st.text_area(
        "시스템 메시지", 
        value="너는 항상 '주인님'이라는 호칭으로 대화를 시작하는 매우 친절한 비서야.",
        help="AI의 성격이나 역할을 자유롭게 지정해보세요."
    )
    
    st.divider()
    
    # 대화 기록 초기화 버튼
    if st.button("🗑️ 대화 기록 초기화", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun() # 화면 새로고침

    st.markdown("[API 발급 받기](https://platform.openai.com/api-keys)") 

# ----------------세션 상태(Session State) 초기화------------------
# 대화 기록을 저장할 리스트를 세션 상태에 생성합니다. (새로고침 시 날아가지 않도록)
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------기존 대화 기록 출력------------------
# 저장된 메시지들을 화면에 순서대로 그려줍니다.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------메인 화면 (채팅 입력 및 API 호출)--------------------------
# st.chat_input을 사용하면 화면 하단에 고정된 채팅창이 생성됩니다.
if prompt := st.chat_input("질문을 입력하세요..."):
    if not api_key:
        st.error("좌측 사이드바에 OpenAI API Key를 입력하세요.")
    else:
        # 1) 사용자가 입력한 메시지를 화면에 띄우고 세션에 저장
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 2) AI 응답 생성 및 출력
        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=api_key)
                
                # API에 보낼 전체 메시지 구성 = (시스템 메시지) + (누적된 대화 기록)
                messages_for_api = [{"role": "system", "content": system_prompt}] + st.session_state.messages

                # 스트리밍 API 호출 (stream=True)
                stream = client.chat.completions.create(
                    model=model,
                    messages=messages_for_api,
                    stream=True  # 👈 실시간 타이핑 효과의 핵심
                )
                
                # st.write_stream은 스트리밍 데이터를 받아 실시간으로 화면에 그려주고, 최종 문자열을 반환합니다.
                response_content = st.write_stream(stream)
                
                # 3) 완성된 AI 답변을 세션 기록에 저장
                st.session_state.messages.append({"role": "assistant", "content": response_content})
                
            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {e}")