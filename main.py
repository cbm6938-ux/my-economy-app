import streamlit as st
import yfinance as yf
import feedparser
import re
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [시인성 긴급 복구] 지수 글씨 강화 + 초록색 정밀 보정
st.markdown("""
    <style>
    /* 배경색 고정 */
    .stApp { background-color: #f8fafc !important; }
    
    /* 상단 헤더: 남색 배경에 흰색 글자 고정 */
    .header-box {
        background-color: #1e3a8a !important;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
    }
    .header-box h2 { color: #ffffff !important; font-weight: 800 !important; margin: 0 !important; }
    .header-box p { color: #cbd5e1 !important; font-size: 0.9rem !important; }

    /* 지표 카드: 숫자가 안 보이던 문제 해결 (진한 검정색 강제) */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    label[data-testid="stMetricLabel"] { color: #475569 !important; font-weight: 700 !important; }
    
    /* ❗ 지수 숫자(4.59 등)를 가장 진한 남색으로 고정 */
    div[data-testid="stMetricValue"] { 
        color: #0f172a !important; 
        font-weight: 850 !important; 
        font-size: 2rem !important; 
    }

    /* 🟢 [사령관 지시] 초록색(상승)만 진하고 쨍하게 보정 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #047857 !important; /* 짙은 에메랄드 */
        font-weight: 800 !important;
        background: #ecfdf5 !important;
        padding: 2px 10px !important;
        border-radius: 6px !important;
    }

    /* 🔴 빨간색(하락)은 시스템 기본값으로 건드리지 않음 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Down"]) {
        background: transparent !important;
    }

    /* 섹션 제목 선명하게 */
    .section-header {
        color: #1e293b !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        border-bottom: 4px solid #1e3a8a;
        padding-bottom: 5px;
        margin: 35px 0 20px 0;
        display: inline-block;
    }

    /* 뉴스 카드 디자인 */
    .news-card {
        background-color: #ffffff !important;
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #e2e8f0 !important;
        border-left: 8px solid #1e3a8a !important;
    }
    .news-link { color: #1e3a8a !important; font-weight: 800 !important; font-size: 1.15rem !important; text-decoration: none !important; display: block; margin-bottom: 8px; }
    .summary-text { color: #334155 !important; font-size: 0.95rem !important; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- 헤더 ---
st.markdown(f"""
    <div class="header-box">
        <h2>🚀 Vibe Economy Dashboard</h2>
        <p>사령관의 실시간 경제 지휘소 | {datetime.now().strftime("%Y.%m.%d %H:%M")} Live</p>
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

# --- 뉴스 섹션 ---
st.markdown('<p class="section-header">📰 오늘의 실시간 요약</p>', unsafe_allow_html=True)

# 4. 고성능 뉴스 요약 엔진 (제목 중복 제거)
@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

def get_pure_summary(item):
    title = item.title
    # 원문 요약에서 HTML 제거
    raw_desc = item.get('summary', '') or item.get('description', '')
    clean_desc = re.sub('<[^<]+?>', '', raw_desc)
    
    # ❗ [핵심 로직] 요약문에서 제목과 겹치는 부분을 도려냄
    # 보통 구글 뉴스는 요약 앞에 제목이 붙어서 오기 때문에 이를 제거합니다.
    pure_text = clean_desc.replace(title, "").strip()
    
    # 만약 다 지워서 너무 짧아지면 원문의 뒷부분이라도 노출
    if len(pure_text) < 10:
        pure_text = "본문 기사에서 상세한 시장 분석과 전문가 의견을 확인하실 수 있습니다."
    
    return pure_text[:140] + "..." if len(pure_text) > 140 else pure_text

try:
    news_items = fetch_news()
    for item in news_items:
        summary = get_pure_summary(item)
        st.markdown(f"""
            <div class="news-card">
                <a href="{item.link}" target="_blank" class="news-link">{item.title}</a>
                <p class="summary-text">🚩 <b>요약:</b> {summary}</p>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v3.5 | Anti-Blur & Pure Summary Mode</p>", unsafe_allow_html=True)
