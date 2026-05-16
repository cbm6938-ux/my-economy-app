import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [최종 시각화 조치] 초록색 수치 폭발적 가시성 + 뉴스 섹터 태그 디자인
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc !important; }
    
    /* 상단 헤더: 남색 배경 + 순백색 글자 강제 고정 */
    .header-box {
        background-color: #1e3a8a !important;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
    }
    .header-box h2 { color: #ffffff !important; font-weight: 800 !important; margin: 0 !important; }
    .header-box p { color: #cbd5e1 !important; font-size: 0.9rem !important; }

    /* 지표 카드 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    label[data-testid="stMetricLabel"] { color: #475569 !important; font-weight: 700 !important; font-size: 1rem !important; }
    div[data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 900 !important; font-size: 1.9rem !important; }

    /* 🟢 [초정밀 타격] 상승(초록색) 지표 가시성 극대화 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #ffffff !important; 
        background-color: #059669 !important; /* 진한 에메랄드 배경 */
        font-weight: 900 !important;
        padding: 4px 12px !important;
        border-radius: 8px !important;
        font-size: 1.1rem !important;
        box-shadow: 0 2px 4px rgba(5, 150, 105, 0.3);
    }

    /* 하단 섹션 제목 선명하게 */
    .section-header {
        color: #0f172a !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        border-left: 8px solid #1e3a8a;
        padding-left: 15px;
        margin: 40px 0 20px 0;
    }

    /* 뉴스 카드 및 섹터 태그 */
    .news-card {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #e2e8f0 !important;
        display: flex;
        align-items: center;
    }
    .sector-tag {
        background-color: #f1f5f9;
        color: #1e3a8a;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 800;
        margin-right: 15px;
        white-space: nowrap;
        border: 1px solid #cbd5e1;
    }
    .news-link { color: #1e293b !important; font-weight: 700 !important; font-size: 1.05rem !important; text-decoration: none !important; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

# --- 헤더 ---
st.markdown(f"""
    <div class="header-box">
        <h2>🚀 Vibe Economy Dashboard</h2>
        <p>사령관의 실시간 종목별 뉴스 기지 | {datetime.now().strftime("%Y.%m.%d %H:%M")} Live</p>
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
st.markdown('<p class="section-header">📰 주요 섹터별 실시간 뉴스</p>', unsafe_allow_html=True)

# 4. 섹터 분류 엔진
def classify_sector(title):
    sectors = {
        "반도체": ["반도체", "삼성전자", "SK하이닉스", "엔비디아", "칩"],
        "건설": ["건설", "부동산", "아파트", "주택", "토목"],
        "조선": ["조선", "선박", "컨테이너", "해운", "LNG선"],
        "우주/항공": ["우주", "항공", "위성", "나사", "발사"],
        "에너지/유가": ["유가", "에너지", "정유", "가스", "배터리", "2차전지"],
        "금융/금리": ["금리", "은행", "금융", "연준", "환율", "증시"],
        "자동차": ["자동차", "전기차", "현대차", "기아", "테슬라"],
        "빅테크/AI": ["AI", "인공지능", "구글", "애플", "MS", "메타"]
    }
    for sector, keywords in sectors.items():
        if any(kw in title for kw in keywords):
            return sector
    return "경제일반"

@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:7] # 뉴스 7개로 증강

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

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v3.6 | Tactical Sector Tagging Mode</p>", unsafe_allow_html=True)
