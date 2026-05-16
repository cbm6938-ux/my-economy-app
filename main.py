import streamlit as st
import yfinance as yf
import feedparser
import re
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [가독성 최종 정밀 보정] 초록색 강화 및 헤더 선명도 업그레이드
st.markdown("""
    <style>
    /* 배경색 고정 */
    .stApp { background-color: #f1f3f5 !important; }
    
    /* 상단 헤더 섹션 */
    .header-box {
        background-color: #1e3a8a !important;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
    }
    .header-box h2 { color: #ffffff !important; font-weight: 800 !important; margin: 0 !important; }
    .header-box p { color: #cbd5e1 !important; font-size: 0.9rem !important; margin-top: 8px !important; }

    /* 지표 카드 가독성 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 16px !important;
    }
    label[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 700 !important; font-size: 1rem !important; }
    div[data-testid="stMetricValue"] { color: #1e40af !important; font-weight: 800 !important; }

    /* 🟢 초록색(상승) 지표 진하게 보정 */
    [data-testid="stMetricDelta"] > div { 
        color: #065f46 !important; /* 더 짙은 에메랄드 그린 */
        font-weight: 900 !important; 
        background: rgba(6, 95, 70, 0.1); /* 약간의 배경색으로 대비 증가 */
        padding: 2px 8px;
        border-radius: 5px;
    }

    /* 🔴 빨간색(하락) 지표도 함께 보정 */
    [data-testid="stMetricDelta"] > div[data-direction="down"] {
        color: #991b1b !important; /* 더 짙은 레드 */
    }

    /* 흐릿했던 하단 섹션 제목 선명하게 */
    .section-header {
        color: #0f172a !important; /* 아주 진한 네이비 */
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin-top: 30px !important;
        margin-bottom: 15px !important;
        border-bottom: 3px solid #1e3a8a;
        display: inline-block;
        padding-bottom: 5px;
    }

    /* 뉴스 카드 및 요약 텍스트 */
    .news-card {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #ced4da !important;
        border-left: 8px solid #1e3a8a !important;
    }
    .news-card a { color: #1e3a8a !important; font-weight: 800 !important; font-size: 1.1rem !important; text-decoration: none !important; }
    .summary-text { color: #475569 !important; font-size: 0.95rem !important; margin-top: 10px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown(f"""
    <div class="header-box">
        <h2>🚀 Vibe Economy Dashboard</h2>
        <p>실시간 경제 지표 브리핑 | {datetime.now().strftime("%Y.%m.%d %H:%M")} Live</p>
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

# --- 하단 섹션 제목 (선명도 강화) ---
st.markdown('<p class="section-header">📰 오늘의 실시간 요약</p>', unsafe_allow_html=True)

# 4. 실시간 뉴스 & 실제 내용 요약 엔진
@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

def clean_html(text):
    return re.sub('<[^<]+?>', '', text) # HTML 태그 제거

try:
    news_items = fetch_news()
    for item in news_items:
        # 뉴스 내용(description/summary)에서 실제 텍스트 추출 및 요약
        raw_summary = item.get('summary', item.get('description', '내용 요약 정보가 없습니다.'))
        clean_text = clean_html(raw_summary)
        # 너무 길면 자르고 1줄 요약 바이브로 변경
        short_summary = clean_text[:120] + "..." if len(clean_text) > 120 else clean_text
        
        st.markdown(f"""
            <div class="news-card">
                <a href="{item.link}" target="_blank">{item.title}</a>
                <p class="summary-text">🚩 <b>실시간 요약:</b> {short_summary}</p>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v3.3 | Final Visibility Tuning</p>", unsafe_allow_html=True)
