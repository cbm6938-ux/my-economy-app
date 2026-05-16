import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 (모바일 최적화 & 다크 테마 바이브)
st.set_page_config(page_title="Vibe Economy 2.0", layout="wide", initial_sidebar_state="collapsed")

# 🎨 사령관 전용 다크모드 커스텀 스타일링
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border-radius: 12px; padding: 15px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #58a6ff !important; }
    .news-card { background-color: #161b22; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #238636; }
    .summary-text { color: #8b949e; font-size: 0.95rem; margin-top: 8px; line-height: 1.5; }
    a { text-decoration: none !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Vibe Economy Dashboard 2.0")
st.markdown(f"**사령관님의 실시간 경제 기지** | {datetime.now().strftime('%Y-%m-%d %H:%M')} 업데이트")

# 2. 실시간 지표 (상단 가로 배치 - 모바일에서는 자동 줄바꿈)
def get_data(ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        val = d['Close'].iloc[-1]
        change = val - d['Close'].iloc[-2]
        return val, change
    except: return 0, 0

indices = {"국채 금리(10Y)": "^TNX", "WTI 유가": "CL=F", "환율(USD/KRW)": "USDKRW=X", "KOSPI": "^KS11", "NASDAQ": "^IXIC"}
cols = st.columns(len(indices))

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_data(ticker)
    cols[i].metric(name, f"{val:,.2f}", f"{diff:+.2f}")

st.divider()

# 3. 실시간 뉴스 자동 수집 (구글 RSS 기반)
st.subheader("📰 지금 이 시각 주요 뉴스 (사령관의 1줄 브리핑)")

@st.cache_data(ttl=600) # 10분마다 뉴스 갱신
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

try:
    news_items = fetch_news()
    for item in news_items:
        with st.container():
            st.markdown(f"""
                <div class="news-card">
                    <a href="{item.link}" target="_blank" style="color:#58a6ff; font-size:1.15rem; font-weight:bold;">{item.title}</a>
                    <p class="summary-text">🚩 <b>사령관 요약:</b> 시장의 흐름을 결정지을 핵심 보급로 정보입니다. 지인들께도 이 흐름을 공유하세요.</p>
                </div>
                """, unsafe_allow_html=True)
except:
    st.error("⚠️ 뉴스 통신망에 일시적인 장애가 발생했습니다.")

st.success("✅ 모든 시스템이 사령관님의 지휘 하에 실시간 가동 중입니다.")
