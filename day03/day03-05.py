#인코딩 자동 감지 + 한글 폰트 막대 그래프
#여러 인코딩("utf-8-sig","cp949","euc-kr") 
#내가 쓸 폰트 같은 경로에 있어야 함
#객실등급별 생존율 막대그래프 생성 후 그림을 저장 chart.png
#실행은 streamlit run day03-05.py 

import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib import font_manager, rc

file_path = os.path.join(os.path.dirname(__file__), "titanic_cleaned.csv")

# 1. 여러 인코딩을 순차적으로 시도하는 함수
def read_csv_with_auto_encoding(file_path, **kwargs):
    encodings = ["utf-8-sig", "cp949", "euc-kr"]
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding, **kwargs)
            return df
        except UnicodeDecodeError:
            pass
        except Exception as e:
            st.warning(f"'{encoding}' 시도 중 에러 발생: {e}")
            pass
    raise ValueError(f"파일을 읽을 수 없습니다. 시도한 인코딩: {encodings}")

#인코딩 자동 감지로 Csv 읽기
st.subheader("1)인코딩 자동 감지") 
df = read_csv_with_auto_encoding(file_path)

#객실등급(pclass)별 생존율 집계 
#사망 0/ 생존1 등급별 평균 Survived
#생존 등급별 평균을 내면 
#그대로가 등급의 생존 비율이 된다.
#10명 남3 여자7
#1000 생존 300 300/1000 30%

pclass_survival_rate = df.groupby("Pclass")["Survived"].mean().sort_index() 
st.dataframe(( pclass_survival_rate*100 ).round(1).rename("생존율(%)")  )

# df_df = st.dataframe(( pclass_survival_rate*100 ).round(1).rename("생존율(%)")  )
# st.write(df_df) 

# 차트 그리기

st.markdown("---")

st.subheader("3) 객실등급별 생존율 막대그래프")
font_path='PlayfairDisplay-Regular.ttf'

try : 
    #폰트 파일이 없으면 'FileNotFoundError'가 발생.
    font_prop = font_manager.FontProperties(fname=font_path)
    # matplotlib font_manager에 폰트를 등록하고, 전역 폰트로 설정.
    font_manager.fontManager.addfont(font_path)
    plt.rcParams["font.family"] = font_prop.get_name()
    st.write("PlayfairDisplay-Regular.ttf 폰트를 적용했습니다")
except FileNotFoundError:
    st.warning("폰트파일을 찾을 수 없습니다.")

fig, ax = plt.subplots(figsize = (8,5))
(pclass_survival_rate*100).plot(kind="bar", color="blue", ax=ax)
ax.set_title("Surviving rate by Pclass")
ax.set_xlabel("Pclass")
ax.set_ylabel("Surviving rate(%)")

st.pyplot(fig)

output_path = os.path.join(os.path.dirname(__file__),"chart.png")
fig.savefig(output_png)

