import streamlit as st
import yfinance as yf
import feedparser
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

# 1. 페이지 설정 및 가독성 최적화
st.set_page_config(page_title="Vibe Economy 4.0", layout="wide", initial_sidebar_state="collapsed")

# 🎨 UI 디자인 (미드나잇 블루 & 가독성 강화 테마)
st.markdown("""
    <style>
    .main { background-color: #1a202c; color: #f7fafc; }
    .header-container { padding: 1.5rem 0; border-bottom: 2px solid #4a5568; margin-bottom: 2rem; text-align: center; }
    .title-text { font-size: 2.2rem !important; font-weight: 800; color: #63b3ed; margin: 0; }
    
    /* 지표 카드 디자인 */
    [data-testid="stMetric"] { 
        background-color: #2d3748; 
        border-radius: 15px; padding: 20px; border: 1px solid #4a5568;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    
    /* 뉴스 및 1줄 요약 박스 */
    .news-card { 
        background-color: #2d3748; padding: 20px; border-radius: 15px; 
        margin-bottom: 15px; border: 1px solid #4a5568; border-left: 8px solid #4299e1; 
    }
    .summary-box { 
        background-color: #1a202c; padding: 12px; border-radius: 8px; 
        margin-top: 10px; border: 1px solid #4a5568;
    }
    .summary-text { color: #63b3ed !important; font-size: 1rem; font-weight: 500; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# 헤더 섹션
st.markdown('<div class="header-container"><p class="title-text">📊 Vibe Economy 4.0</p></div>', unsafe_allow_html=True)

# 2. 데이터 수집 및 분석 함수
@st.cache_data(ttl=300)
def get_fleet_data(ticker, period="7d"):
    try:
        data = yf.Ticker(ticker).history(period=period)
        val = data['Close'].iloc[-1]
        change = val - data['Close'].iloc[-2]
        pct = (change / data['Close'].iloc[-2]) * 100
        return val, change, pct, data['Close']
    except: return 0, 0, 0, pd.Series()

# 🌡️ 시장 온도계 (Gauge Chart) 제작 함수
def draw_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "시장 온도 (Vibe Index)", 'font': {'size': 20, 'color': "#f7fafc"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#4a5568"},
            'bar': {'color': "#63b3ed"},
            'bgcolor': "#1a202c",
            'borderwidth': 2,
            'bordercolor': "#4a5568",
            'steps': [
                {'range': [0, 30], 'color': '#68d391'}, # 공포(기회)
                {'range': [30, 70], 'color': '#cbd5e0'}, # 중립
                {'range': [70, 100], 'color': '#fc8181'}  # 탐욕(주의)
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      font={'color': "#f7fafc", 'family': "Arial"}, height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# 지표 리스트 정의
indices = {"미국채 금리(10Y)": "^TNX", "WTI 유가": "CL=F", "환율(USD/KRW)": "USDKRW=X", "KOSPI": "^KS11", "NASDAQ": "^IXIC"}

# 3. 메인 화면 구성
# [1단계] 시장 온도계 배치
score_total = 0
results = {}

for name, ticker in indices.items():
    val, change, pct, history = get_fleet_data(ticker)
    results[name] = (val, change, pct, history)
    # 온도계 로직: 주식 상승(+), 금리/환율/유가 하락(-) 시 점수 부여 (간단 모델)
    if name in ["KOSPI", "NASDAQ"]: score_total += (50 + pct*5)
    else: score_total += (50 - pct*5)

market_score = max(0, min(100, score_total / len(indices)))
st.plotly_chart(draw_gauge(market_score), use_container_width=True)

st.divider()

# [2단계] 지표 카드 + 7일 트렌드(Sparkline)
st.subheader("📈 핵심 지표 흐름 (7일 트렌드)")
cols = st.columns(2)

for i, (name, (val, change, pct, history)) in enumerate(results.items()):
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{change:+.2f} ({pct:+.2f}%)")
        # 스파크라인 차트 추가
        if not history.empty:
            st.line_chart(history, height=100, use_container_width=True)
        st.write("")

st.divider()

# [3단계] 실시간 뉴스 1줄 요약
st.subheader("📰 사령관의 실시간 1줄 브리핑")

@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

try:
    for item in fetch_news():
        # 첫 문장만 추출하여 요약 생성
        summary_line = item.summary.split('.')[0] + '.' if item.summary else "상세 내용을 확인하십시오."
        st.markdown(f"""
            <div class="news-card">
                <a href="{item.link}" target="_blank" style="color:#ebf8ff; font-size:1.1rem; font-weight:bold; text-decoration:none;">{item.title}</a>
                <div class="summary-box">
                    <p class="summary-text">🚩 <b>1줄 요약:</b> {summary_line}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
except:
    st.error("통신망 재설정 중...")

st.markdown(f"<p style='text-align: center; color: #a0aec0; margin-top: 30px;'>{datetime.now().strftime('%Y-%m-%d %H:%M')} 함대 정상 가동 중</p>", unsafe_allow_html=True)
