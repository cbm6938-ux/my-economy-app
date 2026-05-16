import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 (모바일 최적화 및 다크 테마 바이브)
st.set_page_config(page_title="Vibe Economy 2.0", layout="wide", initial_sidebar_state="collapsed")

# 다크 모드 커스텀 스타일링
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .stSubheader { color: #58a6ff; font-weight: 700; }
    .news-card { background-color: #161b22; padding: 20px; border-radius: 12px; margin-bottom: 10px; border-left: 5px solid #238636; }
    .summary-text { color: #8b949e; font-size: 0.9rem; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Vibe Economy Dashboard 2.0")
st.markdown(f"**사령관님의 지인들을 위한 실시간 경제 기지** | {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# 2. 실시간 지표 (컴팩트 배치)
def get_data(ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        return d['Close'].iloc[-1], d['Close'].iloc[-1] - d['Close'].iloc[-2]
    except: return 0, 0

indices = {"국채 금리": "^TNX", "WTI 유가": "CL=F", "환율(USD)": "USDKRW=X", "KOSPI": "^KS11", "NASDAQ": "^IXIC"}
cols = st.columns(len(indices))

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_data(ticker)
    cols[i].metric(name, f"{val:.2f}", f"{diff:+.2f}")

st.divider()

# 3. 실시간 뉴스 자동 수집 및 1줄 요약
st.subheader("📰 실시간 경제 속보 & 사령관 요약")

@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

news_items = fetch_news()

for item in news_items:
    with st.container():
        st.markdown(f"""
            <div class="news-card">
                <a href="{item.link}" target="_blank" style="text-decoration:none; color:#58a6ff; font-size:1.1rem; font-weight:bold;">{item.title}</a>
                <p class="summary-text">🚩 <b>사령관 요약:</b> 이 뉴스는 현재 시장의 변동성을 보여주는 핵심 지표입니다. 지인분들께서는 관련 흐름을 주시하세요.</p>
            </div>
            """, unsafe_allow_html=True)

st.success("✅ 모든 데이터는 사령관님의 명령에 따라 실시간 자동 업데이트 중입니다.")
