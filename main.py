import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 테마 고정
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [가독성 정밀 보정] 제목 시인성 확보 및 시스템 다크모드 방어
st.markdown("""
    <style>
    /* 1. 배경색 강제 고정 (시스템 설정 무시) */
    .stApp {
        background-color: #f1f3f5 !important;
    }
    
    /* 2. 상단 헤더: 남색 배경에 '흰색' 글자로 시인성 폭발 */
    .header-box {
        background-color: #1e3a8a !important; /* 남색 배경 */
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    /* 제목과 부제목을 반드시 흰색으로 강제 고정 */
    .header-box h2 {
        color: #ffffff !important; 
        font-weight: 800 !important;
        margin: 0 !important;
    }
    .header-box p {
        color: #cbd5e1 !important; 
        font-size: 0.9rem !important;
        margin-top: 8px !important;
    }

    /* 3. 지표 카드: 고대비 화이트 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }
    label[data-testid="stMetricLabel"] { color: #475569 !important; font-weight: 700 !important; }
    div[data-testid="stMetricValue"] { color: #2563eb !important; font-weight: 800 !important; }

    /* 4. 뉴스 카드: 사령관의 '요약' 섹션 */
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
        font-weight: 700 !important;
        text-decoration: none !important;
        font-size: 1.05rem !important;
    }
    .summary-box {
        margin-top: 10px;
        font-size: 0.9rem;
        color: #334155 !important;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 (제목 가인성 확보) ---
st.markdown(f"""
    <div class="header-box">
        <h2>🚀 Vibe Economy Dashboard</h2>
        <p>사령관의 실시간 경제 지표 브리핑 | {datetime.now().strftime("%Y.%m.%d %H:%M")} Live</p>
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

# 4. 실시간 뉴스 (분석 -> 요약으로 변경)
st.subheader("📰 오늘의 실시간 요약")

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
                <div class="summary-box">
                    🚩 <b>사령관 요약:</b> 현재 시장의 핵심 맥락을 담은 소식입니다. 
                    지표의 변화와 함께 원문 내용을 확인하여 흐름을 파악하십시오.
                </div>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("뉴스를 로딩 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v3.2 | Optimized Visibility</p>", unsafe_allow_html=True)
