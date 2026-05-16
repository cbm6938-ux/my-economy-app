import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 테마 강제 고정
st.set_page_config(page_title="Vibe Economy Fixed", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [시스템 다크모드 방어용] 고정형 고대비 스타일링
st.markdown("""
    <style>
    /* 1. 시스템 설정 무시하고 배경색 강제 고정 (연한 그레이) */
    .stApp {
        background-color: #f1f3f5 !important;
    }
    
    /* 2. 모든 글자색을 짙은 차콜로 강제 고정 (가시성 핵심) */
    h1, h2, h3, p, span, div, label {
        color: #212529 !important;
    }

    /* 3. 상단 헤더: 짙은 네이비 (시스템 색상 무시) */
    .header-box {
        background-color: #1e3a8a !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-box h2, .header-box p {
        color: #ffffff !important; /* 헤더 안의 글자만 화이트로 고정 */
    }

    /* 4. 지표 카드: 완전 화이트 배경에 진한 테두리 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }
    /* 지표 숫자 색상 (상승/하락 색상 유지하되 대비 강화) */
    [data-testid="stMetricValue"] {
        color: #0d6efd !important; /* 기본 값은 블루 */
    }

    /* 5. 뉴스 카드: 선명한 대비 레이아웃 */
    .news-card {
        background-color: #ffffff !important;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #ced4da !important;
        border-left: 6px solid #1e3a8a !important;
    }
    .news-card a {
        color: #1e3a8a !important;
        font-weight: 800 !important;
        text-decoration: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown(f"""
    <div class="header-box">
        <h2>📊 Vibe Economy Pro (Fixed)</h2>
        <p>시스템 설정을 무시하고 가시성을 최우선으로 설계된 함대입니다. | {datetime.now().strftime("%H:%M")} Live</p>
    </div>
    """, unsafe_allow_html=True)

# 2. 데이터 수집
@st.cache_data(ttl=300)
def get_eco(ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        val = d['Close'].iloc[-1]
        diff = val - d['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

# 3. 실시간 지표 (2열 배치)
indices = {"🇺🇸 국채 10년": "^TNX", "🛢️ WTI 유가": "CL=F", "💵 환율(USD)": "USDKRW=X", "🇰🇷 KOSPI": "^KS11", "🇺🇸 NASDAQ": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_eco(ticker)
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

st.divider()

# 4. 실시간 뉴스
st.subheader("📰 오늘의 실시간 브리핑")

@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

try:
    news_items = fetch_news()
    for item in news_items:
        st.markdown(f"""
            <div class="news-card">
                <a href="{item.link}" target="_blank">{item.title}</a>
                <p style="margin-top:8px; font-size:0.9rem; color:#495057 !important;">
                    🚩 <b>사령관 분석:</b> 시장 흐름의 핵심 기사입니다. 지표와 함께 체크하세요.
                </p>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#adb5bd; font-size:0.8rem;'>System-Proof Version v3.1</p>", unsafe_allow_html=True)
