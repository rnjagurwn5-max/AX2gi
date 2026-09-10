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

# 1. 현재 파일(exchange.py) 기준 상위 폴더의 상위 폴더(.env 위치)를 정확히 지정
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '..', '.env') # 만약 .env가 AX2gi 폴더에 있다면 이 경로 확인
load_dotenv(dotenv_path)

# 혹은 .env 파일을 아예 exchange.py와 같은 폴더(API TEST)에 넣었다면 아래처럼 수정:
# load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")