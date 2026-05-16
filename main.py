import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정 및 테마 강제 고정
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [가독성 정예화 디자인] 사령관의 눈을 위한 최종 시각 최적화
st.markdown("""
    <style>
    /* 배경색 고정 */
    .stApp { background-color: #f1f3f5 !important; }
    
    /* 상단 헤더: 남색 배경 + 순백색 제목 */
    .header-box {
        background-color: #0c1c4f !important;
        padding: 25px; border-radius: 12px; margin-bottom: 30px; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .header-box h2 { color: #ffffff !important; font-weight: 900 !important; margin: 0 !important; font-size: 1.8rem !important; }

    /* 지표 카드 스타일 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    label[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 800 !important; font-size: 1.1rem !important; }
    
    /* ❗ 지수 숫자: 완전한 검정색 (시인성 극대화) */
    div[data-testid="stMetricValue"] { 
        color: #000000 !important; 
        font-weight: 900 !important; 
        font-size: 2.3rem !important; 
    }

    /* 🟢 상승(녹색) 수치: 네온 에메랄드 뱃지 (채도 폭발) */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #ffffff !important;           
        background-color: #00c853 !important; 
        font-weight: 900 !important;
        padding: 5px 14px !important;
        border-radius: 10px !important;
        font-size: 1.25rem !important;
        box-shadow: 0 0 10px rgba(0, 200, 83, 0.4);
    }

    /* 🔴 하락(빨간색) 수치: 기본 대비 유지 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Down"]) {
        color: #dc2626 !important;
        font-weight: 600 !important;
    }

    /* 뉴스 섹션 */
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
        padding: 18px; border-radius: 12px; margin-bottom: 12px;
        border: 1px solid #cbd5e1 !important;
        display: flex; align-items: center;
    }
    .sector-tag {
        background-color: #0c1c4f; color: #ffffff !important;
        padding: 5px 12px; border-radius: 6px; font-size: 0.85rem;
        font-weight: 900; margin-right: 15px; white-space: nowrap;
    }
    .news-link { color: #000000 !important; font-weight: 800 !important; font-size: 1.1rem !important; text-decoration: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown('<div class="header-box"><h2>🚀 Vibe Economy Dashboard</h2></div>', unsafe_allow_html=True)

# 2. 데이터 수집 엔진 (간소화 버전)
@st.cache_data(ttl=300)
def get_eco(ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        val = d['Close'].iloc[-1]
        diff = val - d['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

# 3. 실시간 지표 (깔끔한 2열 배치)
indices = {"🇺🇸 국채 10년": "^TNX", "🛢️ WTI 유가": "CL=F", "💵 환율(USD)": "USDKRW=X", "🇰🇷 KOSPI": "^KS11", "🇺🇸 NASDAQ": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_eco(ticker)
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

st.markdown('<p class="section-header">📰 섹터별 주요 소식 (Top 5)</p>', unsafe_allow_html=True)

# 4. 뉴스 섹터 분류 및 출력
def classify_sector(title):
    sectors = {"반도체": ["반도체", "삼성전자", "하이닉스", "엔비디아"], "건설/부동산": ["건설", "부동산", "아파트"], "조선/해운": ["조선", "선박", "해운"], "자동차": ["자동차", "전기차", "현대차"], "금융": ["금리", "환율", "연준", "은행"]}
    for sector, keywords in sectors.items():
        if any(kw in title for kw in keywords): return sector
    return "경제일반"

@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

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

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v4.1 | Clean & Fast Mode</p>", unsafe_allow_html=True)
