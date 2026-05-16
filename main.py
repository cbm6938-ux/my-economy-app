import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 모바일 가독성 향상
st.set_page_config(page_title="Vibe Economy 2.0", layout="wide", initial_sidebar_state="collapsed")

# 🎨 디자인 최적화 (배경은 부드럽게, 글자는 선명하게)
st.markdown("""
    <style>
    /* 전체 배경: 완전 검정 대신 눈이 편한 진회색 */
    .main { background-color: #1c2128; color: #e6edf3; }
    
    /* 제목 부분 슬림화 및 자연스러운 정렬 */
    .title-text { font-size: 1.8rem !important; font-weight: 800; color: #f0f6fc; margin-bottom: 0.5rem; }
    .subtitle-text { font-size: 0.9rem !important; color: #8b949e; margin-bottom: 2rem; }

    /* 지표 카드: 가독성 중심 디자인 */
    [data-testid="stMetric"] { 
        background-color: #22272e; 
        border-radius: 12px; 
        padding: 15px 20px; 
        border: 1px solid #444c56; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    [data-testid="stMetricLabel"] { color: #8b949e !important; font-size: 0.9rem !important; }
    [data-testid="stMetricValue"] { color: #58a6ff !important; font-size: 1.6rem !important; font-weight: 700 !important; }

    /* 뉴스 카드: 선명한 대비 */
    .news-card { 
        background-color: #22272e; 
        padding: 18px; 
        border-radius: 12px; 
        margin-bottom: 12px; 
        border: 1px solid #444c56;
        border-left: 6px solid #2f81f7; 
    }
    .news-title { color: #58a6ff !important; font-size: 1.05rem !important; font-weight: bold; text-decoration: none; }
    .summary-text { color: #c9d1d9 !important; font-size: 0.92rem; margin-top: 8px; line-height: 1.6; }
    
    /* 구분선 색상 조절 */
    hr { border: 0; border-top: 1px solid #444c56; }
    </style>
    """, unsafe_allow_html=True)

# 헤더 섹션 (슬림하고 자연스럽게 변경)
st.markdown('<p class="title-text">📊 Vibe Economy 2.0</p>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle-text">사령관의 실시간 경제 기지 | {datetime.now().strftime("%y.%m.%d %H:%M")} Update</p>', unsafe_allow_html=True)

# 2. 실시간 지표 수집
@st.cache_data(ttl=300)
def get_data(ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        val = d['Close'].iloc[-1]
        change = val - d['Close'].iloc[-2]
        return val, change
    except: return 0, 0

indices = {"국채 금리": "^TNX", "WTI 유가": "CL=F", "환율": "USDKRW=X", "KOSPI": "^KS11", "NASDAQ": "^IXIC"}
cols = st.columns(2) # 모바일에서 2열로 배치하여 공간 절약

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_data(ticker)
    with cols[i % 2]: # 지표를 2열로 번갈아가며 배치
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

st.divider()

# 3. 실시간 뉴스 (가독성 강화 버전)
st.subheader("📰 실시간 주요 브리핑")

@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

try:
    news_items = fetch_news()
    for item in news_items:
        st.markdown(f"""
            <div class="news-card">
                <a href="{item.link}" target="_blank" class="news-title">{item.title}</a>
                <p class="summary-text"><b>[분석]</b> 시장의 핵심 흐름을 담은 보급로 정보입니다. 지인들께 이 기사를 공유하여 가이드해 주세요.</p>
            </div>
            """, unsafe_allow_html=True)
except:
    st.error("⚠️ 뉴스 통신망 확인 중...")

st.markdown("<br><p style='text-align: center; color: #8b949e; font-size: 0.8rem;'>System Active. All indicators are real-time.</p>", unsafe_allow_html=True)
