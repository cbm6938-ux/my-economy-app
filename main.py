import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 라이트 모드 최적화
st.set_page_config(page_title="Vibe Economy Light", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [라이트 테마 조치] 깨끗하고 선명한 화이트 & 그레이 바이브
st.markdown("""
    <style>
    /* 1. 전체 배경: 깨끗한 연그레이/화이트 */
    .main { background-color: #f8f9fa; color: #1a1a1a; }
    
    /* 2. 상단 여백 및 헤더 디자인 */
    .block-container { padding-top: 2rem !important; }
    .app-header {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    .main-title { color: #212529 !important; font-size: 1.6rem !important; font-weight: 800; margin: 0; }
    .sub-title { color: #6c757d !important; font-size: 0.85rem !important; margin-top: 5px; }

    /* 3. 지표 카드: 화이트 배경에 소프트 쉐도우 */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 15px;
        padding: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    label[data-testid="stMetricLabel"] { color: #495057 !important; font-size: 1rem !important; font-weight: 600 !important; }
    div[data-testid="stMetricValue"] { color: #0d6efd !important; font-size: 1.8rem !important; font-weight: 800 !important; }
    
    /* 4. 뉴스 카드: 가독성 중심의 깔끔한 카드 */
    .news-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #dee2e6;
        border-left: 6px solid #0d6efd;
    }
    .news-link { color: #212529 !important; font-size: 1.1rem !important; font-weight: 700; text-decoration: none; }
    .news-summary { color: #495057 !important; font-size: 0.9rem; margin-top: 10px; line-height: 1.5; }
    
    /* 구분선 */
    hr { border-top: 1px solid #dee2e6; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 섹션 ---
st.markdown(f"""
    <div class="app-header">
        <p class="main-title">📈 Vibe Economy Light</p>
        <p class="sub-title">사령관님의 실시간 경제 브리핑 | {datetime.now().strftime("%Y.%m.%d %H:%M")} 기준</p>
    </div>
    """, unsafe_allow_html=True)

# 2. 지표 수집 함수
@st.cache_data(ttl=300)
def get_eco_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d")
        val = data['Close'].iloc[-1]
        diff = val - data['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

# 3. 실시간 지표 (깔끔한 2열 배치)
indices = {"국채 금리": "^TNX", "WTI 유가": "CL=F", "원/달러 환율": "USDKRW=X", "코스피": "^KS11", "나스닥": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_eco_data(ticker)
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

st.divider()

# 4. 실시간 뉴스 (라이트 모드 가독성 강화)
st.subheader("📰 오늘의 주요 경제 뉴스")
@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

try:
    news_items = fetch_news()
    for item in news_items:
        st.markdown(f"""
            <div class="news-card">
                <a href="{item.link}" target="_blank" class="news-link">{item.title}</a>
                <p class="news-summary">🚩 <b>분석:</b> 지인분들이 꼭 챙겨봐야 할 핵심 뉴스입니다. 클릭하여 상세 내용을 확인하세요.</p>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("실시간 뉴스를 수신 중입니다...")

st.markdown("<p style='text-align: center; color: #adb5bd; font-size: 0.85rem; margin-top: 3rem;'>Copyright © 2024 Commander Vibe. All Rights Reserved.</p>", unsafe_allow_html=True)
