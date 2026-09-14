import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="무엇이든 물어보자기", page_icon="✋✋") 
st.title("✋예제1) 무엇이든 물어보자기") # 오타 수정(물엇이든 -> 무엇이든)
st.caption("질문 하나 입력하면 OpenAI chat completions API 한번 호출, 답변을 받아오는 가장 단순한 방법")

# ----------------사이드바 API 모델------------------
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("OpenAI API Key", type="password", help="sk-로 시작하는 OpenAI API Key를 입력하세요.")
    # 존재하지 않는 모델명 수정 (gpt-4.1-mini -> gpt-3.5-turbo)
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)
    st.markdown("[API 발급 받기](https://platform.openai.com/api-keys)") 

#---------------메인 화면--------------------------
# 오타 수정: question - st.text_input -> question = st.text_input
question = st.text_input("질문을 입력하세요", placeholder="예) 오늘 날씨가 어떤가요?")

if st.button("질문하기",type="primary"):
    if not api_key:
        st.error("OpenAI API Key를 입력하세요.")
    elif not question:
        st.error("질문을 입력하세요.")
    else:
        client = OpenAI(api_key=api_key)
        
        # 1) 답변을 생각하는 중.. (로딩 스피너 적용)
        with st.spinner("답변을 생각하는 중.."):
            try:
                # 2) API 호출
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        # '주인님'으로 시작하는 친절한 답변가 프롬프트 적용
                        {"role": "system", "content": "너는 항상 '주인님'이라는 호칭으로 대화를 시작하는 매우 친절한 비서야."},
                        {"role": "user", "content": question}
                    ]
                )
                
                answer = response.choices[0].message.content
                usage = response.usage
                
                # 답변 출력
                st.success(answer)
                
                # 3) 사용한 토큰 수 표시
                st.info(f"""
                💡 **사용한 토큰 수 안내**
                - 입력(Prompt) 토큰: {usage.prompt_tokens}
                - 출력(Completion) 토큰: {usage.completion_tokens}
                - **총(Total) 토큰 수: {usage.total_tokens}**
                """)
                
            # 4) 오류가 있으면 메시지 출력
            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {e}")