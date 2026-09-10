# supply chain shipment type

import io 
import pandas as pd
import streamlit as st

st.title("🚢 Supply Chain 데이터 기초 탐색")
st.caption("pandas의 head/tail/shape/info/columns로 공급망 배송 데이터셋 기본 정보를 확인합니다.") 

# Supply Chain 데이터 가져오기
CSV_PATH = "Suppy_Chain_Shipment_Data.csv"

# 파일 업로더
uploaded_file = st.file_uploader("Suppy_Chain_Shipment_Data.csv 파일을 직접 업로드 할 수 있습니다(선택사항)", type="csv")

if uploaded_file is not None:
    # uploade_file 오타 수정, upload_file 변수명 통일
    df = pd.read_csv(uploaded_file)
else:
    try: 
        # 이 스크립트와 같은 폴더에 있는 파일을 읽어옵니다.
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError: 
        # 파일이 없을 때 사용자 안내
        st.error(f"❌ '{CSV_PATH}' 파일을 찾을 수가 없습니다.")
        st.info("같은 경로에 파일을 업로드하거나 csv파일을 폴더에 넣고 새로고침 하세요.")
        df = None

if df is not None:
    st.subheader("1) head(): 데이터의 앞부분 5개 행 미리보기")  # heade 오타 수정 및 설명 수정
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("2) tail(): 데이터의 뒷부분 5개 행 미리보기")
    st.dataframe(df.tail(), use_container_width=True)

    st.subheader("3) shape(): 행 개수, 열 개수")  # spape 오타 수정
    col1, col2 = st.columns(2)
    with col1:
        st.metric("행 개수", f"{df.shape[0]:,}개")  # 천 단위 콤마 추가

    with col2:
        st.metric("열 개수", f"{df.shape[1]}개")

    st.subheader("4) columns : 전체 열(컬럼) 이름 목록")
    st.write(list(df.columns))

    st.subheader("5) info(): 각 열의 자료형과 결측치(NaN) 여부 요약")
    # df.info는 값을 리턴하지 않고 화면에 직접 출력만 해주는 함수라서
    # io.StringIO()라는 "메모리 위에 가짜 파일"에 결과를 받아낸 뒤 그 내용을 text로 보여준다. 
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())