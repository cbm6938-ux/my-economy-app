import streamlit as st
import yfinance as yf
import feedparser
import pandas as pd
from datetime import datetime

# 1. 페이지 및 테마 설정
st.set_page_config(page_title="Vibe Economy 3.5", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [소프트 다크 & 가독성 최적화]
st.markdown("""
    <style>
    /* 배경: 너무 까맣지 않은 세련된 다크 그레이 */
    .main { background-color: #0d1117; color: #c9d1d9; }
    
    /* 헤더 슬림화 */
    .block-container { padding-top: 1.5rem !important; }
    
    /* 지표 카드 디자인 */
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px !important;
    }

    /* 상태 표시 배지 디자인 */
    .status-badge {
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-left: 5px;
    }
    .high { background-color: #f85149; color: white; }
    .stable { background-color: #238636; color: white; }
    .low { background-color: #1f6feb; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 분석 엔진 (1년치 기준)
@st.cache_data(ttl=3600)
def get_analysis_data(ticker):
    try:
        # 1년치 데이터 수집
        data = yf.Ticker(ticker).history(period="1y")
        if data.empty: return None
        
        curr = data['Close'].iloc[-1]
        prev = data['Close'].iloc[-2]
        high_1y = data['Close'].max()
        low_1y = data['Close'].min()
        
        # 상태 판정 로직 (1년 범위 내 위치 기준)
        range_1y = high_1y - low_1y
        position = (curr - low_1y) / range_1y
        
        if position > 0.8: status = ("높음", "high")
        elif position < 0.2: status = ("낮음", "low")
        else: status = ("안정", "stable")
        
        # 차트용 데이터 정리 (이름 제거)
        chart_df = data[['Close']].copy()
        chart_df.index.name = None
        chart_df.columns = [None]
        
        return {"curr": curr, "diff": curr-prev, "status": status, "chart": chart_df}
    except: return None

# 헤더
st.markdown(f"### 📊 Vibe Economy 3.5")
st.caption(f"사령관의 지능형 경제 기지 | {datetime.now().strftime('%Y-%m-%d %H:%M')} 실시간 분석")

# 3. 메인 지표 & 1년 차트 레이아웃
indices = {"국채 금리": "^TNX", "WTI 유가": "CL=F", "환율": "USDKRW=X", "코스피": "^KS11", "나스닥": "^IXIC"}

for name, ticker in indices.items():
    res = get_analysis_data(ticker)
    if res:
        # 지표와 상태 표시
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric(name, f"{res['curr']:,.2f}", f"{res['diff']:+.2f}")
            st.markdown(f"현재 상태: <span class='status-badge {res['status'][1]}'>{res['status'][0]}</span>", unsafe_allow_html=True)
        
        with col2:
            # 1년치 Area 차트 (Y축 자동 줌)
            st.area_chart(res['chart'], height=120, use_container_width=True)
    st.divider()

# 4. 뉴스 브리핑 (기존 유지)
st.subheader("📰 실시간 경제 브리핑")
@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

for item in fetch_news():
    st.markdown(f"""
        <div style="background-color: #161b22; padding: 12px; border-radius: 10px; border-left: 4px solid #58a6ff; margin-bottom: 8px;">
            <a href="{item.link}" target="_blank" style="color:#58a6ff; font-weight:bold; text-decoration:none; font-size:0.9rem;">{item.title}</a>
        </div>
        """, unsafe_allow_html=True)
