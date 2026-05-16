import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 미드톤 테마 최적화
st.set_page_config(page_title="Vibe Economy Mid", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [색상 정밀 교정] 배경은 차분하게, 지표는 쨍하게!
st.markdown("""
    <style>
    /* 1. 전체 배경: 눈이 편한 미드톤 실버 그레이 */
    .main { background-color: #ebedef; color: #212529; }
    
    /* 2. 상단 헤더: 깊이감 있는 네이비 포인트 */
    .app-header {
        background: #1e3a8a;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-title { color: #ffffff !important; font-size: 1.6rem !important; font-weight: 800; margin: 0; }
    .sub-title { color: #bfdbfe !important; font-size: 0.85rem !important; margin-top: 5px; }

    /* 3. 지표 카드: 화이트 배경으로 고대비 실현 */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #cfd4da;
        border-radius: 12px;
        padding: 20px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* 지표 이름 글자색 */
    label[data-testid="stMetricLabel"] { color: #4b5563 !important; font-size: 0.95rem !important; font-weight: 700 !important; }
    
    /* 초록색/빨간색 지표 가시성 강제 강화 */
    [data-testid="stMetricDelta"] > div { font-weight: 800 !important; }
    [data-testid="stMetricDelta"] svg { filter: drop-shadow(0px 0px 1px rgba(0,0,0,0.2)); }

    /* 4. 뉴스 카드: 정돈된 리스트 바이브 */
    .news-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 12px;
        border: 1px solid #cfd4da;
        border-left: 6px solid #1e3a8a;
    }
    .news-link { color: #1e3a8a !important; font-size: 1.05rem !important; font-weight: 700; text-decoration: none; }
    .news-summary { color: #374151 !important; font-size: 0.9rem; margin-top: 8px; line-height: 1.5; }
    
    hr { border-top: 1px solid #cfd4da; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 섹션 ---
st.markdown(f"""
    <div class="app-header">
        <p class="main-title">📈 Vibe Economy Mid-tone</p>
        <p class="sub-title">사령관 전용 실시간 경제 브리핑 | {datetime.now().strftime("%Y.%m.%d %H:%M")}</p>
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

# 3. 실시간 지표 (2열 배치)
indices = {"국채 금리": "^TNX", "WTI 유가": "CL=F", "원/달러 환율": "USDKRW=X", "코스피": "^KS11", "나스닥": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_eco_data(ticker)
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

st.divider()

# 4. 실시간 뉴스
st.subheader("📰 오늘의 주요 브리핑")
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
                <p class="news-summary">🚩 <b>분석:</b> 시장의 흐름을 결정지을 핵심 보급로 정보입니다. 클릭하여 상세 내용을 확인하세요.</p>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("뉴스를 수신하는 중입니다...")

st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 0.8rem; margin-top: 3rem;'>Commander Terminal v2.2 | Optimized Visibility</p>", unsafe_allow_html=True)
