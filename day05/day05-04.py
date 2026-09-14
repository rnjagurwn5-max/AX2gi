import streamlit as st
from openai import OpenAI
import io

# ----------------새로 추가된 텍스트 추출 함수------------------
def extract_text(uploaded_file):
    """업로드된 파일의 확장자에 따라 텍스트를 추출하는 함수"""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        # 1. PDF 파일 처리
        if file_extension == 'pdf':
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
            return text
            
        # 2. Word(docx) 파일 처리
        elif file_extension == 'docx':
            import docx
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
            
        # 3. 그 외 일반 텍스트 파일 (txt, csv, md 등)
        else:
            return uploaded_file.getvalue().decode("utf-8")
            
    except Exception as e:
        return f"Error: {e}"

# ----------------페이지 기본 설정------------------
st.set_page_config(page_title="통합 문서 요약 앱", page_icon="📄") 
st.title("📄 통합 문서 요약 앱")
st.caption("TXT, PDF, DOCX(Word) 등 다양한 형식의 파일을 업로드하면 텍스트를 추출해 요약해 줍니다.")

# ----------------사이드바 설정------------------
with st.sidebar:
    st.header("⚙️ 기본 설정")
    api_key = st.text_input("OpenAI API Key", type="password", help="sk-로 시작하는 OpenAI API Key를 입력하세요.")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)
    
    st.divider()
    
    st.header("📝 요약 설정")
    summary_option = st.radio(
        "요약 옵션 (길이)", 
        ["3줄 핵심 요약", "짧은 단락 요약", "상세한 전체 요약"]
    )
    
    summary_style = st.selectbox(
        "요약 스타일", 
        ["개조식 (글머리 기호 사용)", "서술형 (자연스러운 줄글)", "전문적인 보고서 톤", "친절한 말투 (이모지 포함)"]
    )

    st.divider()
    st.markdown("[API 발급 받기](https://platform.openai.com/api-keys)") 

# ----------------메인 화면 (파일 업로드 및 요약)--------------------------

# type 속성을 지워서(또는 확장해서) 다양한 파일을 받을 수 있게 변경
uploaded_file = st.file_uploader(
    "요약할 문서를 업로드하세요. (지원: TXT, PDF, DOCX, CSV 등)", 
    type=["txt", "pdf", "docx", "csv", "md"]
)

if st.button("문서 요약하기", type="primary"):
    if not api_key:
        st.error("좌측 사이드바에 OpenAI API Key를 입력하세요.")
    elif not uploaded_file:
        st.error("요약할 파일을 먼저 업로드하세요.")
    else:
        # 1) 확장자에 맞춰 파일 내용 추출 (새로 만든 함수 사용)
        file_contents = extract_text(uploaded_file)
        
        # 파일 추출 중 에러가 발생했거나, 해독할 수 없는 파일인 경우
        if file_contents.startswith("Error:"):
            st.error(f"파일을 읽는 중 문제가 발생했습니다.\n{file_contents}")
            st.stop()
        elif not file_contents.strip():
            st.warning("파일에서 텍스트를 찾을 수 없습니다. (스캔된 이미지로만 이루어진 PDF일 수 있습니다.)")
            st.stop()

        # 2) 요약을 위한 프롬프트 구성
        prompt = f"""
다음 제공되는 문서 내용을 설정된 옵션에 맞게 요약해 주세요.

[설정 옵션]
- 요약 길이: {summary_option}
- 요약 스타일: {summary_style}

[문서 내용]
{file_contents}
"""

        st.subheader("💡 요약 결과")
        
        # 3) AI 응답 생성 및 스트리밍 출력
        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=api_key)
                
                stream = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "너는 제공된 문서를 사용자의 요구에 맞춰 정확하고 깔끔하게 요약하는 전문 요약가야."},
                        {"role": "user", "content": prompt}
                    ],
                    stream=True
                )
                
                st.write_stream(stream)
                
            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {e}") 

