import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정: 어플 같은 느낌을 주는 레이아웃
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [디자인 마감] 전문가용 대시보드 스타일링
st.markdown("""
    <style>
    /* 배경: 깨끗하고 고급스러운 화이트 그레이 */
    .main { background-color: #f0f2f6; }
    
    /* 헤더: 신뢰감을 주는 네이비 바 */
    .header-container {
        background-color: #1e3a8a;
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 지표 카드: 고대비 및 가시성 극대화 */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 20px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* 초록색(상승) 글자색을 더 짙게 보정하여 가독성 확보 */
    [data-testid="stMetricDelta"] > div { font-weight: 700 !important; color: #059669 !important; }

    /* 뉴스 카드: 깔끔한 블로그 스타일 */
    .news-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #1e3a8a;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .news-link { color: #1e3a8a !important; font-size: 1.1rem !important; font-weight: 700; text-decoration: none; }
    .news-summary { color: #4b5563 !important; font-size: 0.95rem; margin-top: 10px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown(f"""
    <div class="header-container">
        <h2 style="margin:0;">📊 Vibe Economy Pro</h2>
        <p style="margin:5px 0 0 0; opacity:0.8; font-size:0.9rem;">
            지인들을 위한 실시간 경제 지표 브리핑 | {datetime.now().strftime("%Y-%m-%d %H:%M")}
        </p>
    </div>
    """, unsafe_allow_html=True)

# 2. 데이터 수집 (캐싱 적용)
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

# 4. 자동 뉴스 브리핑 (제목 클릭 시 이동)
st.subheader("📰 오늘의 핵심 경제 뉴스")

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
                <p class="news-summary">
                    🚩 <b>사령관의 요약:</b> 현재 시장의 흐름을 보여주는 중요한 소식입니다. 
                    지인분들께서는 위 지표의 변화와 함께 이 기사의 원문을 참고하시기 바랍니다.
                </p>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("데이터 로딩 중...")

st.markdown("<br><p style='text-align:center; color:#9ca3af;'>Commander Terminal v3.0 | Protected by Vibe Coding</p>", unsafe_allow_html=True)
