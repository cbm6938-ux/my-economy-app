import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 강제 고대비 테마
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [긴급 시인성 복구] 녹색 수치 폭발 + 지수 칠흑색 강화
st.markdown("""
    <style>
    /* 배경색 고정 (시스템 다크모드 방어) */
    .stApp { background-color: #f1f3f5 !important; }
    
    /* 상단 헤더: 남색 배경 + 순백색 제목 */
    .header-box {
        background-color: #0c1c4f !important;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 30px;
        text-align: center;
    }
    .header-box h2 { color: #ffffff !important; font-weight: 900 !important; margin: 0 !important; }

    /* 지표 카드 디자인 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 15px !important;
    }
    label[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 800 !important; font-size: 1.1rem !important; }
    
    /* ❗ 지수 숫자(4.59 등): 완전한 검정색으로 시인성 확보 */
    div[data-testid="stMetricValue"] { 
        color: #000000 !important; 
        font-weight: 900 !important; 
        font-size: 2.2rem !important; 
    }

    /* 🟢 [사령관 지시] 녹색(상승) 수치 가시성 "폭발" 보정 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #064e3b !important; /* 칠흑 같은 짙은 녹색 */
        background-color: #4ade80 !important; /* 형광 그린 배경 */
        font-weight: 900 !important;
        padding: 4px 12px !important;
        border-radius: 8px !important;
        font-size: 1.2rem !important;
        border: 1px solid #059669 !important;
    }

    /* 섹션 제목 */
    .section-header {
        color: #000000 !important;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        border-left: 10px solid #0c1c4f;
        padding-left: 15px;
        margin: 40px 0 20px 0;
    }

    /* 뉴스 카드 및 섹터 태그 */
    .news-card {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #cbd5e1 !important;
        display: flex;
        align-items: center;
    }
    .sector-tag {
        background-color: #0c1c4f;
        color: #ffffff !important;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 900;
        margin-right: 15px;
        white-space: nowrap;
    }
    .news-link { color: #000000 !important; font-weight: 800 !important; font-size: 1.1rem !important; text-decoration: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown(f"""
    <div class="header-box">
        <h2>🚀 Vibe Economy Dashboard</h2>
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

st.markdown('<p class="section-header">📰 섹터별 주요 소식</p>', unsafe_allow_html=True)

# 4. 섹터 분류 엔진 (요약 대신 태그 추출)
def classify_sector(title):
    sectors = {
        "반도체": ["반도체", "삼성전자", "SK하이닉스", "엔비디아", "칩", "TSMC"],
        "건설/부동산": ["건설", "부동산", "아파트", "주택", "재건축"],
        "조선/해운": ["조선", "선박", "해운", "LNG선", "HMM"],
        "우주/항공": ["우주", "항공", "위성", "발사", "방산"],
        "자동차/배터리": ["자동차", "전기차", "배터리", "현대차", "기아", "테슬라"],
        "AI/빅테크": ["AI", "인공지능", "구글", "애플", "마이크로소프트", "메타"],
        "에너지/금속": ["유가", "에너지", "구리", "철강", "리튬"],
        "금융/정책": ["금리", "은행", "금융", "연준", "환율", "정부"]
    }
    for sector, keywords in sectors.items():
        if any(kw in title for kw in keywords):
            return sector
    return "경제일반"

@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:7]

try:
    news_items = fetch_news()
    for item in news_items:
        sector = classify_sector(item.title)
        st.markdown(f"""
            <div class="news-card">
                <span class="sector-tag">{sector}</span>
                <a href="{item.link}" target="_blank" class="news-link">{item.title}</a>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v3.8 | Maximum Visibility Mode</p>", unsafe_allow_html=True)
