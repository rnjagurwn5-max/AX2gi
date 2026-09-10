#로또 V1
#로또 V2
#SDFSADFSADFAS

import streamlit as st
import random 
from datetime import datetime

st.title("🎱로또 번호 자동 생성기")
st.caption("버튼을 누르면 1~45 사이의 중복 없는 번호 6개짜리 세트를 5개 만들어줍니다.")

def lotto_one_set() -> list:
    """1~45 에서 중복 없이 번호 6개 뽑아 정렬된 리스트로 반환"""
    number: set[int] = set()
    while len(number) < 6: 
        number.add(random.randint(1, 45))  # 1 이상 45 이하 정수 하나 뽑기
    return sorted(number)

st.markdown("---") 

# 버튼을 눌렀을 때만 실행되도록 if문 적용
if st.button("5세트 번호 생성하기"):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"생성 시각: **{now_str}**")

    # 번호 순서별 적용할 Streamlit 내장 색상 (빨, 주, 초, 파, 보, 무지개)
    colors = ["red", "orange", "green", "blue", "violet", "rainbow"]

    for set_index in range(1, 6):
        lotto_num = lotto_one_set()
        
        # 각 숫자에 색상 태그 적용 (예: :red[7], :orange[12], ...)
        colored_nums = [f":{colors[i]}[**{num}**]" for i, num in enumerate(lotto_num)]
        
        # 기존 형식 그대로 리스트 모양으로 출력
        st.write(f"{set_index}세트 : [{', '.join(colored_nums)}]")

