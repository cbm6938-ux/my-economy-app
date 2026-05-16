import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 모바일 최적화
st.set_page_config(page_title="Vibe Economy 2.1", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [긴급 조정] 가독성 및 상단 디자인 마감
st.markdown("""
    <style>
    /* 1. 전체 배경: 눈이 편하면서도 선명한 딥 그레이 */
    .main { background-color: #0d1117; color: #c9d1d9; }
    
    /* 2. 상단 여백 확보 (잘림 방지) */
    .block-container { padding-top: 2.5rem !important; padding-bottom: 0rem !important; }
    
    /* 3. 제목 섹션: 선명한 화이트 및 슬림 디자인 */
    .app-header {
        background: linear-gradient(90deg, #1f6feb, #111);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-bottom: 1px solid #30363d;
    }
    .main-title { color: #ffffff !important; font-size: 1.5rem !important; font-weight: 800; margin: 0; }
    .sub-title { color: #8b949e !important; font-size: 0.8rem !important; }

    /* 4. 지표 카드: 고대비 및 입체감 적용 */
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    label[data-testid="stMetricLabel"] { color: #f0f6fc !important; font-size: 0.95rem !important; font-weight: 600 !important; }
    div[data-testid="stMetricValue"] { color: #58a6ff !important; font-size: 1.8rem !important; font-weight: 800 !important; }
    
    /* 5. 뉴스 카드 디자인 강화 */
    .news-card {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
        border: 1px solid #30363d;
        border-left: 5px solid #58a6ff;
    }
    .news-link { color: #f0f6fc !important; font-size: 1rem !important; font-weight: 700; text-decoration: none; line-height: 1.4; }
    .news-summary { color: #8b949e !important; font-size: 0.85rem; margin-top: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 섹션 (부자연스러움 해결) ---
st.markdown(f"""
    <div class="app-header">
        <p class="main-title">🚀 Vibe Economy 2.1</p>
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

# 3. 실시간 지표 (2열 배치로 시원하게)
indices = {"국채 금리": "^TNX", "WTI 유가": "CL=F", "원/달러 환율": "USDKRW=X", "코스피": "^KS11", "나스닥": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_eco_data(ticker)
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

st.divider()

# 4. 실시간 뉴스 자동 업데이트
st.subheader("📰 실시간 경제 속보")
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
                <p class="news-summary">🚩 <b>사령관 분석:</b> 시장 흐름의 핵심입니다. 제목을 클릭해 원문을 확인하세요.</p>
            </div>
            """, unsafe_allow_html=True)
except:
    st.write("데이터 복구 중...")

st.markdown("<p style='text-align: center; color: #30363d; font-size: 0.8rem; margin-top: 2rem;'>COMMANDER SYSTEM V2.1 ACTIVE</p>", unsafe_allow_html=True)
