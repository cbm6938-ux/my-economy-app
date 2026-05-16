import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 테마 강제 고정
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [채도 폭발 조치] 상승(녹색) 지표를 전용 뱃지 스타일로 변경
st.markdown("""
    <style>
    /* 배경색 고정 */
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
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    label[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 800 !important; font-size: 1.1rem !important; }
    
    /* 지수 숫자: 완전한 검정색 강화 */
    div[data-testid="stMetricValue"] { 
        color: #000000 !important; 
        font-weight: 900 !important; 
        font-size: 2.2rem !important; 
    }

    /* 🟢 [사령관 지시] 녹색(상승) 수치: 채도 100% 네온 그린 뱃지 적용 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #ffffff !important;           /* 글씨는 흰색으로 반전 */
        background-color: #16a34a !important; /* 채도 높은 선명한 녹색 (Vivid Green) */
        font-weight: 900 !important;
        padding: 5px 14px !important;
        border-radius: 10px !important;
        font-size: 1.25rem !important;
        box-shadow: 0 4px 8px rgba(22, 163, 74, 0.4); /* 녹색 광원 효과 추가 */
        display: inline-flex !important;
        align-items: center;
    }

    /* 🔴 빨간색(하락) 수치: 기본 스타일 유지하여 녹색을 더 돋보이게 함 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Down"]) {
        background-color: transparent !important;
        color: #dc2626 !important;
        font-weight: 600 !important;
    }

    /* 섹터 뉴스 스타일 */
    .section-header {
        color: #000000 !important;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        border-left: 10px solid #0c1c4f;
        padding-left: 15px;
        margin: 40px 0 20px 0;
    }

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
st.markdown('<div class="header-box"><h2>🚀 Vibe Economy Dashboard</h2></div>', unsafe_allow_html=True)

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

# 4. 섹터 분류 엔진
def classify_sector(title):
    sectors = {
        "반도체": ["반도체", "삼성전자", "SK하이닉스", "엔비디아", "칩", "ASML"],
        "건설/부동산": ["건설", "부동산", "아파트", "주택", "재건축"],
        "조선/해운": ["조선", "선박", "해운", "LNG선", "벌크선"],
        "우주/항공": ["우주", "항공", "위성", "발사", "국방"],
        "자동차/배터리": ["자동차", "전기차", "배터리", "현대차", "기아", "테슬라"],
        "AI/빅테크": ["AI", "인공지능", "구글", "애플", "마이크로소프트", "메타"],
        "에너지/금속": ["유가", "에너지", "구리", "철강", "원자력"],
        "금융/정책": ["금리", "은행", "금융", "연준", "환율", "세금"]
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

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v3.9 | Vivid Green Aura Mode</p>", unsafe_allow_html=True)
