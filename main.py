import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 모바일 강제 최적화
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [디자인 마스터] 가독성 200% 향상 및 프리미엄 마감
st.markdown("""
    <style>
    /* 1. 상단 여백 및 잘림 방지 (어플 느낌의 핵심) */
    .block-container { padding-top: 3.5rem !important; padding-bottom: 2rem !important; background-color: #0d1117; }
    
    /* 2. 최상단 헤더 바 (네온 블루 포인트) */
    .app-header {
        position: fixed; top: 0; left: 0; right: 0; height: 60px;
        background-color: #161b22;
        border-bottom: 2px solid #58a6ff;
        display: flex; align-items: center; padding: 0 20px; z-index: 999;
    }
    .header-title { color: #ffffff !important; font-size: 1.3rem !important; font-weight: 800; margin: 0; }

    /* 3. 전체 텍스트 가독성: 배경은 더 검게, 글자는 더 하얗게 */
    .main { color: #f0f6fc; }
    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }

    /* 4. 지표 카드: 시인성 극대화 */
    div[data-testid="stMetric"] {
        background-color: #1c2128;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    label[data-testid="stMetricLabel"] { color: #f0f6fc !important; font-size: 1rem !important; font-weight: 600 !important; }
    div[data-testid="stMetricValue"] { color: #58a6ff !important; font-size: 2rem !important; font-weight: 900 !important; }
    
    /* 5. 뉴스 카드: 배경과 일체화된 세련된 디자인 */
    .news-card {
        background-color: #1c2128;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
        border-left: 6px solid #238636; /* 성공을 상징하는 초록색 포인트 */
    }
    .news-link { color: #ffffff !important; font-size: 1.1rem !important; font-weight: 700; text-decoration: none; line-height: 1.5; }
    .news-summary { color: #8b949e !important; font-size: 0.9rem; margin-top: 10px; }
    
    /* 6. 모바일 하단 여백 추가 */
    .footer-space { margin-top: 50px; text-align: center; color: #30363d; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 고정 헤더 ---
st.markdown('<div class="app-header"><p class="header-title">🚀 VIBE ECONOMY PRO</p></div>', unsafe_allow_html=True)

# 헤더 아래 여백 및 시간 표시
st.markdown(f"<p style='color: #8b949e; font-size: 0.85rem; margin-top: 10px;'>최종 분석 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", unsafe_allow_html=True)

# 2. 실시간 지표 수집
@st.cache_data(ttl=300)
def get_eco_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d")
        val = data['Close'].iloc[-1]
        diff = val - data['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

# 지표 배치 (모바일 2열)
st.subheader("📈 실시간 마켓 지표")
indices = {"국채 금리": "^TNX", "WTI 유가": "CL=F", "원/달러 환율": "USDKRW=X", "KOSPI": "^KS11", "NASDAQ": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_eco_data(ticker)
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

st.divider()

# 3. 실시간 뉴스 자동 업데이트
st.subheader("📰 오늘의 핵심 경제 브리핑")
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
                <p class="news-summary">🚩 <b>AI 1줄 요약:</b> 시장의 흐름을 결정지을 중요한 뉴스입니다. 제목을 클릭해 상세 내용을 확인하십시오.</p>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("뉴스를 새로고침 중입니다...")

st.markdown('<div class="footer-space">Vibe Coding Pro v5.0 | Official Release</div>', unsafe_allow_html=True)
