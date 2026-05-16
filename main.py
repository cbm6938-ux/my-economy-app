import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 미드톤 테마 최적화
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [최종 시각화 조치] 눈이 편한 배경 & 녹색 수치 폭발적 가시성
st.markdown("""
    <style>
    /* 1. 전체 배경: 눈이 편한 샌드 그레이 미드톤 */
    .stApp { background-color: #ebedef !important; color: #212529; }
    
    /* 2. 상단 헤더: 깊이감 있는 딥 네이비 포인트 */
    .header-box {
        background-color: #0c1c4f;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        text-align: center;
    }
    .main-title { color: #ffffff !important; font-size: 1.8rem !important; font-weight: 800; margin: 0; }
    .update-time { color: #bfdbfe !important; font-size: 0.9rem !important; margin-top: 5px; }

    /* 3. 지표 카드: 고대비 화이트 배경 */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 2px solid #dee2e6;
        border-radius: 12px;
        padding: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* 지표 레이블 글자색 */
    label[data-testid="stMetricLabel"] { color: #495057 !important; font-size: 1rem !important; font-weight: 600 !important; }
    
    /* 🟢 [사령관 지시] 상승(녹색) 지표 시인성 폭발적 강화 */
    [data-testid="stMetricDelta"] > div { 
        color: #064e3b !important; /* 칠흑처럼 짙은 에메랄드 */
        font-weight: 900 !important; 
        background: #d1fae5; /* 옅은 민트색 배경 */
        padding: 3px 10px;
        border-radius: 6px;
    }

    /* 🔴 하락(빨간색) 지표도 가시성 확보 */
    [data-testid="stMetricDelta"] > div[data-direction="down"] {
        color: #991b1b !important; /* 진한 레드 */
        background: #fee2e2; /* 옅은 핑크색 배경 */
    }

    /* 4. 뉴스 섹션: 전문 대시보드 바이브 */
    .section-header {
        color: #0f172a !important; /* 아주 진한 네이비 */
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        margin-top: 40px !important;
        margin-bottom: 20px !important;
        border-left: 8px solid #00E5FF;
        padding-left: 15px;
        display: inline-block;
    }
    .news-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 8px solid #1e3a8a;
    }
    .sector-tag {
        background-color: #f1f5f9;
        color: #1e3a8a;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 12px;
    }
    .news-link { color: #212529 !important; font-weight: 700 !important; font-size: 1.05rem !important; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown(f"""
    <div class="header-box">
        <p class="main-title">📊 Vibe Economy Pro 3.7</p>
        <p class="update-time">사령관님의 실시간 종목별 뉴스 기지 | {datetime.now().strftime("%Y.%m.%d %H:%M")} Live</p>
    </div>
    """, unsafe_allow_html=True)

# 2. 데이터 수집 함수
@st.cache_data(ttl=300)
def get_eco_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d")
        val = data['Close'].iloc[-1]
        diff = val - data['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

# 3. 실시간 지표 (깔끔한 2열 배치)
indices = {"🇺🇸 국채 10년": "^TNX", "🛢️ WTI 유가": "CL=F", "💵 환율(USD)": "USDKRW=X", "🇰🇷 KOSPI": "^KS11", "🇺🇸 NASDAQ": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_eco_data(ticker)
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

st.divider()

# 4. 섹터 분류 엔진 & 뉴스
st.markdown('<p class="section-header">📰 주요 섹터별 실시간 뉴스</p>', unsafe_allow_html=True)

def classify_sector(title):
    sectors = {
        "반도체": ["반도체", "삼성전자", "SK하이닉스", "엔비디아", "칩"],
        "에너지/유가": ["유가", "에너지", "정유", "가스", "배터리"],
        "금융/금리": ["금리", "은행", "금융", "연준", "환율"],
        "조선": ["조선", "선박", "LNG선", "해운"],
        "자동차": ["자동차", "현대차", "기아", "테슬라"],
        "건설": ["건설", "부동산", "아파트"]
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
    st.info("데이터 로딩 중...")

st.markdown("<p style='text-align: center; color: #6c757d; font-size: 0.8rem;'>Vibe Coding Pro v3.7 | Commander's Secure Terminal</p>", unsafe_allow_html=True)
